from dataclasses import dataclass
import enum
from datetime import datetime


@dataclass
class MNKGameData:
    id: str
    status: enum
    created: str # dateTime in str for showing in json response
    