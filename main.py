import os
import time

import psutil


def get_cpu_usage():
    cpu_usage_percent = psutil.cpu_percent()
    cpu_usage_per_core = psutil.cpu_percent(percpu=True)
    return cpu_usage_percent, cpu_usage_per_core


def get_memory_usage():
    memory_usage = psutil.virtual_memory()
    swap_usage = psutil.swap_memory()
    gb = 1024**3
    used_ram = memory_usage.used / gb
    total_ram = memory_usage.total / gb
    used_swap = swap_usage.used / gb
    total_swap = swap_usage.total / gb
    return used_ram, total_ram, used_swap, total_swap


def get_disk_usage():
    disk_usage = psutil.disk_usage("/")
    gb = 1024**3
    used_disk_space = disk_usage.used / gb
    total_disk_space = disk_usage.total / gb
    return used_disk_space, total_disk_space


def get_cpu_intensive_processes(num_processes=30):
    ps_output = os.popen("ps x -o pid,pcpu,comm").readlines()[1:]
    processes = [
        (int(parts[0]), float(parts[1]), parts[2])
        for parts in [line.strip().split() for line in ps_output]
        if parts
    ]
    processes.sort(key=lambda x: x[1], reverse=True)

    num_per_col = (num_processes + 1) // 2
    result = [
        f"{i + 1:<4} PID:{p1[0]:<6} {p1[2]:<15} {p1[1]:<6.1f}%   "
        f"{num_per_col + i + 1:<4} PID:{p2[0]:<6} {p2[2]:<15} {p2[1]:<6.1f}%"
        for i, (p1, p2) in enumerate(
            zip(processes[:num_per_col], processes[num_per_col:])
        )
    ]
    return result


def run_monitor():
    while True:
        total_cpu_usage, cpu_usage_per_core = get_cpu_usage()
        used_ram, total_ram, used_swap, total_swap = get_memory_usage()
        used_disk_space, total_disk_space = get_disk_usage()

        cpu_data = [("Total CPU usage", f"{total_cpu_usage:.1f}%")] + [
            (f"CPU core {i}", f"{cpu_usage:.1f}%")
            for i, cpu_usage in enumerate(cpu_usage_per_core)
        ]

        extra_data = [
            ("RAM", f"{used_ram:.2f} GB / {total_ram:.2f} GB"),
            ("Swap", f"{used_swap:.2f} GB / {total_swap:.2f} GB"),
            ("Disk space", f"{used_disk_space:.2f} GB / {total_disk_space:.2f} GB"),
        ]

        max_rows = max(len(cpu_data), len(extra_data))
        table_str = "\n".join(
            [
                f"{cpu_data[i][0]:<20}{cpu_data[i][1]:<20}"
                f"{extra_data[i][0]:<20}{extra_data[i][1]:<20}"
                if i < len(cpu_data) and i < len(extra_data)
                else ""
                for i in range(max_rows)
            ]
        )

        os.system("clear")
        print(
            """System Resource Monitor

A lightweight CLI utility that displays system resources including
CPU usage, memory usage, disk space, and the top running processes.
        """
        )
        print(
            "".join(
                [
                    table_str,
                    "\n\nTop processes:\n\n",
                    "\n".join(get_cpu_intensive_processes()),
                ]
            )
        )

        time.sleep(3)


run_monitor()
