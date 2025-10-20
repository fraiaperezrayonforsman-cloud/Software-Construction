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

## Authors 
Julie Truc Dao

Fraia Pérez-Rayón

Natalia Piegat

