import os


class PowerSupplyStatus:
    @staticmethod
    def __parse_power_uevent(path) -> dict[str, str | int]:
        properties = {}

        with open(path, "r", encoding="utf-8") as uevent:
            uevent.readline()
            for line in uevent:
                key, value = line.split("=")

                key = key.lower()
                value = value.strip()

                properties[key] = value if not value.isdigit() else int(value)

        return properties

    @staticmethod
    def get_power_supply_report() -> list[dict[str, str | int]]:
        report = []

        BASE_PATH = "/sys/class/power_supply/"

        devices = [dir for dir in os.listdir(BASE_PATH)]
        for dev in devices:
            path = os.path.join(BASE_PATH, dev, "uevent")
            dev_report = PowerSupplyStatus.__parse_power_uevent(path)
            report.append(dev_report)

        return report
