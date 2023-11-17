#!/usr/bin/python3
import sys
import os
import psutil
import pandas as pd


def get_directory_sizes(path):
    directories = []
    sizes = []

    # Iterate through directory entries
    for entry in os.scandir(path):
        try:
            if entry.is_dir(follow_symlinks=False):
                # Calculate directory size recursively
                total_size = get_size(entry.path)
                total_size = total_size / (1024 * 1024)  # Convert to MB
                directories.append(entry.path)
                sizes.append(total_size)
        except Exception as e:
            print(f"Exception for {entry.path}: {e}")

    return directories, sizes


def get_size(path):
    total_size = 0
    # Calculate size of files and directories within a directory
    for entry in os.scandir(path):
        try:
            if entry.is_dir(follow_symlinks=False):
                total_size += get_size(entry.path)  # Recursively calculate directory size
            else:
                total_size += entry.stat(follow_symlinks=False).st_size  # Get file size
        except Exception as e:
            print(f"Exception for {entry.path}: {e}")
            total_size += 0  # If error occurs, treat size as 0
    return total_size


if __name__ == '__main__':
    path = '/home'
    print("Total arguments passed: ", len(sys.argv))

    directory = sys.argv[1] if len(sys.argv) >= 2 else path

    # Retrieve directory sizes
    directories, sizes = get_directory_sizes(directory)

    # Get RAM information
    ram = psutil.virtual_memory()
    ram_total = ram.total / (1024 * 1024)  # RAM total in MB
    ram_used = ram.used / (1024 * 1024)  # RAM used in MB
    ram_available = ram.available / (1024 * 1024)  # RAM available in MB

    # Get disk usage information
    disk = psutil.disk_usage('/')
    disk_total = disk.total / (1024 * 1024)  # Disk total in MB
    disk_used = disk.used / (1024 * 1024)  # Disk used in MB
    disk_available = disk.free / (1024 * 1024)  # Disk available in MB

    # Get CPU usage information
    cpu_usage = psutil.cpu_percent(interval=1)  # CPU usage in percentage

    # Create a dictionary for DataFrame
    usage_dict = {
        'directory': directories,
        'usage (MB)': sizes,
        'RAM Total (MB)': [ram_total] * len(directories),
        'RAM Used (MB)': [ram_used] * len(directories),
        'RAM Available (MB)': [ram_available] * len(directories),
        'Disk Total (MB)': [disk_total] * len(directories),
        'Disk Used (MB)': [disk_used] * len(directories),
        'Disk Available (MB)': [disk_available] * len(directories),
        'CPU Usage (%)': [cpu_usage] * len(directories)
    }
    df = pd.DataFrame(usage_dict)

    # Print RAM, disk, and CPU information
    print("RAM Total (MB):", ram_total)
    print("RAM Used (MB):", ram_used)
    print("RAM Available (MB):", ram_available)
    print("Disk Total (MB):", disk_total)
    print("Disk Used (MB):", disk_used)
    print("Disk Available (MB):", disk_available)
    print("CPU Usage (%):", cpu_usage)

    # Print DataFrame containing directory usage information
    print(df)

    # Save DataFrame to CSV file
    df.to_csv('disk_usage.csv', index=False)
