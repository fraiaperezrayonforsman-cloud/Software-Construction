#GLOBAL DEVICES LIST 
all_devices = []
#PARENT CLASS DEVICE
def toggle_status(self):
    if self["status"] == "on":
        self["status"] = "off"
    else:
        self["status"] = "on"
    return self["status"]

def device_new(name, location, base_power, status):
    return {
        "name": name,
        "location": location,
        "base_power": base_power,
        "status": status,
        "_class": Device
    }

def call(self, method_name, *args,**kwargs):
    method = find(self["_class"], method_name)
    return method(self, *args, **kwargs)

def find(cls, method_name):
    if method_name in cls:
        return cls[method_name]
    for parent in cls.get("_parent", []):
        if isinstance(parent, dict):
            try:
                method = find(parent, method_name)
                if method:
                    return method
            except NotImplementedError:
                continue
    raise NotImplementedError("method not found")

def get_power_consumption(self):
    raise NotImplementedError("get_power_consumption")

def describe_device(self):
    raise NotImplementedError("describe_device")

Device = {
    "get_power_consumption": get_power_consumption,
    "describe_device": describe_device,
    "toggle_status": toggle_status,
    "_classname": "Device",
    "_new": device_new
}


#CREATE NEW 
def make(cls, *args):
    device = cls["_new"](*args)
    return device  


#PARENT CLASS CONNECTABLE
def connectable_new():
    return {
        "connected": False,
        "ip": None,
        "_class": Connectable,
    }

def connect(self, ip):
    self["connected"] = True
    self["ip"] = ip

def disconnect(self):
    self["connected"] = False

def is_connected(self):
    if self["connected"] == True:
        return f"It is currently connected to server {self['ip']}."
    else:
        return "It is currently disconnected."

Connectable = {
    "connect": connect,
    "disconnect": disconnect,
    "is_connected": is_connected,
    "_new": connectable_new,
    "_classname": "Connectable",
}

#SUBCLASS LIGHT
def light_consumption(self):
    if self["status"] != "on":
        return 0
    return round(self["base_power"] * (self["brightness"]/100))

def light_description(self):
    return f"The {self['name']} is located in the {self['location']}, is currently {self['status']} and is currently set to {self['brightness']}% brightness."

def light_new(name, location, base_power, status, brightness):
    return make(Device, name, location, base_power, status) | {
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


#SUBCLASS THERMOSTAT
def thermostat_new(name, location, base_power, status, room_temperature, target_temperature):
    therm_c = make(Connectable)
    therm_d = make(Device, name, location, base_power, status)
    return (therm_c | therm_d) | {
            "room_temperature": room_temperature,
            "target_temperature": target_temperature,
            "_class": Thermostat
    }

def thermostat_consumption(self):
    if self["status"] != "on":
        return 0
    return self["base_power"] * abs(self["target_temperature"] - self["room_temperature"])

def thermostat_description(self):
    return f"The {self['name']} is located in the {self['location']}, is currently {self['status']}, and is currently set to {self['target_temperature']} degrees Celsius in an {self['room_temperature']} degree room. {is_connected(self)}"

Thermostat = {
    "get_power_consumption": thermostat_consumption,
    "describe_device": thermostat_description,
    "_new": thermostat_new,
    "_classname": "Thermostat",
    "_parent": [Device, Connectable]
}

def set_target_temperature(self, temperature):
    self["target_temperature"] = temperature

def get_target_temperature(self):
    return self["target_temperature"]

#SUBCLASS CAMERA 
def camera_new(name, location, base_power, status, resolution_factor):
    therm_c = make(Connectable)
    therm_d = make(Device, name, location, base_power, status)
    return (therm_c | therm_d) | {
            "resolution_factor": resolution_factor,
            "_class": Camera
    }

def camera_consumption(self):
    if self["status"] != "on":
        return 0
    return self["base_power"] * self["resolution_factor"]

def camera_description(self):
    factor = "medium"
    if self["resolution_factor"] < 5:
        factor = "low"
    if self["resolution_factor"] >= 10:
        factor = "high"
    return f"The {self['name']} is located in the {self['location']}, is currently {self['status']}, and is a {factor} resolution sensor. {is_connected(self)}"

Camera = {
    "get_power_consumption": camera_consumption,
    "describe_device": camera_description,
    "_new": camera_new,
    "_classname": "Camera",
    "_parent": [Device, Connectable]
}


#SMART_HOUSE_FUNCTIONS
def calculate_total_power_consumption(self,search_type = None, search_room = None):
    total_consumption = 0
    for device in all_devices:
        if device['location'] != search_room and search_room is not None:
            continue
        if device["_class"]["_classname"] != search_type and search_type is not None:
            continue
        total_consumption += call(device,"get_power_consumption")
    return total_consumption

def get_all_connected_devices(self,ip = None):
    power_consumption = 0
    descriptions = []
    for device in all_devices:
        if device["_class"]["_classname"] in ["Light"]:
            continue
        if device["connected"] == False:
            continue
        if device['status'] == 'off':
            continue 
        if ip is not None and device["ip"] != ip:
            continue
        power_consumption += call(device, 'get_power_consumption')
        desc = call(device, 'describe_device')
        descriptions.append(desc)
    return power_consumption,descriptions

def get_all_device_description(self,search_type = None, search_room = None):
    descriptions = []
    for device in all_devices:
        if search_room is not None and device["location"] != search_room:
            continue
        if search_type is not None and device["_class"]["_classname"] != search_type:
            continue
        desc = call(device, "describe_device")
        descriptions.append(desc)
    return descriptions

#SMARTHOUSE 
def SmartHouseManagement_new(name,search_type = None,search_room = None):
    return {
        "name": name,
        "_class": SmartHouseManagement,
        "search_type":search_type,
        "search_name": search_room
    }

SmartHouseManagement = {
    "_classname": "SmartHouseManagement",
    "calculate_total_power_consumption": calculate_total_power_consumption,
    "get_all_device_description" : get_all_device_description,
    "get_all_connected_devices" : get_all_connected_devices,
    "_new": SmartHouseManagement_new
}

#EXAMPLES
bedroom_light = make(Light, "Bedtable Light", "Bedroom", 300, "off", 70)
living_room_camera = make(Camera, "New RGB Camera", "Living Room", 500, "on", 8)
bathroom_thermostat = make(Thermostat, "Towel Thermostat", "Bathroom", 1200, "on", 18, 24)

examples = [bedroom_light, living_room_camera, bathroom_thermostat]
toggle_status(bedroom_light)
connect(bathroom_thermostat, "10.10.10.4")
for ex in examples:
    n = ex["name"]
    d_i = call(ex, "describe_device")
    print(f"{n}: {d_i}")

disconnect(bathroom_thermostat)
print(call(bathroom_thermostat, "describe_device"))
set_target_temperature(bathroom_thermostat, 30)
print(get_target_temperature(bathroom_thermostat))

#SMART_HOUSE_TESTING
smart_house = make(SmartHouseManagement, "Alexa")
print(call(smart_house,"calculate_total_power_consumption", search_room = "Bedroom"))

#MORE_DEVICES
bedroom_thermostat = make(Thermostat, "Bed Thermostat", "Bedroom", 800, "on", 20,25)
bedroom_camera = make(Camera,"Bed Camera","Bedroom",500,"on", 10 )

#TURNING_DEVICES_ON_AND_OFF
print(call(smart_house,"calculate_total_power_consumption", search_room = "Bedroom"))
toggle_status(bedroom_camera)
toggle_status(bedroom_thermostat)
print(call(smart_house,"calculate_total_power_consumption", search_room = "Bedroom"))

#CHANGING_TEMPERATURE
toggle_status(bedroom_thermostat)
print(call(smart_house,"get_all_device_description", search_room = "Bedroom", search_type = "Thermostat"))
print(call(smart_house,"calculate_total_power_consumption", search_room = "Bedroom"))
set_target_temperature(bedroom_thermostat, 30)
print(call(smart_house,"get_all_device_description", search_room = "Bedroom", search_type = "Thermostat"))
print(call(smart_house,"calculate_total_power_consumption", search_room = "Bedroom", search_type = "Thermostat"))

#TEST_CONNECTED_DEVICES
connect(bedroom_thermostat,"10.10.10.4")
connect(bathroom_thermostat,"10.10.10.4")
connect(living_room_camera,"11.10.10.4")

#SHOW_DEVICES_CONNECTED_TO_ADDRESS
print(call(smart_house,"get_all_connected_devices","10.10.10.4"))
#SHOW_DEVICES_CONNECTED_TO_ANY_ADDRESS
print(call(smart_house,"get_all_connected_devices"))