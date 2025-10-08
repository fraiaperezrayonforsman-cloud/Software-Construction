#PARENT CLASS DEVICE
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

def call(self, method_name, *args):
    method = find(self["_class"], method_name)
    return method(self, *args)

def find(cls, method_name):
    while cls is not None:
        if method_name in cls:
            return cls[method_name]
        cls = cls["_parent"]
    raise NotImplementedError("method_name")

def get_power_consumption(self):
    return call(self, "get_power_consumption")

def describe_device(self):
    return call(self, "describe_device")

Device = {
    "get_power_consumption": get_power_consumption,
    "describe_device": describe_device,
    "toggle_status": toggle_status,
    "_classname": "Device",
    "_new": device_new
}


#CREATE NEW 
def make(cls, *args):
    return cls["_new"](*args)


#PARENT CLASS CONNECTABLE
def conntectable_new():
    return {
        "connected": False,
        "ip": None
    }

def connect(self, ip):
    self["connected"] = True
    self["ip"] = ip

def disconnect(self):
    self["connected"] = False

def is_connected(self):
    if self["connected"] == True:
        return f"It is currently connected to server {self["ip"]}."
    else:
        return "It is currently disconnected."

Connectable = {
    "connect": connect,
    "disconnect": disconnect,
    "is_connected": is_connected,
    "_new": conntectable_new,
    "_classname": "Connectable",
}


#SUBCLASS LIGHT
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
#print(light_description(bedroom_light))
toggle_status(bedroom_light)
print(get_power_consumption(bedroom_light))
print(describe_device(bedroom_light))


#SUBCLASS THERMOSTAT
def thermostat_new(name, location, basepower, status, room_temperature, target_temperature):
    therm_c = make(Connectable)
    therm_d = make(Device, name, location, basepower, status)
    return (therm_c | therm_d) | {
            "room_temperature": room_temperature,
            "target_temperature": target_temperature,
            "_class": Thermostat
    }

def thermostat_consumption(self):
    return self["basepower"] * abs(self["target_temperature"] - self["room_temperature"])

def thermostat_description(self):
    return f"The {self["name"]} is located in the {self["location"]}, is currently {self["status"]}, and is currently set to {self["target_temperature"]} degrees Celsius in an {self["room_temperature"]} degree room. {is_connected(self)}"

Thermostat = {
    "get_power_consumption": thermostat_consumption,
    "describe_device": thermostat_description,
    "_new": thermostat_new,
    "_classname": "Thermostat"
}

bathroom_thermostat = make(Thermostat, "Towel Thermostat", "Bathroom", 1200, "on", 18, 24)
connect(bathroom_thermostat, "10.10.10.4")
#print(thermostat_description(bathroom_thermostat))

#SUBCLASS CAMERA 
def camera_new(name, location, basepower, status, resolution_factor):
    therm_c = make(Connectable)
    therm_d = make(Device, name, location, basepower, status)
    return (therm_c | therm_d) | {
            "resolution_factor": resolution_factor,
            "_class": Camera
    }

def camera_consumption(self):
    return self["basepower"] * self["resolution_factor"]

def camera_description(self):
    factor = "medium"
    if self["resolution_factor"] < 5:
        factor = "low"
    if self["resolution_factor"] >= 10:
        factor = "high"
    return f"The {self["name"]} is located in the {self["location"]}, is currently {self["status"]}, and is a {factor} resolution sensor. {is_connected(self)}"

Camera = {
    "get_power_consumption": camera_consumption,
    "describe_device": camera_description,
    "_new": camera_new,
    "_classname": "Camera"
}

living_room_camera = make(Camera, "New RGB Camera", "Living Room", 500, "on", 8)
#print(camera_description(living_room_camera))