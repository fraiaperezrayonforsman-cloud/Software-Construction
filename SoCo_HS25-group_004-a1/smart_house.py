Device = {
    "get_power_consumption": get_power_consumption,
    "describe_device": describe_device,
    "toggle_status": toggle_status,
    "_classname": "Device"
}

def device_new(name, location, basepower, status):
    return {
        "name": name,
        "location": location,
        "basepower": basepower,
        "status": status,
        "_class": Device
    }





def light_consumption(self):
    if self["status"] != "on":
        return 0
    return round(self["basepower"] * (self["brightness"]/100))

def light_description(self):
    return f"The {self["name"]} is located in the {self["location"]}, is currently {self["status"]} and is currently set to {self["brightness"]}% brightness."

Light = {
    "get_power_consumption": light_consumption,
    "describe_device": light_description,
    "_classname": "Light",
    "_parent": Device
}

def light_new(name, location, basepower, status, brightness):
    return {
        "name": name,
        "location": location,
        "basepower": basepower,
        "status": status,
        "brightness": brightness,
        "_class": Light
    }