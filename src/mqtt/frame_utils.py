from datetime import datetime
from pydantic import BaseModel
from typing import Dict, Any, Union

# Define a sub-model so you can use dot notation: .value and .unit
class ReadingValue(BaseModel):
    value: Union[float, str]
    unit: str

class MQTTFormattedDataModel(BaseModel):
    timestamp: datetime
    label: str
    location: str
    imei: str
    noOfDevices: int
    deviceNo: str
    deviceTypeID: str
    multipleData: str
    flag: str
    # Use Dict[str, ReadingValue] to allow .value access
    readings: Dict[str, ReadingValue] 

def parse_timestamp(date_str: str, time_str: str) -> datetime:
    raw_dt = f"{date_str} {time_str}"
    # Added %y%m%d for your '210226' example
    formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%y%m%d %H%M%S"]
    
    for fmt in formats:
        try:
            return datetime.strptime(raw_dt, fmt)
        except ValueError:
            continue
    raise ValueError(f"Time data '{raw_dt}' does not match expected formats.")

def process_readings(device_type_id: str, raw_vals: list) -> Dict[str, Any]:
    device_map = {'1': 'electric_meter', '2': 'water_meter'}
    device_type_name = device_map.get(str(device_type_id))

    units_map = {
        "electric_meter": {
            "keys": ["Vr", "Vy", "Vb", "Cr", "Cy", "Cb", "TotalWatts", "PF", "Frequency"],
            "units": ["V", "V", "V", "A", "A", "A", "W", "PF", "Hz"]
        },
        "water_meter": {
            "keys": ["FlowRate", "TotalVolume", "LeakStatus"],
            "units": ["L/min", "m3", "bool"]
        }
    }

    if device_type_name in units_map:
        config = units_map[device_type_name]
        result = {}
        for i, key in enumerate(config["keys"]):
            if i < len(raw_vals):
                val = raw_vals[i].strip()
                try:
                    numeric_val = float(val)
                except ValueError:
                    numeric_val = val
                
                # Matches the ReadingValue model structure
                result[key] = {"value": numeric_val, "unit": config["units"][i]}
        return result
    return {}

def parse_mqtt_frame(frame: str) -> MQTTFormattedDataModel:
    clean_frame = frame.strip('$/#')
    parts = clean_frame.split('/')
    
    timestamp = parse_timestamp(parts[0], parts[1])
    raw_readings_list = parts[10].split(',')
    
    data_dict = {
        "timestamp": timestamp,
        "label": parts[2],
        "location": parts[3],
        "imei": parts[4],
        "noOfDevices": int(parts[5]),
        "deviceNo": parts[6],
        "deviceTypeID": parts[7],
        "multipleData": parts[8],
        "flag": parts[9],
        "readings": process_readings(parts[7], raw_readings_list)
    }
    
    return MQTTFormattedDataModel(**data_dict)

# --- Test ---
frame = "$/2026-03-08/11:50/MainPanel/Basement/GW001/1/D01/1/1/0/230,231,232,5,5,5,3450,0.95,50/#"
telemetry = parse_mqtt_frame(frame)

print(f"Validated Timestamp: {telemetry.timestamp}")
# Now this works perfectly!
print(f"Total Watts: {telemetry.readings['TotalWatts'].value} {telemetry.readings['TotalWatts'].unit}")