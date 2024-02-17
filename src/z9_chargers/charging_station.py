from enum import Enum
import time

class ChargingStatus(Enum):
    OPEN = "OPEN"
    ERROR = "ERROR"
    FINISHED = "FINISHED"

class ChargerStatus(Enum):
    FREE = "FREE"
    CHARGING = "CHARGING"
    ERROR = "ERROR"

class ClientAccount:
    def __init__(self, client_id, name, funds):
        self.id = client_id
        self.name = name
        self.funds = funds

class Car:
    def __init__(self, vin, total_charged_kwh, max_current_kw):
        self.vin = vin
        self.total_charged_kwh = total_charged_kwh
        self.max_current_kw = max_current_kw

class ChargingSession:
    def __init__(self, csid, status, current_kw, total_kwh):
        self.csid = csid
        self.status = status
        self.current_kw = current_kw
        self.total_kwh = total_kwh
        self.start_time = None
        self.end_time = None

class Charger:
    def __init__(self, max_current_kw):
        self.max_current_kw = max_current_kw
        self.total_charged_kw = 0
        self.attached_car_vin = None
        self.status = ChargerStatus.FREE

class ChargingService:
    def __init__(self, time_modifier=1.0):
        self.chargers = []
        self.time_modifier = time_modifier

    def start_charging(self, client_id, vin, kwh, desired_current_kw, charger_position):
        charger = self.chargers[charger_position]
        if charger.status == ChargerStatus.FREE and charger.max_current_kw >= desired_current_kw:
            charger.status = ChargerStatus.CHARGING
            charger.attached_car_vin = vin
            session = ChargingSession(csid=len(self.chargers), status=ChargingStatus.OPEN, current_kw=desired_current_kw, total_kwh=kwh)
            session.start_time = time.time()
            return session
        else:
            return None

    def stop_charging(self, client_id, vin):
        for charger in self.chargers:
            if charger.attached_car_vin == vin:
                charger.status = ChargerStatus.FREE
                charger.attached_car_vin = None
                break

    def attach_charger(self, charger):
        self.chargers.append(charger)

    def disable_charger(self, charger_position):
        self.chargers[charger_position].status = ChargerStatus.ERROR

    def enable_charger(self, charger_position):
        self.chargers[charger_position].status = ChargerStatus.FREE

    def remove_charger(self, charger):
        self.chargers.remove(charger)

    def get_charging_time(self, session):
        if session.start_time is not None and session.end_time is not None:
            return (session.end_time - session.start_time) * self.time_modifier
        else:
            return None
