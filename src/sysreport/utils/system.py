import os
import time


class SystemSpecs:
    def __init__(self) -> None:
        self.distro_name = ""
        self.distro_version = ""
        self.uptime_secs = 0.0

        self.__parse_os_release_properties()

    def __parse_os_release_properties(self) -> None:
        with open("/etc/os-release", "r", encoding="utf-8") as os_release_file:
            for line in os_release_file:
                if line.startswith("NAME"):
                    self.distro_name = line.split("=")[1].strip()
                elif line.startswith("VERSION_ID"):
                    self.distro_version = line.split("=")[1].replace('"', "").strip()

    def get_distro_name(self) -> str:
        return self.distro_name

    def get_distro_version(self) -> str:
        return self.distro_version

    def __update_uptime_secs(self) -> None:
        before = time.time()
        with open("/proc/uptime", "r", encoding="utf-8") as uptime_file:
            uptime_line = uptime_file.readline()

            after = time.time()
            delta = after - before

            self.uptime_secs = float(uptime_line.split(" ")[0]) + delta

    def get_uptime_seconds(self) -> float:
        self.__update_uptime_secs()
        return self.uptime_secs

    def get_kernel_version(self) -> str:
        return os.uname().release

    def get_system_arch(self) -> str:
        return os.uname().machine
