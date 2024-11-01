import uuid


def get_mac_address():
    node = uuid.getnode()
    node_hex = hex(node)
    mac = node_hex.replace("0x", "").upper()

    # Format the MAC address as XX:XX:XX:XX:XX:XX
    return ":".join(mac[i : i + 2] for i in range(0, len(mac), 2))
