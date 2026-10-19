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

- `--json`:
- `--json-pretty`:

## Output example

### No options (normal run)

```
System specs

Distro: NixOS 26.05 x86_64
Kernel: Linux 7.2.9
Uptime: 57 minutes

-----------------

CPU information

CPU: AMD Ryzen 5 7520U with Radeon Graphics -- 19.85%
Load average: 0.78, 1.11, 1.25
Core temperature: 56.0 °C
Core frequency: 
	0: 2.85 GHz
	1: 2.85 GHz
	2: 2.84 GHz
	3: 2.81 GHz
	4: 1.9 GHz
	5: 2.68 GHz
	6: 2.51 GHz
	7: 2.65 GHz
Average core frequency: 2.64 GHz

-----------------

Disk usage

/boot
Device mounted: /dev/nvme0n1p1
Filesystem: vfat
Total storage: 1.07 GB
Used storage: (0.27/1.07) GB -- 33.89%
Available storage: 0.8 GB

/
Device mounted: /dev/nvme0n1p2
Filesystem: ext4
Total storage: 385.68 GB
Used storage: (51.87/385.68) GB -- 16.51%
Available storage: 314.14 GB

-----------------

Memory usage

RAM total: 7.04 GB
RAM used: 5.28 GB -- 75.0%
Swap total: 12.32 GB
Swap used: 0.24 GB -- 1.98%
```

### Ran with `--json`

```
{"cpu": {"cpu_model": "AMD Ryzen 5 7520U with Radeon Graphics", "load_average": [0.7880859375, 1.25439453125, 1.34423828125], "cpu_temp": 56000.0, "cpu_khz": {"0": 2582359.0, "1": 1109831.0, "2": 2442094.0, "3": 1264282.0, "4": 2497615.0, "5": 2452207.0, "6": 2556110.0, "7": 2640155.0}, "cpu_usage": 7.862407862407861}, "disk": {"/": {"total_space": 385676742656, "free_space": 333805998080, "usable_space": 314139750400, "mount_device": "/dev/nvme0n1p2", "disk_fs_type": "ext4"}, "/boot": {"total_space": 1071628288, "free_space": 800354304, "usable_space": 800354304, "mount_device": "/dev/nvme0n1p1", "disk_fs_type": "vfat"}}, "memory": {"memtotal": 7383696.0, "memavailable": 1588612.0, "swaptotal": 12918984.0, "swapfree": 12637624.0}, "system": {"name": "NixOS", "version_id": "26.05", "k_ver": "7.2.9", "arch": "x86_64", "k_name": "Linux", "uptime": 4047.9800228881836}}
```

### Ran with `--json-pretty`

```
{
	"cpu": {
		"cpu_model": "AMD Ryzen 5 7520U with Radeon Graphics",
		"load_average": [
			0.865234375,
			1.20361328125,
			1.322265625
		],
		"cpu_temp": 56000.0,
		"cpu_khz": {
			"0": 1264402.0,
			"1": 1529683.0,
			"2": 2789436.0,
			"3": 2582881.0,
			"4": 1264225.0,
			"5": 2006644.0,
			"6": 2602986.0,
			"7": 2119672.0
		},
		"cpu_usage": 5.940594059405946
	},
	"disk": {
		"/": {
			"total_space": 385676742656,
			"free_space": 333805965312,
			"usable_space": 314139717632,
			"mount_device": "/dev/nvme0n1p2",
			"disk_fs_type": "ext4"
		},
		"/boot": {
			"total_space": 1071628288,
			"free_space": 800354304,
			"usable_space": 800354304,
			"mount_device": "/dev/nvme0n1p1",
			"disk_fs_type": "vfat"
		}
	},
	"memory": {
		"memtotal": 7383696.0,
		"memavailable": 1577416.0,
		"swaptotal": 12918984.0,
		"swapfree": 12637644.0
	},
	"system": {
		"name": "NixOS",
		"version_id": "26.05",
		"k_ver": "7.2.9",
		"arch": "x86_64",
		"k_name": "Linux",
		"uptime": 4093.1900228881836
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
