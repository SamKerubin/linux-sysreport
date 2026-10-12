#!/usr/bin/env python

from sysreport.utils.cpu import CPUInfo
from sysreport.utils.disk import DiskUsage
from sysreport.utils.memory import MemoryUsage
from sysreport.utils.system import SystemSpecs

"""
!!! Currently using this file for quick testing
"""

print("System \n")
print(SystemSpecs.get_system_specs_report())

print("--------------")

print("Disk \n")
print(DiskUsage.get_disk_usage_report("/"))

print("--------------")

print("CPU \n")
print(CPUInfo.get_cpu_info_report())

print("--------------")

print("Memory \n")
print(MemoryUsage.get_memory_report())
