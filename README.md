# linux-sysreport

linux-sysreport is a CLI tool made with Python for Linux subsystems focused on, as the name implies, reporting the status of the system.

## Installation

For a quick, rapid installation, you can use the _[install.sh](./install.sh)_ script.
If you cant execute it remember to give it execution permissions with: `chmod +x install.sh`

Otherwise, if youd like to do the installation manually, here are the steps:

1. Create a virtual environment: `python -m venv venv`
2. Activate the environment: `source venv/bin/activate`
3. Install the required dependencies with `pip install -e .`
4. To create the final binary, run pyinstaller: `pyinstaller --onefile --name=sysreport src/sysreport/core.py`

And thats it! If you didnt specify a `distpath` with pyinstaller, your binary will be at `./dist/sysreport`

> NOTE: If you want to modify the source code, run: `pip install --group dev`.
It will install all developers dependencies. You can then run the program with: `./src/sysreport/core.py`

## Report

The report includes various fields from the system, this includes:

### System specs

- Distro name
- Distro version
- Kernel name
- Kernel version
- Machine architecture
- Uptime (seconds)

### CPU information

- CPU model
- Load average (1, 5, 15)
- Core temperature in millicelcius (°C)
- Frequency of each individual core (KHz)
- Average frequency of all cores (KHz)
- CPU usage (%)

> NOTE: CPU usage takes a 0.5 seconds time interval to be executed

### Disk usage

Reports the state of the root `/` disk partition. If running on UEFI, reports the state of `/boot` following the same fields.

- Device mounted (`/dev/sdaX`, `/dev/nvme0n1pX`)
- Filesystem type
- Total disk size (bytes)
- Free disk space (bytes)
- Available disk space (bytes)

### Memory usage

- Total RAM (kB)
- RAM available (kB)
- Total Swap (kB)
- Swap available (kB)

## Command options

- `--json`: Returns a one-liner JSON string.
- `--json-pretty`: Returns a prettyfied JSON dictionary.

## Output example

### No options (normal run)

```
System specs

Distro: NixOS 26.11 x86_64
Kernel: Linux 7.2.10
Uptime: 3 hours 52 minutes

-----------------

CPU information

CPU: AMD Ryzen 5 7520U with Radeon Graphics -- 4.48%
Load average: 0.76, 0.99, 1.13
Core temperature: 55.0 °C
Core frequency: 
	0: 1.11 GHz
	1: 1.11 GHz
	2: 1.11 GHz
	3: 2.57 GHz
	4: 1.11 GHz
	5: 1.26 GHz
	6: 1.81 GHz
	7: 2.74 GHz
Average core frequency: 1.6 GHz

-----------------

Disk usage

/boot
Device mounted: /dev/nvme0n1p1
Filesystem: vfat
Total storage: 1.07 GB
Used storage: (0.23/1.07) GB -- 27.8%
Available storage: 0.84 GB

/
Device mounted: /dev/nvme0n1p2
Filesystem: ext4
Total storage: 385.68 GB
Used storage: (68.15/385.68) GB -- 22.88%
Available storage: 297.86 GB

-----------------

Memory usage

RAM total: 7.56 GB
RAM used: 5.48 GB -- 72.49%
Swap total: 13.23 GB
Swap used: 0.69 GB -- 5.23%

-----------------

Power supply status

AC0
Connected to current: yes

BAT0
Model: OEM -- X160535
Voltage: 12.54 V
Capacity: 100% -- Full, Fully charged
Battery health: 75.89%
```

### Ran with `--json`

```
{"cpu": {"cpu_model": "AMD Ryzen 5 7520U with Radeon Graphics", "load_average": [0.83837890625, 0.96435546875, 1.1083984375], "cpu_temp": 55000.0, "cpu_khz": {"0": 2631666, "1": 1109831, "2": 2676434, "3": 2719825, "4": 1918139, "5": 1109831, "6": 2754696, "7": 2801561}, "cpu_usage": 6.716417910447758}, "disk": {"/": {"total_space": 385676742656, "free_space": 317526855680, "usable_space": 297860608000, "mount_device": "/dev/nvme0n1p2", "disk_fs_type": "ext4"}, "/boot": {"total_space": 1071628288, "free_space": 838496256, "usable_space": 838496256, "mount_device": "/dev/nvme0n1p1", "disk_fs_type": "vfat"}}, "memory": {"memtotal": 7384720, "memavailable": 2035488, "swaptotal": 12919496, "swapfree": 12244400}, "power_supply": [{"power_supply_name": "AC0", "power_supply_type": "Mains", "power_supply_online": 1}, {"power_supply_name": "BAT0", "power_supply_type": "Battery", "power_supply_status": "Full", "power_supply_present": 1, "power_supply_technology": "Li-ion", "power_supply_cycle_count": 0, "power_supply_voltage_min_design": 11850000, "power_supply_voltage_now": 12543000, "power_supply_current_now": 0, "power_supply_charge_full_design": 3550000, "power_supply_charge_full": 2694000, "power_supply_charge_now": 2694000, "power_supply_capacity": 100, "power_supply_capacity_level": "Full", "power_supply_model_name": "X160535", "power_supply_manufacturer": "OEM", "power_supply_serial_number": ""}], "system": {"name": "NixOS", "version_id": "26.11", "k_ver": "7.2.10", "arch": "x86_64", "k_name": "Linux", "uptime": 13998.14004529953}}```
```

### Ran with `--json-pretty`

```
{
	"cpu": {
		"cpu_model": "AMD Ryzen 5 7520U with Radeon Graphics",
		"load_average": [
			0.86962890625,
			0.9658203125,
			1.10693359375
		],
		"cpu_temp": 56000.0,
		"cpu_khz": {
			"0": 2495167,
			"1": 2654677,
			"2": 2571383,
			"3": 1263313,
			"4": 1550114,
			"5": 2631660,
			"6": 1837174,
			"7": 1699612
		},
		"cpu_usage": 4.455445544554459
	},
	"disk": {
		"/": {
			"total_space": 385676742656,
			"free_space": 317526851584,
			"usable_space": 297860603904,
			"mount_device": "/dev/nvme0n1p2",
			"disk_fs_type": "ext4"
		},
		"/boot": {
			"total_space": 1071628288,
			"free_space": 838496256,
			"usable_space": 838496256,
			"mount_device": "/dev/nvme0n1p1",
			"disk_fs_type": "vfat"
		}
	},
	"memory": {
		"memtotal": 7384720,
		"memavailable": 2034632,
		"swaptotal": 12919496,
		"swapfree": 12244420
	},
	"power_supply": [
		{
			"power_supply_name": "AC0",
			"power_supply_type": "Mains",
			"power_supply_online": 1
		},
		{
			"power_supply_name": "BAT0",
			"power_supply_type": "Battery",
			"power_supply_status": "Full",
			"power_supply_present": 1,
			"power_supply_technology": "Li-ion",
			"power_supply_cycle_count": 0,
			"power_supply_voltage_min_design": 11850000,
			"power_supply_voltage_now": 12544000,
			"power_supply_current_now": 0,
			"power_supply_charge_full_design": 3550000,
			"power_supply_charge_full": 2694000,
			"power_supply_charge_now": 2694000,
			"power_supply_capacity": 100,
			"power_supply_capacity_level": "Full",
			"power_supply_model_name": "X160535",
			"power_supply_manufacturer": "OEM",
			"power_supply_serial_number": ""
		}
	],
	"system": {
		"name": "NixOS",
		"version_id": "26.11",
		"k_ver": "7.2.10",
		"arch": "x86_64",
		"k_name": "Linux",
		"uptime": 14010.860024318696
	}
}
```

## Troubleshooting and contributions

If you encounter any problem or have a suggestion,
feel free to open an issue! Ill be glad to help you out

## Future development

This first version only includes reports for system specs, CPU information, disk usage, and memory usage.
In future versions it is expected to include:

- Processes report
- Network report
