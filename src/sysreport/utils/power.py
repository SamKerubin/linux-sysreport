import os


class PowerSupplyStatus:
    @staticmethod
    def __parse_power_uevent(path) -> dict[str, str | int | None]:
        properties: dict[str, str | int | None] = {
            "power_supply_name": None,
            "power_supply_type": None,
            "power_supply_status": None,
            "power_supply_charge_type": None,
            "power_supply_health": None,
            "power_supply_present": None,
            "power_supply_online": None,
            "power_supply_authentic": None,
            "power_supply_technology": None,
            "power_supply_cycle_count": None,
            "power_supply_scope": None,
            "power_supply_capacity": None,
            "power_supply_capacity_alert_min": None,
            "power_supply_capacity_alert_max": None,
            "power_supply_capacity_level": None,
            "power_supply_voltage_max_design": None,
            "power_supply_voltage_min_design": None,
            "power_supply_voltage_max": None,
            "power_supply_voltage_min": None,
            "power_supply_voltage_now": None,
            "power_supply_voltage_avg": None,
            "power_supply_voltage_ocv": None,
            "power_supply_voltage_boot": None,
            "power_supply_current_max": None,
            "power_supply_current_now": None,
            "power_supply_current_avg": None,
            "power_supply_current_boot": None,
            "power_supply_power_now": None,
            "power_supply_power_avg": None,
            "power_supply_charge_full_design": None,
            "power_supply_charge_full": None,
            "power_supply_charge_now": None,
            "power_supply_charge_avg": None,
            "power_supply_charge_counter": None,
            "power_supply_energy_full_design": None,
            "power_supply_energy_full": None,
            "power_supply_energy_now": None,
            "power_supply_energy_avg": None,
            "power_supply_temp": None,
            "power_supply_temp_max": None,
            "power_supply_temp_min": None,
            "power_supply_temp_alert_min": None,
            "power_supply_temp_alert_max": None,
            "power_supply_temp_ambient": None,
            "power_supply_time_to_empty_now": None,
            "power_supply_time_to_empty_avg": None,
            "power_supply_time_to_full_now": None,
            "power_supply_time_to_full_avg": None,
            "power_supply_model_name": None,
            "power_supply_manufacturer": None,
            "power_supply_serial_number": None,
            "power_supply_usb_type": None,
            "power_supply_typec_mode": None,
            "power_supply_typec_power_role": None,
            "power_supply_input_current_limit": None,
            "power_supply_input_voltage_limit": None,
            "power_supply_input_power_limit": None,
        }

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
