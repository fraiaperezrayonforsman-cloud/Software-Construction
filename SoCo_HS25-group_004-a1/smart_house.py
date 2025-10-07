Device = {
    "get_power_consumption": get_power_consumption,
    "describe_device": describe_device,
    "toggle_stats": toggle_status,
    "_classname": Device
}

def device_new(name, location, basepower, status):
    return {
        "name": name,
        "location": location,
        "basepower": basepower,
        "status": status,
        "_class": "Device"
    }

