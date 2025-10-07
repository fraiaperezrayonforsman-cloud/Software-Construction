def toggle_status(self):
    if self["status"] == "on":
        self["status"] = "off"
    else:
        self["status"] = "on"
    return self["status"]

def device_new(name, location, basepower, status):
    return {
        "name": name,
        "location": location,
        "basepower": basepower,
        "status": status,
        "_class": Device
    }

Device = {
    #"get_power_consumption": get_power_consumption,
    #"describe_device": describe_device,
    "toggle_status": toggle_status,
    "_classname": "Device",
    "_new": device_new
}







def make(cls, *args):
    return cls["_new"](*args)




def light_consumption(self):
    if self["status"] != "on":
        return 0
    return round(self["basepower"] * (self["brightness"]/100))

def light_description(self):
    return f"The {self["name"]} is located in the {self["location"]}, is currently {self["status"]} and is currently set to {self["brightness"]}% brightness."

def light_new(name, location, basepower, status, brightness):
    return make(Device, name, location, basepower, status) | {
            "brightness": brightness,
            "_class": Light
    }

Light = {
    "get_power_consumption": light_consumption,
    "describe_device": light_description,
    "_new": light_new,
    "_classname": "Light",
    "_parent": Device,
}

bedroom_light = make(Light, "Bedtable Light", "Bedroom", 300, "off", 70)
print(light_description(bedroom_light))

