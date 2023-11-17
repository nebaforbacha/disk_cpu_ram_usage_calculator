import sys
import os
import psutil
import pandas as pd


# Function to retrieve directory sizes
def get_directory_sizes(path):
    directories = []
    sizes = []

    for entry in os.scandir(path):
        try:
            if entry.is_dir(follow_symlinks=False):
                total_size = get_size(entry.path)
                total_size = total_size / (1024 * 1024)
                directories.append(entry.path)
                sizes.append(total_size)
        except Exception as e:
            print(f"Exception for {entry.path}: {e}")

    return directories, sizes


# Function to calculate size of files and directories
def get_size(path):
    total_size = 0
    for entry in os.scandir(path):
        try:
            if entry.is_dir(follow_symlinks=False):
                total_size += get_size(entry.path)
            else:
                total_size += entry.stat(follow_symlinks=False).st_size
        except Exception as e:
            print(f"Exception for {entry.path}: {e}")
            total_size += 0
    return total_size


if __name__ == '__main__':
    path = 'C:\\Users\\user\\'  # Change this to the desired directory path
    print("Total arguments passed: ", len(sys.argv))

    directory = sys.argv[1] if len(sys.argv) >= 2 else path

    directories, sizes = get_directory_sizes(directory)

    ram = psutil.virtual_memory()
    ram_total = ram.total / (1024 * 1024)  # RAM total in MB
    ram_used = ram.used / (1024 * 1024)  # RAM used in MB
    ram_available = ram.available / (1024 * 1024)  # RAM available in MB

    disk = psutil.disk_usage(directory)
    disk_total = disk.total / (1024 * 1024)  # Disk total in MB
    disk_used = disk.used / (1024 * 1024)  # Disk used in MB
    disk_available = disk.free / (1024 * 1024)  # Disk available in MB

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

    print(df)

    df.to_csv('disk_usage.csv', index=False)
