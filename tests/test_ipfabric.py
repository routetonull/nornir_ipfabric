from nornir import InitNornir

nr = InitNornir(
    inventory={"plugin": "IPFabricInventory"}, logging={"enabled": False}
)


def test_hosts():
    assert len(nr.inventory.hosts) > 0
