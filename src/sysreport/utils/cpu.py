import os


class CPUInfo:
    def __init__(self) -> None:
        self.cpu_model = "Unknown"
        self.__parse_cpu_model()

    def __parse_cpu_model(self) -> None:
        with open("/proc/cpuinfo", "r", encoding="utf-8") as cpu_info:
            for line in cpu_info:
                if line.startswith("model name"):
                    self.cpu_model = line.split(":")[1].strip()
                    break

    def get_cpu_model(self) -> str:
        return self.cpu_model

    def get_load_average(self) -> tuple[float, float, float]:
        return os.getloadavg()
