# importing necessary modules
import os
import platform
import shutil
import humanize 
import subprocess
import re
import shlex
# plan:
# function has a category, that gets specs in order. Linux gets kernel version and distro name
# cpu gets vendor name and core/thread count
# gpu gets vendor name and model
# ram gets memory
# disk gets size and type
# write the function to get os details
CPU = {}
RAM = {}
GPU = []
Distro = platform.freedesktop_os_release()
GPU_MODEL = ["GTX", "RTX", "UHD", "AMD", "RADEON", "Radeon", "VEGA", "Vega"]
GPUfind = subprocess.run(['bash', '-c', 'lspci -mm | grep VGA'], capture_output=True, text=True)
gpuclean = GPUfind.stdout.strip('')
split = shlex.split(gpuclean)
GPU.append(split)
with open("/proc/cpuinfo", "r") as file:
    for line in file:
        line = line.strip()
        if ":" in line:
            key, value = line.split(":", 1)
            CPU[key] = value
with open("/proc/meminfo", "r") as file:
    for line in file:
        line = line.strip("kB\n")
        if ":" in line:
            key, value = line.split(":", 1)
            RAM[key] = value
def get_specs(name):
    specs = {
        "Linux": platform.release(),
        "CPU": CPU.get("""model name\t"""),
        "RAM": RAM.get("MemTotal").strip(),
        "Distro": Distro.get("NAME"),
        "GPU": [item for item in GPU[0] if any(GPU_MODEL in item for GPU_MODEL in GPU_MODEL)],
    }
    result = specs.get(name)
    return result
# find gpu
print(os.getlogin() +'@' + platform.node())
print(f"Distro: {get_specs("Distro").strip()}")
print(f"Kernel: {get_specs("Linux")}")
print(f'CPU: {get_specs("CPU").strip()}')
print(f'RAM: {humanize.naturalsize(int(get_specs("RAM")) * 1024, binary=True)}')
print(f'GPU: {get_specs("GPU")}')
