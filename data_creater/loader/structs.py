import datetime
from dataclasses import dataclass


@dataclass
class Data:
    Date: str
    Value1: float
    Value2: float
    idData: int
    idMeasure: int

    def get_date(self):
        date_format = "%a, %d %b %Y %H:%M:%S %Z"
        return datetime.datetime.strptime(self.Date, date_format)


@dataclass
class Point:
    ControlledParameter: str
    Description: str
    Direction: int
    Name: str
    idPoint: int
    idTrain: int


@dataclass
class Measure:
    AlarmLevel2: float
    AlarmLevel3: float
    AlarmLevel4: float
    AlarmType: int
    Description: str
    Name: str
    Param1: float
    Param2: float
    Param3: float
    RangeType: int
    Type: int
    Units: int
    idMeasure: int
    idPoint: int


@dataclass
class Train:
    idTrain: int
    Name: str
    Description: str
