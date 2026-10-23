import os
import time


class NetworkStatus:
    @staticmethod
    def __get_network_type(id) -> str:
        match id:
            case 1:
                return "Ethernet"

            case 772:
                return "Loopback"

            case _:
                return "Unknown"

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
                report[dev]["type"] = NetworkStatus.__get_network_type(net_type_int)

        return report
