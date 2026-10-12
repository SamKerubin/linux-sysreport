import os


class DiskUsage:
    def __init__(self, path) -> None:
        self.disk_metadata = os.statvfs(path)

        self.mount_device = ""
        self.disk_fs_type = ""

        self.__parse_device_properties(path)

    def __parse_device_properties(self, path) -> None:
        with open("/proc/mounts", "r", encoding="utf-8") as proc_mounts:
            for line in proc_mounts:
                split = line.split()
                if split[1] == path:
                    self.mount_device = split[0]
                    self.disk_fs_type = split[2]

    def get_total_space_bytes(self) -> int:
        return self.disk_metadata.f_blocks * self.disk_metadata.f_frsize

    def get_free_space_bytes(self) -> int:
        return self.disk_metadata.f_bfree * self.disk_metadata.f_frsize

    def get_usable_space_bytes(self) -> int:
        return self.disk_metadata.f_bavail * self.disk_metadata.f_frsize

    def get_mount_device(self) -> str:
        return self.mount_device

    def get_filesystem_type(self) -> str:
        return self.disk_fs_type
