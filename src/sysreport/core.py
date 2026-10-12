#!/usr/bin/env python

from sysreport.utils.disk import DiskUsage
from sysreport.utils.system import SystemSpecs

"""
!!! Currently using this file for quick testing
"""

system = SystemSpecs()
disk = DiskUsage("/")

print("System \n")
print(system.get_distro_name())
print(system.get_distro_version())
print(system.get_system_arch())
print(system.get_kernel_version())
print(system.get_uptime_seconds())

print("--------------")

print("Disk \n")
print(disk.get_total_space_bytes())
print(disk.get_free_space_bytes())
print(disk.get_usable_space_bytes())
