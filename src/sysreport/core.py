#!/usr/bin/env python

from sysreport.utils.system import SystemSpecs

"""
!!! Currently using this file for quick testing
"""

system = SystemSpecs()

print("System \n")
print(system.get_distro_name())
print(system.get_distro_version())
print(system.get_system_arch())
print(system.get_kernel_version())
print(system.get_uptime_seconds())
