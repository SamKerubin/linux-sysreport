import os


class DiskUsage:
    def __init__(self, path) -> None:
        self.disk_metadata = os.statvfs(path)

    def get_total_space_bytes(self) -> int:
        return self.disk_metadata.f_blocks * self.disk_metadata.f_frsize

    def get_free_space_bytes(self) -> int:
        return self.disk_metadata.f_bfree * self.disk_metadata.f_frsize

    def get_usable_space_bytes(self) -> int:
        return self.disk_metadata.f_bavail * self.disk_metadata.f_frsize
