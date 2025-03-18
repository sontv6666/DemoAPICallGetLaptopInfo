from fastapi import FastAPI
import psutil
import GPUtil
import platform
import os

app = FastAPI()


def get_cpu_info():
    return {
        "brand": platform.processor(),
        "cores": psutil.cpu_count(logical=False),
        "threads": psutil.cpu_count(logical=True),
        "frequency": psutil.cpu_freq()._asdict()
    }


def get_gpu_info():
    gpus = GPUtil.getGPUs()
    gpu_list = [{
        "name": gpu.name,
        "memory_total": f"{gpu.memoryTotal} MB",
        "memory_used": f"{gpu.memoryUsed} MB",
        "memory_free": f"{gpu.memoryFree} MB",
        "temperature": f"{gpu.temperature} °C",
        "load": f"{gpu.load * 100} %",
        "driver_version": gpu.driver
    } for gpu in gpus]

    return gpu_list if gpu_list else [{"message": "No GPU detected"}]


def get_ram_info():
    ram = psutil.virtual_memory()
    return {
        "total": f"{ram.total / (1024 ** 3):.2f} GB",
        "available": f"{ram.available / (1024 ** 3):.2f} GB",
        "used": f"{ram.used / (1024 ** 3):.2f} GB",
        "percent": f"{ram.percent} %"
    }


@app.get("/")
def home():
    return {"message": "Welcome to System Info API!"}


@app.get("/cpu")
def cpu_info():
    return get_cpu_info()


@app.get("/gpu")
def gpu_info():
    return get_gpu_info()


@app.get("/ram")
def ram_info():
    return get_ram_info()
