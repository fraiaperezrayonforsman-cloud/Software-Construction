import smart_house as sh
import sys
import time

#Test States: Implement three possible states for a test: pass, fail, or error.
#check correct addition to all_devices of each new device and its structure
def test_structure(cls, cls_name, *args):
    prev_count = len(sh.all_devices)

    #create a new device
    device = cls["_new"](*args)

    #check correct structure
    assert isinstance(device, dict), f"{cls["name"]} should be a dictionary"
    for attribute in ["name", "location", "base_power", "status", "_class"]:
        assert attribute in device, f"Missing '{attribute}' in {cls["name"]} structure"

    #check correct name assignment
    assert device["_class"]["_classname"] == cls_name, f"Expected classname of {cls_name}, got {device['_class']['_classname']}"

    #check whether correctly included in all_devices
    post_count = len(sh.all_devices)
    if cls_name in ["Light", "Thermostat", "Camera"]:
        assert post_count == prev_count + 1, f"New device {cls_name} not inserted to all devices"
        assert device in sh.all_devices, f"New device {cls_name} missing in all devices"
    else:
        assert prev_count == post_count, f"{cls_name} should not be in all devices"
    
    print(f"{device["name"]} passed structure and registration test")

#check whether total power consumption is being calculated correctly
def test_total_power_consumption(cls, cls_name, *args, search_type = None, search_room = None):
    sh.all_devices.clear()

    device = cls["_new"](*args)
    sh.all_devices.append(device)
    
    #calculate expected power
    expected_pwr = 0
    for device in sh.all_devices:
        if search_room is not None and device["location"] != search_room:
            continue
        if search_type is not None and device["_class"]["_classname"] != search_type:
            continue
        expected_pwr += sh.call(device,"get_power_consumption")
    
    #calculated power
    smarthouse = sh.SmartHouseManagement["_new"]("Test")
    total = sh.call(smarthouse, "calculate_total_power_consumption", search_type=search_type, search_room=search_room)

    assert total == expected_pwr, f"The total power consumption is not being calculated correctly"

    print(f"{device["name"]} passed test on total power, total power consumption is being calculated correctly")

#test whether objects are connected to the given ip-address 
def test_connectivity(cls, cls_name, *args, expected_ip = None):
    device = cls["_new"](*args)

    assert "connected" in device, f"Device {device['name']} not connectable"

    sh.call(device, "connect", expected_ip)

    assert device["connected"] == True, f'Expected {device['name']} to be connected, but it is not'

    assert device["ip"] == expected_ip, f"Expected {device['name']} to be connected to ip{expected_ip}, but is connected to {device["ip"]}"
   
    print(f"{device["name"]} passed connectivity test, total power consumption is being calculated correctly")

#Implement a function that finds and executes all the test functions in your test smart house.py file
#automatically and...
#Implement a command-line option with the --select pattern parameter, allowing you to run only
#the tests that match a specific pattern in their name
def match_pattern():
    pattern = None
    verbose = False

    for i, arg in enumerate(sys.argv):
        if arg == "--select" and i + 1 < len(sys.argv):
            pattern = sys.argv[i + 1].lower()
        elif arg == "--verbose":
            verbose = True
    return pattern, verbose

def setup():
    sh.all_devices.clear()

def teardown():
    sh.all_devices.clear()

def run_tests(test_args):
    pattern, verbose = match_pattern()
    results = {"pass": 0, "fail": 0, "error": 0}

    if verbose:
        print("Variables starting with 'test':")
        for name, obj in globals().items():
            if name.startswith("test"):
                print(f"{name}:{type(obj).__name__}")
        print()

    for name, test in globals().items():
        arg_sets = test_args.get(name, [()])
        if not name.startswith("test_") or not callable(test):
            continue

        if pattern is not None:
            filtered_args = []
            for args in arg_sets:
                # Only match string arguments
                if any(pattern in str(a).lower() for a in args if isinstance(a, str)):
                    filtered_args.append(args)
            arg_sets = filtered_args

        for args in arg_sets:
            start_time = time.time()
            try:
                setup()
                test(*args)
                time_lapse = time.time() - start_time
                results["pass"] += 1
                print(f"{name} passed in {time_lapse}s")
                print("-------------------------------------------------------------------------------------------------------------------------")
            except AssertionError as e:
                time_lapse = time.time() - start_time
                results["fail"] += 1
                print(f"{name} failed: {e} in {time_lapse}s")
                print("-------------------------------------------------------------------------------------------------------------------------")
            except Exception as e:
                time_lapse = time.time() - start_time
                results["error"] += 1
                print(f"{name} error: {e} in {time_lapse}s")
                print("-------------------------------------------------------------------------------------------------------------------------")
            finally:
                teardown()

    print(f"pass {results['pass']}")
    print(f"fail {results['fail']}")
    print(f"error {results['error']}")

TEST_ARGUMENTS = {
    "test_structure": [
        (sh.Light, "Light", "Lamp1", "Living Room", 10, "on", 50),
        (sh.Thermostat, "Thermostat", "Thermo1", "Bedroom", 20, "off", 22, 25),
        (sh.Camera, "Camera", "Cam1", "Kitchen", 15, "on", 5)
    ],
    "test_total_power_consumption": [
        (sh.Light, "Light", "Lamp2", "Living Room", 10, "on", 50),
        (sh.Camera, "Camera", "Cam2", "Kitchen", 20, "on", 5)
    ],
    "test_connectivity": [
        (sh.Camera, "Camera", "Cam3", "Kitchen", 15, "on", 5, "192.168.0.10"),
        (sh.Thermostat, "Thermostat", "Thermo2", "Office", 25, "on", 22, 25, "10.10.10.4"),
        #(sh.Light, "Light", "Lamp3", "Kitchen", 11, "on", 30)
    ]
}

#only functions called test are executed, proof:
test_house = "Smart House 1"

run_tests(TEST_ARGUMENTS)

