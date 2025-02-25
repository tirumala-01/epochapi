import datetime
import decimal
import re
from typing import Any, Dict, Union
from loguru import logger

pattern = r"^(?:[LS]-(0[0-9]{5}|[1-9][0-9]{5})|V-(0[0-9]{2}|[1-9][0-9]{2}))$"


def get_extracted_id(id: Union[str, int]) -> int:
    if isinstance(id, str):
        return int(id.split("-")[1])
    elif isinstance(id, int):
        return id


def validate_id(id: str):
    if not re.match(pattern, id):
        logger.error(f"Invalid Id {id}")
        raise ValueError("Invalid Id")


def convert_numbers_to_string(data: Any) -> Any:
    if isinstance(data, dict):
        return {key: convert_numbers_to_string(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_numbers_to_string(item) for item in data]
    elif isinstance(
        data, (int, float, decimal.Decimal, datetime.date, datetime.datetime)
    ):
        return str(data)
    else:
        return data


def validate_city_names(origin: str, destination: str) -> None:
    city_re = "^(?=[a-zA-Z])[a-zA-Z ]+$"
    if not (re.match(city_re, origin) and re.match(city_re, destination)):
        logger.error(f"Invalid origin or destination {origin}-{destination}")
        raise ValueError("Invalid origin or destination")


def validate_vehicle_name(vehicle_id):
    vehicle_id_re = "^V-(0[0-9]{2}|[1-9][0-9]{2})$"
    if not re.match(vehicle_id_re, vehicle_id):
        logger.error(f"Invalid Vehicle Id {vehicle_id}")
        raise ValueError("Invalid Vehicle Id")


def extract_metric(
    data: Dict[str, Any], metric: str, metric_type: str
) -> Dict[str, Any]:
    valid_metrics = {
        "delivery_time": {
            "average": "avg_delivery_time",
            "maximum": "max_delivery_time",
            "minimum": "min_delivery_time",
            "total": "total_delivery_time",
        },
        "shipment_cost": {
            "average": "avg_shipment_cost",
            "maximum": "max_shipment_cost",
            "minimum": "min_shipment_cost",
            "total": "total_shipment_cost",
        },
    }
    metric_key = valid_metrics[metric_type][metric]
    filtered_entry = {
        key: value
        for key, value in data.items()
        if key in {"route_id", "origin", "destination", "total_trips", metric_key}
    }
    return filtered_entry


def extract_efficiency_type(data: Dict[str, Any], metric: str) -> Dict[str, Any]:
    valid_metrics = {
        "average": "avg_mileage_per_liter",
        "maximum": "max_mileage_per_liter",
        "minimum": "min_mileage_per_liter",
    }
    metric_key = valid_metrics[metric]
    filtered_entry = {
        key: value
        for key, value in data.items()
        if key
        in {"vehicle_id", "vehicle_full_id", "vehicle_name", "total_trips", metric_key}
    }
    return filtered_entry
