#!/usr/bin/env python

import argparse
import sys

from sysreport.collector.collector import ReportCollector
from sysreport.formatter.formatter import ReportFormatter


def main() -> None:
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "--json",
        action="store_true",
        help="Returns the report in a JSON string format.",
    )
    parser.add_argument(
        "--json-pretty",
        action="store_true",
        help="Returns the report as a prettyfied JSON string.",
    )
    parser.add_argument(
        "--collect",
        default="all",
        help="Select fields to create a report. Works as a list of fields. Default: 'all'.\n"
        "all: Every field.\n"
        "cpu: Generate CPU report.\n"
        "system: Generate system specs report.\n"
        "mem: Generate memory report.\n"
        "disk: Generate disk report.\n"
        "power: Generate power supply report.\n",
    )

    args = parser.parse_args()

    report = ReportCollector.collect(args)
    report_str = ReportFormatter.stringify_report(report, args)
    print(report_str)


if __name__ == "__main__":
    main()
