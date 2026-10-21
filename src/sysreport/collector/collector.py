import os
import sys

from sysreport.utils.cpu import CPUInfo
from sysreport.utils.disk import DiskUsage
from sysreport.utils.memory import MemoryUsage
from sysreport.utils.power import PowerSupplyStatus
from sysreport.utils.system import SystemSpecs


class ReportCollector:
    @staticmethod
    def collect(args) -> dict:
        VALID_FIELDS = ("all", "cpu", "mem", "system", "disk", "power")

        fields = args.collect.split(",")

        if "all" in fields and len(fields) > 1:
            print(
                "Error: Cant use field 'all' along side another report field.",
                file=sys.stderr,
            )
            sys.exit(2)

        for f in fields:
            if f not in VALID_FIELDS:
                print(
                    f"Error: Invalid field '{f}' used. May only use: {VALID_FIELDS}",
                    file=sys.stderr,
                )
                sys.exit(2)

        report = {}

        if "cpu" in fields or "all" in fields:
            report["cpu"] = CPUInfo.get_cpu_info_report()

        if "disk" in fields or "all" in fields:
            report["disk"] = {}
            report["disk"]["/"] = DiskUsage.get_disk_usage_report("/")
            if os.path.exists("/sys/firmware/efi"):
                report["disk"]["/boot"] = DiskUsage.get_disk_usage_report("/boot")

        if "mem" in fields or "all" in fields:
            report["memory"] = MemoryUsage.get_memory_report()

        if "power" in fields or "all" in fields:
            report["power_supply"] = PowerSupplyStatus.get_power_supply_report()

        if "system" in fields or "all" in fields:
            report["system"] = SystemSpecs.get_system_specs_report()

        return report
