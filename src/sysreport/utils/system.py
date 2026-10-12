import os
import time


class SystemSpecs:
    def __init__(self) -> None:
        self.os_release_properties = {}
        self.uptime_secs = 0.0

        self.__parse_os_release_properties()

    def __parse_os_release_properties(self) -> None:
        with open("/etc/os-release", "r", encoding="utf-8") as os_release_file:
            for line in os_release_file:
                key, value = line.split("=")

                if value.startswith('"'):
                    value = value.replace('"', '')

                key = key.strip("\n")
                value = value.strip("\n")

                self.os_release_properties[key] = value

    def get_distro_name(self) -> str:
        return self.os_release_properties["NAME"]

    def get_distro_version(self) -> str:
        return self.os_release_properties["VERSION_ID"]

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
