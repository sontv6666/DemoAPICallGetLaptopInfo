from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
import psutil
import GPUtil
import platform

# Define API token
API_TOKEN = "my_secure_token_123"

# Create FastAPI app
app = FastAPI()

# Enable CORS (Allow frontend to access API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change if needed)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Define API Key security
api_key_header = APIKeyHeader(name="API_KEY", auto_error=True)

def validate_api_key(api_key: str = Security(api_key_header)):
    """Validate API Key"""
    if api_key != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid API Key")

# System Info Functions
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
    swap = psutil.swap_memory()

    return {
        "physical_memory": {
            "total": f"{ram.total / (1024 ** 3):.2f} GB",
            "available": f"{ram.available / (1024 ** 3):.2f} GB",
            "used": f"{ram.used / (1024 ** 3):.2f} GB",
            "free": f"{ram.free / (1024 ** 3):.2f} GB",
            "percent_used": f"{ram.percent} %",
            "active": f"{ram.active / (1024 ** 3):.2f} GB",
            "inactive": f"{ram.inactive / (1024 ** 3):.2f} GB",
            "buffers": f"{ram.buffers / (1024 ** 3):.2f} GB",
            "cached": f"{ram.cached / (1024 ** 3):.2f} GB",
            "shared": f"{ram.shared / (1024 ** 3):.2f} GB",
        },
        "swap_memory": {
            "total": f"{swap.total / (1024 ** 3):.2f} GB",
            "used": f"{swap.used / (1024 ** 3):.2f} GB",
            "free": f"{swap.free / (1024 ** 3):.2f} GB",
            "percent_used": f"{swap.percent} %",
            "swapped_in": f"{swap.sin / (1024 ** 3):.2f} GB",
            "swapped_out": f"{swap.sout / (1024 ** 3):.2f} GB"
        }
    }


# Protected Endpoints
@app.get("/")
def home():
    return {"message": "Welcome to System Info API!"}

@app.get("/cpu", dependencies=[Depends(validate_api_key)])
def cpu_info():
    return get_cpu_info()

@app.get("/gpu", dependencies=[Depends(validate_api_key)])
def gpu_info():
    return get_gpu_info()

@app.get("/ram", dependencies=[Depends(validate_api_key)])
def ram_info():
    return get_ram_info()
