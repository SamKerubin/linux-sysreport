import os
import time


class CPUInfo:
    @staticmethod
    def __parse_cpu_model() -> str:
        with open("/proc/cpuinfo", "r", encoding="utf-8") as cpu_info:
            for line in cpu_info:
                if line.startswith("model name"):
                    return line.split(":")[1].strip()

        return "Unknown"

    @staticmethod
    def __parse_cpu_khz_cpuinfo(cpu_id) -> int | None:
        with open("/proc/cpuinfo", "r", encoding="utf-8") as cpu_info:
            content = cpu_info.read()

            for section in content.strip().split("\n\n"):
                fields = {}
                for line in section.splitlines():
                    key, value = line.split(":")

                    fields[key.strip()] = value.strip()

                if fields["processor"] != cpu_id:
                    continue

                try:
                    return int(float(fields["cpu MHz"])) * 1000
                except (ValueError, TypeError, KeyError):
                    return None

        return None

    @staticmethod
    def __read_cpu_activity() -> tuple[float, float]:
        with open("/proc/stat", "r", encoding="utf-8") as proc_stat:
            line = proc_stat.readline()

            times = [float(x) for x in line.split()[1:]]
            total = sum(times)
            idle = times[4] + times[3]

            return total, idle

    @staticmethod
    def get_cpu_info_report() -> dict[str, str | float | dict | tuple]:
        report = {}

        cpu_model = CPUInfo.__parse_cpu_model()

        with open(
            "/sys/class/thermal/thermal_zone0/temp", "r", encoding="utf-8"
        ) as temp:
            line = temp.readline()
            cpu_temp = float(line)

        cpu_khz = []
        CPU_FREQ_BASE_PATH = "/sys/devices/system/cpu/"

        cores = [
            dir
            for dir in os.listdir(CPU_FREQ_BASE_PATH)
            if dir.startswith("cpu") and dir[3:].isdigit()
        ]
        for core in cores:
            path = os.path.join(CPU_FREQ_BASE_PATH, core, "cpufreq/scaling_cur_freq")

            if not os.path.exists(path):
                khz = CPUInfo.__parse_cpu_khz_cpuinfo(core[3:])
                cpu_khz.append(khz)
                continue

            with open(path, "r", encoding="utf-8") as core_freq:
                khz = int(core_freq.readline().strip())
                cpu_khz.append(khz)

        total1, idle1 = CPUInfo.__read_cpu_activity()
        time.sleep(0.5)
        total2, idle2 = CPUInfo.__read_cpu_activity()

        idle_delta = idle2 - idle1
        total_delta = total2 - total1

        cpu_usage = (1.0 - (idle_delta / total_delta)) * 100.0

        report["cpu_model"] = cpu_model
        report["load_average"] = os.getloadavg()
        report["cpu_temp"] = cpu_temp
        report["cpu_khz"] = {x: cpu_khz[x] for x in range(len(cpu_khz))}
        report["cpu_usage"] = cpu_usage

        return report
