#!/usr/bin/env python

import argparse
import json
import os
import sys

from sysreport.utils.cpu import CPUInfo
from sysreport.utils.disk import DiskUsage
from sysreport.utils.memory import MemoryUsage
from sysreport.utils.system import SystemSpecs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--json",
        action="store_true",
        help="Returns the report in a JSON string format.",
    )

    args = parser.parse_args()

    report = {
        "cpu": CPUInfo.get_cpu_info_report(),
        "disk": {
            "/": DiskUsage.get_disk_usage_report("/"),
            "/boot": DiskUsage.get_disk_usage_report("/boot")
            if os.path.exists("/sys/firmware/efi")
            else {},
        },
        "memory": MemoryUsage.get_memory_report(),
        "system": SystemSpecs.get_system_specs_report(),
    }

    if args.json:
        print(json.dumps(report))
        sys.exit(0)

    def to_readable_time(t) -> str:
        if t == 0:
            return "0 seconds"

        days, t = divmod(t, 86400)
        hours, t = divmod(t, 3600)
        minutes, sec = divmod(t, 60)

        units = [
            (days, "day", "days"),
            (hours, "hour", "hours"),
            (minutes, "minute", "minutes"),
            (sec, "second", "seconds"),
        ]

        parts = []
        for val, singular, plural in units:
            if val > 0:
                unit = singular if val == 1 else plural
                parts.append(f"{int(val)} {unit}")

        if len(parts) == 1:
            return parts[0]

        return " ".join(parts[:-1])

    def print_disk_report(d_rep) -> None:
        if d_rep == {}:
            return

        print(f"Device mounted: {d_rep['mount_device']}")
        print(f"Filesystem: {d_rep['disk_fs_type']}")

        used_storage = d_rep["total_space"] - d_rep["free_space"]
        used_storage_percent = round(used_storage / d_rep["usable_space"] * 100, 2)

        print(f"Total storage: {round(d_rep['total_space'] / 1000**3, 2)} GB")
        print(
            f"Used storage: ({round(used_storage / 1000**3, 2)}/{round(d_rep['total_space'] / 1000**3, 2)}) GB -- {used_storage_percent}%"
        )
        print(f"Available storage: {round(d_rep['usable_space'] / 1000**3, 2)} GB")

        print()

    sys_report = report["system"]

    print("\nSystem specs\n")
    print(
        f"Distro: {sys_report['name']} {sys_report['version_id']} {sys_report['arch']}"
    )
    print(f"Kernel: {sys_report['k_name']} {sys_report['k_ver']}")
    print(f"Uptime: {to_readable_time(sys_report['uptime'])}")

    print("\n-----------------")

    cpu_report = report["cpu"]

    print("\nCPU information\n")
    print(f"CPU: {cpu_report['cpu_model']} -- {round(cpu_report['cpu_usage'], 2)}%")
    print(
        f"Load average: {round(cpu_report['load_average'][0], 2)}, {round(cpu_report['load_average'][1], 2)}, {round(cpu_report['load_average'][2], 2)}"
    )
    print(f"Core temperature: {round(cpu_report['cpu_temp'] / 10**3, 2)} °C")
    print("Core frequency: ")

    average_freq = 0.0

    for core, freq_khz in cpu_report["cpu_khz"].items():
        freq_ghz = round(freq_khz / 10**6, 2)
        print(f"\t{core}: {freq_ghz} GHz")

        average_freq += freq_ghz

    average_freq /= len(cpu_report["cpu_khz"].keys())

    print(f"Average core frequency: {round(average_freq, 2)} GHz")

    print("\n-----------------")

    disk_usage = report["disk"]

    print("\nDisk usage\n")
    if disk_usage["/boot"] != {}:
        print("/boot")
    print_disk_report(disk_usage["/boot"])

    print("/")
    print_disk_report(disk_usage["/"])

    print("-----------------")

    memory_usage = report["memory"]

    ram_used = memory_usage["memtotal"] - memory_usage["memavailable"]
    swap_used = memory_usage["swaptotal"] - memory_usage["swapfree"]

    print("\nMemory usage\n")
    print(f"RAM total: {round(memory_usage['memtotal'] / 1024**2, 2)} GB")
    print(
        f"RAM used: {round(ram_used / 1024**2, 2)} GB -- {round(ram_used / memory_usage['memtotal'] * 100, 2)}%"
    )
    print(f"Swap total: {round(memory_usage['swaptotal'] / 1024**2, 2)} GB")
    print(
        f"Swap used: {round(swap_used / 1024**2, 2)} GB -- {round(swap_used / memory_usage['swaptotal'] * 100, 2)}%"
    )


if __name__ == "__main__":
    main()
