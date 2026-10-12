class MemoryUsage:
    @staticmethod
    def get_memory_report() -> dict[str, float]:
        report = {}

        with open("/proc/meminfo", "r", encoding="utf-8") as proc_meminfo:
            for line in proc_meminfo:
                if line.startswith(
                    ("MemTotal", "MemAvailable", "SwapTotal", "SwapFree")
                ):
                    split = line.split(":")

                    key = split[0].lower()
                    value = split[1].strip()[:-3]

                    report[key] = float(value)

        return report
