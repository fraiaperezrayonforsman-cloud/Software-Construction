# Smart House

**HS25  SoCo-group  004**

## Project Introduction

The goal of our project was to employ Smart House Management and test its functionality through multiple tests. 
We implemented three types of home devices: Lights, Thermostats and Cameras. 

In the table below, we described the specific methods for each class:
| Light| Thermostat | Camera |
|-----------|-----------|-----------|
| get_power_consumption() | get_power_consumption() | get_power_consumption() |
| describe_device() | describe_device() | describe_device() |
| - | set target temperature(temperature) | - |
| - | get target temperature() | - |

Each class was implemented using Python dictionaries. 

## Smart House Management

In order to track all devices and manage them we employed a global list. Every time when a new device is created, its instance is appended to this list.
The functions of the SmartHouseManagement class were represented in the table below:
|SmartHouseManagement|
|-----------|
| calculate_total_power_consumption (search_type = None, search_room = None) | 
| get_all_device_description (search_type = None, search_room = None) | 
| get_all_connected_devices (ip = None) | 

Thanks to keyword arguments (search_room and search_type) we can calculate power consumption only for devices in a specific room or of a specific type. 
Additionally, we can also get device descriptions for them or view  power consumption and device descriptions for devices connected to a specific IP address. 

## Tests
Testing of Smart House System:
Three test functions are conducted. All test functions are generalizable to the three subclasses Light, Thermostat and Camera. 

1. The first test tests the correct base structure and storage of new device instances. We considered this is a 
crucial aspect to test for the correct execution of the rest of the code. To do this we assert that each new instances
include all the minimal characteristics of a device. Furthermore, we assert that each new instance is being added 
correctly to the list all_devices. If instances weren't being stored correctly, all smarthouse management functions would fail.

2. By testing total power consumption, besides testing whether total consumption is being calculated correctly or not (with or without room and type conditions)
we can be sure that the attributes corresponding to each individual subclass are also
being stored correctly to new instances. This attributes are necessary for all power consumption functions as well as describe functions.

3. By testing connectivty, besides testing the correct functioning of the connect function, we also test whether
the make and find functions work as expected for subclasses with two parent classes, i.e. Thermostat and Camera. In other words, whether 
attributes and functions in the Connect class are accessible for their child classes.

Since the test functions are generalizable we test all three subclasses through all three tests, thus assuring robustness across subclasses. 
The subclass Light is also tested in the 3rd test expecting the it to fail, given that it doesn't inherit from the Connect parent class. 

Furthermore, we make sure that only test named global variables are called by adding a callable condition to the run_test function. Only test named functions are called
and other test named variables are left out. 

Additionally, we add a --select command to be able to filter tests by subclasses. 

## Authors 
Julie Truc Dao

Fraia Pérez-Rayón

Natalia Piegat

