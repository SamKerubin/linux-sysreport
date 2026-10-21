import json
import math
import sys


class ReportFormatter:
    @staticmethod
    def __stringify_cpu_report(report) -> str:
        model = report["cpu_model"]
        usage = report["cpu_usage"]
        load1, load5, load15 = report["load_average"]
        temperature = report["cpu_temp"]
        core_freq = report["cpu_khz"]

        temperature_str = (
            f"Core temperature: {math.ceil(temperature / 1000)} °C"
            if temperature
            else "Core temperature: Unknown"
        )

        core_freq_str = "Core frequency:\n"
        individual_core_freq = []
        average_freq = 0.0
        core_count = 0

        for core, freq_khz in core_freq.items():
            if not freq_khz:
                individual_core_freq.append(f"\tC{core}: Unknown\n")
                continue

            freq_ghz = round(freq_khz / 10**6, 2)
            average_freq += freq_ghz
            core_count += 1

            individual_core_freq.append(f"\tC{core}: {freq_ghz} GHz\n")

        average_freq /= core_count

        core_freq_str += "".join(individual_core_freq)
        core_freq_str += f"Average core frequency: {average_freq:.2f} GHz"

        return (
            "\n\nCPU information\n\n"
            f"CPU: {model} -- {math.ceil(usage)}%\n"
            f"Load average: {load1:.2f}, {load5:.2f}, {load15:.2f}\n"
            f"{temperature_str}\n"
            f"{core_freq_str}\n"
        )

    @staticmethod
    def __stringify_disk_report(report) -> str:
        mount_device = report["mount_device"]
        filesystem = report["disk_fs_type"]
        total_storage = report["total_space"]
        free_storage = report["free_space"]
        usable_storage = report["usable_space"]

        used_storage = total_storage - free_storage
        used_storage_percent = math.ceil(
            used_storage / (usable_storage + used_storage) * 100
        )

        return (
            f"Device mounted {mount_device}\n"
            f"Filesystem: {filesystem}\n"
            f"Total storage: {total_storage / 1000**3:.2f} GB\n"
            f"Used storage: ({used_storage / 1000**3:.2f}/{total_storage / 1000**3:.2f}) GB -- {used_storage_percent}%\n"
            f"Available storage: {usable_storage / 1000**3:.2f} GB\n"
        )

    @staticmethod
    def __stringify_memory_report(report) -> str:
        total_memory = report["memtotal"]
        available_memory = report["memavailable"]
        total_swap = report["swaptotal"]
        available_swap = report["swapfree"]

        ram_used = total_memory - available_memory
        ram_used_percent = math.ceil(ram_used / total_memory * 100)

        swap_str = ""
        if total_swap and available_swap:
            swap_used = total_swap - available_swap
            swap_used_percent = math.ceil(swap_used / total_swap * 100)

            swap_str = (
                f"Total Swap: {total_swap * 1.024e-6:.2f} GB\n"
                f"Swap used: {swap_used * 1.024e-6:.2f} GB -- {swap_used_percent}%"
            )

        else:
            swap_str = "No Swap detected"

        return (
            "\n\nMemory usage\n\n"
            f"Total RAM: {total_memory * 1.024e-6:.2f} GB\n"
            f"RAM used: {ram_used * 1.024e-6:.2f} GB -- {ram_used_percent}%\n"
            f"{swap_str}\n"
        )

    @staticmethod
    def __stringify_power_supply_report(report) -> str:
        def stringify_power_supply_device(dev) -> str:
            dev_type = dev["power_supply_type"]
            dev_name = dev["power_supply_name"]

            match dev_type:
                case "Mains":
                    online = dev["power_supply_online"]
                    online_str = ""
                    if online != None:
                        online_str = "yes" if online == 1 else "no"
                    else:
                        online_str = "Unknown"

                    return f"{dev_name}\nConnected to current: {online_str}\n"

                case "Battery":
                    manufacturer = dev["power_supply_manufacturer"]
                    model = dev["power_supply_model_name"]
                    voltage = dev["power_supply_voltage_now"]
                    power = dev["power_supply_power_now"]
                    amper = dev["power_supply_current_now"]
                    status = dev["power_supply_status"]
                    capacity = dev["power_supply_capacity"]
                    capacity_level = dev["power_supply_capacity_level"]
                    charge_full = dev["power_supply_charge_full"]
                    charge_full_design = dev["power_supply_charge_full_design"]

                    model_str = ""
                    if manufacturer:
                        model_str += f"Model: {manufacturer} --"
                    else:
                        model_str += "Model: Unknown manufacturer --"

                    if model:
                        model_str += f" {model}"
                    else:
                        model_str += " Unkown model"

                    voltage_str = ""
                    if voltage:
                        voltage_str += f"Voltage: {voltage / 1000**2:.2f} V"
                    else:
                        voltage_str += "Voltage: Unknown"

                    charge_rate = -1
                    if power:
                        charge_rate = round(power / 1000**2, 2)
                    else:
                        if voltage and amper:
                            charge_rate = round(
                                (voltage / 1000**2) * (amper / 1000**2), 2
                            )

                    status_str = ""
                    if status:
                        if status == "Full":
                            status_str = "Fully charged"
                        elif status == "Discharging":
                            if charge_rate != -1:
                                status_str = f"Discharging at {charge_rate} W"
                            else:
                                status_str = "Discharging at an unknown rate"
                        elif status == "Charging":
                            if charge_rate != -1:
                                status_str = f"Charging at {charge_rate} W"
                            else:
                                status_str = "Charging at an unknown rate"
                        elif status == "Not charging":
                            status_str = "Connected to current. Not charging"
                    else:
                        status_str = "Unknown status"

                    capacity_str = ""
                    if capacity:
                        capacity_str += f"Capacity: {capacity}%"
                    else:
                        capacity_str += "Capacity: Unknown --"

                    if capacity_level:
                        capacity_str += f" {capacity_level}"
                    else:
                        capacity_str += " Unknown capacity level"

                    health_str = ""
                    if charge_full and charge_full_design:
                        health_str = f"Battery health: {math.ceil(charge_full / charge_full_design * 100)}%"
                    else:
                        health_str = "Battery health: Unknown"

                    return (
                        f"{dev_name}\n"
                        f"{model_str}\n"
                        f"{voltage_str}\n"
                        f"{capacity_str}, {status_str}\n"
                        f"{health_str}\n"
                    )

                case _:
                    return f"Unknown device {dev_type}"

        devices = []
        for dev in report:
            devices.append(stringify_power_supply_device(dev))

        return "\n".join(devices)

    @staticmethod
    def __stringify_system_report(report) -> str:
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

        distro = report["name"]
        version_id = report["version_id"]
        arch = report["arch"]
        kernel_name = report["k_name"]
        kernel_version = report["k_ver"]
        uptime = report["uptime"]

        return (
            "\n\nSystem specs\n\n"
            f"Distro: {distro} {version_id} {arch}\n"
            f"Kernel: {kernel_name} {kernel_version}\n"
            f"Uptime: {to_readable_time(uptime)}\n"
        )

    @staticmethod
    def stringify_report(report, args) -> str:
        if args.json and args.json_pretty:
            print(
                "Error: Cant use both [--json] and [--json-pretty] at the same time.",
                file=sys.stderr,
            )
            sys.exit(1)

        if args.json:
            return json.dumps(report)

        if args.json_pretty:
            return json.dumps(report, indent="\t")

        fields = []

        if "system" in report:
            fields.append(ReportFormatter.__stringify_system_report(report["system"]))

        if "cpu" in report:
            fields.append(ReportFormatter.__stringify_cpu_report(report["cpu"]))

        if "disk" in report:
            disk_report = report["disk"]
            disk_report_str = (
                "\n\nDisk usage\n\n"
                + ReportFormatter.__stringify_disk_report(disk_report["/"])
                + "\n"
            )
            if "/boot" in disk_report:
                disk_report_str += ReportFormatter.__stringify_disk_report(
                    disk_report["/boot"]
                )

            fields.append(disk_report_str)

        if "memory" in report:
            fields.append(ReportFormatter.__stringify_memory_report(report["memory"]))

        if "power_supply" in report:
            fields.append(
                "\n\nPower supply status\n\n"
                + ReportFormatter.__stringify_power_supply_report(
                    report["power_supply"]
                )
            )

        return "\n-----------------".join(fields)
