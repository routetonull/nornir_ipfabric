"""nornir_ipfabric.inventory.ipfabric"""
from base64 import b64encode
from nornir.core.inventory import Defaults
from nornir.core.inventory import Groups
from nornir.core.inventory import Host
from nornir.core.inventory import HostOrGroup
from nornir.core.inventory import Hosts
from nornir.core.inventory import Inventory
from typing import Any
from typing import Dict
from typing import Optional
from typing import Type
from typing import Union

import logging
import os
import requests
import simplejson as json
import urllib3


urllib3.disable_warnings()

logger = logging.getLogger(__name__)


def _get_inventory_element(
    typ: Type[HostOrGroup], device: Dict[str, Any], defaults: Defaults
) -> HostOrGroup:
    # map IPF family to netmiko platform names / netmiko device_type
    # list of IP Fabric supported device families https://docs.ipfabric.io/matrix/
    # list of netmiko supported device_types https://github.com/ktbyers/netmiko/blob/master/netmiko/ssh_dispatcher.py
    netmiko_platform_map = {
        "asa": "cisco_asa",
        "ios-xe": "cisco_xe",
        "ios-xr": "cisco_xr",
        "nx-os": "cisco_nxos",
        "wlc-air": "cisco_wlc",
        "pa-vm": "paloalto",
    }
    # napalm platform mapping https://napalm.readthedocs.io/en/latest/support/
    napalm_platform_map = {
        "nx-os": "nxos_ssh",
        "ios-xe": "ios",
        "ios-rx": "iosxr",
    }
    data = {}
    data["address"] = (device.get("loginIp"),)
    data["family"] = device.get("family") or device.get("vendor")
    data["hostname"] = device.get("hostname")
    data["platform"] = device.get("platform")
    data["protocol"] = device.get("loginType")
    data["serial"] = device.get("sn")
    data["siteName"] = device.get("siteName")
    data["vendor"] = device.get("vendor")
    data["version"] = device.get("version")

    return typ(
        name=device.get("loginIp", ""),
        # set netmiko platform, use family or vendor if no match
        platform=netmiko_platform_map.get(
            device["family"], device.get("platform", device.get("vendor", ""))
        ),
        # set groups from site, platform and vendor for filtering
        groups=[
            device.get("siteName", None),
            device.get("platform", None),
            device.get("family", None),
            device.get("vendor", None),
        ],
        data=data,
        # set napalm platform
        connection_options={
            "napalm": {
                "platform": napalm_platform_map.get(
                    data["family"], data["family"]
                )
            }
        },
        defaults=defaults,
    )


class IPFabricInventory(Inventory):
    """
    class IPFabricInventory(Inventory):
    """

    def __init__(
        self,
        ipf_url: Optional[str] = None,
        ipf_user: Optional[str] = None,
        ipf_password: Optional[str] = None,
        ipf_snapshot: Optional[str] = "$last",
        ssl_verify: Union[bool, str] = False,
        **kwargs: Any,
    ) -> None:

        """
        IP Fabric plugin
        API docs https://docs.ipfabric.io/api/
        Arguments:
            ipf_url: IP Fabric url, defaults to http://localhost:8080.
            ipf_user: username to access IP Fabric API
            ipf_password: password to access IP Fabric API
            ipf_snapshot: snapshot to read, details here https://docs.ipfabric.io/api/#tables
            ssl_verify: Enable/disable certificate validation or provide path to CA bundle file
        """
        self.ipf_url = (
            ipf_url
            if ipf_url
            else os.environ.get("IPF_URL", "https://localhost")
        )
        self.ipf_user = (
            ipf_user if ipf_user else os.environ.get("IPF_USER", "admin")
        )
        self.ipf_password = (
            ipf_password
            if ipf_password
            else os.environ.get("IPF_PASSWORD", "admin")
        )
        self.ipf_snapshot = "$last"
        self.ssl_verify = False

    def load(self) -> Inventory:
        """
        Load inventory
        """

        url = f"{self.ipf_url}/api/v1/tables/inventory/devices"
        credentials = b64encode(
            f"{self.ipf_user}:{self.ipf_password}".encode("utf-8")
        ).decode("utf-8")
        headers = {
            "Content-type": "application/json",
            "Authorization": f"Basic {credentials}",
        }
        data = {
            "columns": [
                "loginIp",
                "family",
                "hostname",
                "platform",
                "loginType",
                "sn",
                "siteName",
                "vendor",
                "version",
            ],
            "filters": {},
            "snapshot": self.ipf_snapshot,
        }
        try:  # get device inventory from IP Fabric
            deviceInventory = requests.post(
                url,
                data=json.dumps(data),
                headers=headers,
                verify=self.ssl_verify,
            )
        except:
            raise ValueError(
                f"Failed to get devices from IP Fabric {self.ipf_url} with user {self.ipf_user}"
            )

        if not deviceInventory.status_code == 200:
            raise ValueError(
                f"Failed to get devices from IP Fabric {self.ipf_url} with user {self.ipf_user}"
            )

        ipf_devices = json.loads(deviceInventory.content).get("data")

        defaults = Defaults()

        groups = Groups()
        defaults = Defaults()

        hosts = Hosts()
        for device in ipf_devices:
            hosts[device.get("loginIp")] = _get_inventory_element(
                Host, device, defaults
            )

        return Inventory(hosts=hosts, groups=groups, defaults=defaults)
