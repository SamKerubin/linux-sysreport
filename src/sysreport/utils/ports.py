import os


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
    def get_net_port_status(options) -> dict:
        tcp_opt = options.get("tcp", {})
        udp_opt = options.get("udp", {})

        report = {"tcp": {}, "udp": {}}
        inode_hash = {"tcp": {}, "udp": {}}

        if tcp_opt.get("enable"):
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

                    if status != "LISTEN" and tcp_opt.get("listen_only"):
                        continue

                    local_address, port, sl, inode = PortStatus.__parse_address(parts)

                    report["tcp"][sl] = {
                        "local_address": local_address,
                        "port": port,
                        "status": status,
                    }

                    inode_hash["tcp"][inode] = sl

        if udp_opt.get("enable"):
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

                    if status != "CONN" and udp_opt.get("conn_only"):
                        continue

                    local_address, port, sl, inode = PortStatus.__parse_address(parts)

                    report["udp"][sl] = {
                        "local_address": local_address,
                        "port": port,
                        "status": status,
                    }

                    inode_hash["udp"][inode] = sl

        proc_pid = [pid for pid in os.listdir("/proc/") if pid.isdigit()]
        for pid in proc_pid:
            path = os.path.join("/proc/", pid, "fd")

            fd_list = os.listdir(path)
            for fd in fd_list:
                try:
                    full_path = os.path.join(path, fd)
                    link = os.readlink(full_path)
                except OSError:
                    continue

                if not link.startswith("socket:["):
                    continue

                parts = link.split(":")
                inode_part = parts[1][1:-1]

                port_type = None
                if inode_part in inode_hash["tcp"]:
                    port_type = "tcp"
                if inode_part in inode_hash["udp"]:
                    port_type = "udp"

                if not port_type:
                    continue

                sl = inode_hash[port_type][inode_part]

                comm_path = os.path.join("/proc/", pid, "comm")
                with open(comm_path, "r", encoding="utf-8") as comm:
                    command = comm.readline().strip()

                report[port_type][sl]["process"] = {
                    "pid": pid,
                    "command": command,
                    "fd": fd,
                }

        return report
