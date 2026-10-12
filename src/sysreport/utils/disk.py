import os


class DiskUsage:
    @staticmethod
    def __parse_device_properties(path) -> tuple[str, str]:
        mount_device, disk_fs_type = "", ""

        with open("/proc/mounts", "r", encoding="utf-8") as proc_mounts:
            for line in proc_mounts:
                split = line.split()
                if split[1] == path:
                    mount_device = split[0]
                    disk_fs_type = split[2]
                    break

        return mount_device, disk_fs_type

    @staticmethod
    def get_disk_usage_report(path) -> dict[str, str | int]:
        report = {}

        disk_metadata = os.statvfs(path)

        mount_device, disk_fs_type = DiskUsage.__parse_device_properties(path)

        report["total_space"] = disk_metadata.f_blocks * disk_metadata.f_frsize
        report["free_space"] = disk_metadata.f_bfree * disk_metadata.f_frsize
        report["usable_space"] = disk_metadata.f_bavail * disk_metadata.f_frsize
        report["mount_device"] = mount_device
        report["disk_fs_type"] = disk_fs_type

        return report
