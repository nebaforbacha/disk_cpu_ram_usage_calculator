# disk_cpu_ram_usage_calculator
#a program code to show the utility usage of ram, disk and cpu in a system
#to run for linux need to create a virtual env on the terminal for installation of psutil and pandas as seen below

python3 -m venv /path/to/your/venv
source /path/to/your/venv/bin/activate
pip install psutil

#for windows this part of the code needs to be changed 'C:\\Users\\YourUsername\\' to the name of your directory

#to run the code either of these can be used

python /path/to/your/script.py /home/
python3 /path/to/your/script.py /home/
sudo ./script.py /home/
python3 ./script.py
