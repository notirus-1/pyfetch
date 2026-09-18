#!/usr/bin/python3
import os, shlex, re, subprocess, shutil, platform
art = r"""
 ____        _____    _       _     
|  _ \ _   _|  ___|__| |_ ___| |__  
| |_) | | | | |_ / _ \ __/ __| '_ \ 
|  __/| |_| |  _|  __/ || (__| | | |
|_|    \__, |_|  \___|\__\___|_| |_|
       |___/                        
"""
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
        "totalRAM": RAM.get("MemTotal").strip(),
        "usedRAM": RAM.get("Active").strip(),
        "Distro": Distro.get("NAME"),
        "GPU": str([item for item in GPU[0] if any(GPU_MODEL in item for GPU_MODEL in GPU_MODEL)]).strip("[]").strip("'"),
        "Disk": f'{round(shutil.disk_usage("/").free / (1024**3), 2)} GB / {round(shutil.disk_usage("/").total / (1024**3), 2)} GB',
    }
    result = specs.get(name)
    return result
print(os.getlogin() +'@' + platform.node())
print(art)
print(f"Distro: {get_specs("Distro").strip()}")
print(f"Kernel: {get_specs("Linux")}")
print(f'CPU: {get_specs("CPU").strip()}')
print(f'RAM: {round(int(get_specs("usedRAM")) * 1024 / (1024**3), 1)} GB / {round(int(get_specs("totalRAM")) * 1024 / (1024**3), 1)} GB')
print(f'GPU: {get_specs("GPU")}')
print(f'Disk: {get_specs("Disk")}')
print(f'Storage: {get_specs("Disk")}')
print(f'Shell: {os.getenv('SHELL').strip('bin/')}')
print(f'DE: {os.getenv('DESKTOP_SESSION')}')
