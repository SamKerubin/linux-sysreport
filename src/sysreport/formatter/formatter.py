import sys
import json


class ReportFormatter:
    @staticmethod
    def __stringify_cpu_report(report) -> str:
        return ""

    @staticmethod
    def __stringify_disk_report(report) -> str:
        return ""

    @staticmethod
    def __stringify_memory_report(report) -> str:
        return ""

    @staticmethod
    def __stringify_power_supply_report(report) -> str:
        return ""

    @staticmethod
    def __stringify_system_report(report) -> str:
        return ""

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
            disk_report_str = ReportFormatter.__stringify_disk_report(disk_report["/"]) + "\n"
            if "/boot" in disk_report:
                disk_report_str += ReportFormatter.__stringify_disk_report(disk_report["/boot"])

            fields.append(disk_report_str)

        if "memory" in report:
            fields.append(ReportFormatter.__stringify_memory_report(report["memory"]))

        if "power_supply" in report:
            fields.append(ReportFormatter.__stringify_power_supply_report(report["power_supply"]))

        return "\n-----------------".join(fields)
