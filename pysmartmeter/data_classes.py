import dataclasses
import json
from typing import Any, Optional

from bx_py_utils.anonymize import anonymize


@dataclasses.dataclass
class MqttSettings:
    host: str
    port: int
    user_name: Optional[str]
    password: Optional[str]

    def as_json(self):
        data = dataclasses.asdict(self)
        data_str = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)
        return data_str

    @classmethod
    def from_json(cls, data_str):
        data = json.loads(data_str)
        return cls(**data)

    def anonymized(self):
        data = dataclasses.asdict(self)
        if self.password:
            data['password'] = anonymize(self.password)
        return data


@dataclasses.dataclass
class ObisValue:
    """
    A "raw" Obis value
    """

    key: str  # origin name e.g.: '1-0:1.8.0*255'
    key_slug: str
    name: str  # Human readable name, e.g.: 'Zählerstand (Tariflos)'
    raw_value: str  # e.g.: '0010002*kWh'
    value: Any  # e.g.: 10002.0
    raw_unit: Optional[str] = None  # e.g.: 'kWh'
    unit: Optional[str] = None  # e.g.: 'kWh'

    def copy(self):
        data = dataclasses.asdict(self)
        return ObisValue(**data)


@dataclasses.dataclass
class HomeassistantValue:
    """
    Obis value prepared for Homeassistant submission
    """

    unique_id: str
    value_key: str
    obis_value: ObisValue

    @property
    def key(self):
        return self.obis_value.key
