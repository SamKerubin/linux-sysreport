import os
import time


class CPUInfo:
    def __init__(self) -> None:
        self.cpu_model = "Unknown"
        self.cpu_temp = 0.0
        self.cpu_khz = []
        self.cpu_usage = 0.0

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

    def __update_cpu_temp(self) -> None:
        with open(
            "/sys/class/thermal/thermal_zone0/temp", "r", encoding="utf-8"
        ) as cpu_temp:
            line = cpu_temp.readline()
            self.cpu_temp = float(line)

    def get_cpu_temperature_celcius(self) -> float:
        self.__update_cpu_temp()
        return self.cpu_temp

    def __update_cpu_khz(self) -> None:
        self.cpu_khz = []

        BASE_PATH = "/sys/devices/system/cpu/"

        cores = [
            dir
            for dir in os.listdir(BASE_PATH)
            if dir.startswith("cpu") and dir[3:].isdigit()
        ]
        for core in cores:
            path = os.path.join(BASE_PATH, core, "cpufreq/scaling_cur_freq")
            with open(path, "r", encoding="utf-8") as core_freq:
                khz = float(core_freq.readline().strip())
                self.cpu_khz.append(khz)

    def get_cpu_khz(self) -> list[float]:
        self.__update_cpu_khz()
        return self.cpu_khz

    def __read_cpu_activity(self) -> tuple[float, float]:
        with open("/proc/stat", "r", encoding="utf-8") as proc_stat:
            line = proc_stat.readline()

            times = [float(x) for x in line.split()[1:]]
            total = sum(times)
            idle = times[4] + times[3]

            return total, idle

    def __update_cpu_usage(self) -> None:
        total1, idle1 = self.__read_cpu_activity()
        time.sleep(0.5)
        total2, idle2 = self.__read_cpu_activity()

        idle_delta = idle2 - idle1
        total_delta = total2 - total1

        self.cpu_usage = (1.0 - (idle_delta / total_delta)) * 100.0

    def get_cpu_usage(self) -> float:
        self.__update_cpu_usage()
        return self.cpu_usage
