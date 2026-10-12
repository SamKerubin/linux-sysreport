import os
import time


class SystemSpecs:
    @staticmethod
    def __parse_os_release_properties() -> tuple[str, str]:
        distro_name, distro_version = "", ""

        with open("/etc/os-release", "r", encoding="utf-8") as os_release_file:
            for line in os_release_file:
                if line.startswith("NAME"):
                    distro_name = line.split("=")[1].strip()
                elif line.startswith("VERSION_ID"):
                    distro_version = line.split("=")[1].replace('"', "").strip()

        return distro_name, distro_version

    @staticmethod
    def get_system_specs_report() -> dict[str, str | float]:
        report = {}

        distro_name, distro_version = SystemSpecs.__parse_os_release_properties()

        uname = os.uname()
        before = time.time()
        with open("/proc/uptime", "r", encoding="utf-8") as uptime_file:
            uptime_line = uptime_file.readline()

            after = time.time()
            delta = after - before

            uptime_secs = float(uptime_line.split(" ")[0]) + delta

        report["name"] = distro_name
        report["version_id"] = distro_version
        report["k_ver"] = uname.release
        report["arch"] = uname.machine
        report["uptime"] = uptime_secs

        return report
