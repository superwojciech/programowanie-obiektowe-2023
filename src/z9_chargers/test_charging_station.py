import unittest
from charging_station import ChargingService, Charger, ChargingStatus, ChargerStatus

class TestChargingService(unittest.TestCase):
    def setUp(self):
        self.charging_station = ChargingService()
        self.charger1 = Charger(max_current_kw=50)
        self.charger2 = Charger(max_current_kw=100)
        self.charging_station.attach_charger(self.charger1)
        self.charging_station.attach_charger(self.charger2)

    def test_start_charging_success(self):
        session = self.charging_station.start_charging(client_id=1, vin="VW12345", kwh=20, desired_current_kw=50, charger_position=0)
        self.assertIsNotNone(session)
        self.assertEqual(self.charger1.status, ChargerStatus.CHARGING)
        self.assertEqual(self.charger1.attached_car_vin, "VW12345")
        self.assertEqual(session.status, ChargingStatus.OPEN)

    def test_start_charging_failure(self):
        session = self.charging_station.start_charging(client_id=1, vin="VW12345", kwh=20, desired_current_kw=80, charger_position=0)
        self.assertIsNone(session)
        self.assertEqual(self.charger1.status, ChargerStatus.FREE)
        self.assertIsNone(self.charger1.attached_car_vin)

    def test_stop_charging(self):
        self.charging_station.start_charging(client_id=1, vin="VW12345", kwh=20, desired_current_kw=50, charger_position=0)
        self.charging_station.stop_charging(client_id=1, vin="VW12345")
        self.assertEqual(self.charger1.status, ChargerStatus.FREE)
        self.assertIsNone(self.charger1.attached_car_vin)

    def test_get_charging_time(self):
        session = self.charging_station.start_charging(client_id=1, vin="VW12345", kwh=20, desired_current_kw=50, charger_position=0)
        session.end_time = session.start_time + 10 
        charging_time = self.charging_station.get_charging_time(session)
        self.assertEqual(charging_time, 10 * self.charging_station.time_modifier)

if __name__ == '__main__':
    unittest.main()
