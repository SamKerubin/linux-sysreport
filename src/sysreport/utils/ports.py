class PortStatus:
    @staticmethod
    def __parse_address(parts) -> tuple:
        sl = parts[0][:-1]

        address_hex = parts[1]
        local_address_hex, port_hex = address_hex.split(":")

        local_address_int = int(local_address_hex, 16)
        local_address = (
            f"{local_address_int & 0xFF}.{(local_address_int >> 8) & 0xFF}."
            f"{(local_address_int >> 16) & 0xFF}.{(local_address_int >> 24) & 0xFF}"
        )
        port = str(int(port_hex, 16))

        inode = parts[9]

        return local_address, port, sl, inode

    @staticmethod
    def get_net_port_status(add_tcp, add_udp) -> dict:
        report = {}

        if add_tcp:
            report["tcp"] = {}
            with open("/proc/net/tcp", "r", encoding="utf-8") as tcp:
                tcp.readline()

                for socket in tcp:
                    parts = socket.split()

                    status_hex = parts[3]
                    status = "UNKNOWN"
                    if status_hex == "0A":
                        status = "LISTEN"
                    if status_hex == "01":
                        status = "ESTAB"
                    if status_hex == "06":
                        status = "WAIT"
                    if status_hex == "07":
                        status = "CLOSE"

                    local_address, port, sl, inode = PortStatus.__parse_address(parts)

                    report["tcp"][sl] = {
                        "local_address": local_address,
                        "port": port,
                        "status": status,
                    }

        if add_udp:
            report["udp"] = {}
            with open("/proc/net/udp", "r", encoding="utf-8") as udp:
                udp.readline()

                for socket in udp:
                    parts = socket.split()

                    status_hex = parts[3]
                    status = "UNKNOWN"
                    if status_hex == "01":
                        status = "CONN"
                    if status_hex == "07":
                        status = "UNCONN"

                    local_address, port, sl, inode = PortStatus.__parse_address(parts)

                    report["udp"][sl] = {
                        "local_address": local_address,
                        "port": port,
                        "status": status,
                    }

        return report
