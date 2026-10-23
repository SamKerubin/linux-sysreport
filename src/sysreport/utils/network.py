import os
import time


class NetworkStatus:
    @staticmethod
    def __get_network_type(dev, id) -> str:
        match id:
            case 1:
                with open(
                    f"/sys/class/net/{dev}/uevent", "r", encoding="utf-8"
                ) as uevent:
                    line = uevent.readline().strip()
                    if line == "DEVTYPE=vlan":
                        return "VLAN"

                    if line == "DEVTYPE=wlan":
                        return "Wi-Fi (Wireless)"

                if os.path.exists(f"/sys/class/net/{dev}/wireless"):
                    return "Wi-Fi (Wireless)"

                if os.path.exists(f"/sys/class/net/{dev}/bridge"):
                    return "Virtual bridge"

                if os.path.exists(f"/sys/class/net/{dev}/bonding"):
                    return "Network bond"

                return "Physical ethernet"

            case 772:
                return "Loopback"

            case 65534:
                with open(
                    f"/sys/class/net/{dev}/uevent", "r", encoding="utf-8"
                ) as uevent:
                    line = uevent.readline().strip()
                    if line == "DEVTYPE=wireguard":
                        return "WireGuard VPN"

                if os.path.exists(f"/sys/class/net/{dev}/tun_flags"):
                    with open(
                        f"/sys/class/net/{dev}/tun_flags", "r", encoding="utf-8"
                    ) as tun_flags:
                        line = tun_flags.readline().strip()

                        if int(line) == 0x0001:
                            return "TUN tunnel"

                        if int(line) == 0x0002:
                            return "TAP tunnel"

                    return "TUN/TAP tunnel"

                return "Layer 3 IP tunnel"

            case 512:
                driver_path = os.readlink(f"/sys/class/net/{dev}/device/driver")
                driver = os.path.basename(driver_path)

                if driver == "qmi_wwan" or driver == "rmnet":
                    return "Cellular modem (QMI/RmNet)"

                if driver == "cdc_mbim":
                    return "Cellular modem (MBIM)"

                if driver == "cdc_ncm" or driver == "cdc_ether":
                    return "Cellular modem (USB Ethernet)"

                return "WAN Device"

            case _:
                return f"Unknown device type '{id}'"

    @staticmethod
    def __read_network_activity() -> dict[str, tuple]:
        activity = {}
        with open("/proc/net/dev", "r", encoding="utf-8") as net_dev:
            net_dev.readline()
            net_dev.readline()

            for line in net_dev:
                split = line.split()

                dev_name = split[0][:-1]
                activity[dev_name] = (int(split[1]), int(split[9]))

        return activity

    @staticmethod
    def get_network_report() -> dict:
        report = {}

        activity1 = NetworkStatus.__read_network_activity()
        time.sleep(0.5)
        activity2 = NetworkStatus.__read_network_activity()

        for dev in activity1:
            report[dev] = {}
            if dev not in activity2:
                continue

            b_rec1, b_trans1 = activity1[dev]
            b_rec2, b_trans2 = activity2[dev]

            b_rec_delta = b_rec2 - b_rec1
            b_trans_delta = b_trans2 - b_trans1

            report[dev]["recieved"] = b_rec_delta
            report[dev]["transmitted"] = b_trans_delta

        NET_DEV_BASE_PATH = "/sys/class/net/"
        if not os.path.exists(NET_DEV_BASE_PATH):
            return {"network": "Network is unreachable"}

        net_devs = activity2.keys()
        for dev in net_devs:
            operstate_path = os.path.join(NET_DEV_BASE_PATH, dev, "operstate")
            with open(operstate_path, "r", encoding="utf-8") as op:
                report[dev]["state"] = op.readline().strip()

            dev_type_path = os.path.join(NET_DEV_BASE_PATH, dev, "type")
            with open(dev_type_path, "r", encoding="utf-8") as t:
                net_type_int = int(t.readline().strip())
                report[dev]["type"] = NetworkStatus.__get_network_type(
                    dev, net_type_int
                )

        return report
