import unittest
from unittest.mock import MagicMock, patch
from us2000c_prometheus_exporter import *

class TestUS2000CPrometheusExporter(unittest.TestCase):

    def setUp(self):
        self.ser = MagicMock()

    def test_exec_pwr(self):
        self.ser.in_waiting = 0
        self.ser.read.return_value = b''
        self.ser.write.return_value = None
        resp = exec_pwr(self.ser)
        self.assertEqual(resp, "")

    def test_exec_bat(self):
        self.ser.in_waiting = 0
        self.ser.read.return_value = b''
        self.ser.write.return_value = None
        resp = exec_bat(self.ser, "addr")
        self.assertEqual(resp, "")

    def test_parse_command_pwr(self):
        raw_txt = "pwr\n@\nPower\n$$\npylon>"
        pwr_dicts = parse_command_pwr(raw_txt)
        self.assertEqual(pwr_dicts, [])

    def test_parse_command_bat(self):
        raw_txt = "bat addr\n@\nBattery\n$$\npylon>"
        cell_dicts = parse_command_bat(raw_txt)
        self.assertEqual(cell_dicts, [])

    def test_append_cell_voltage(self):
        pwr_dicts = [{'Power': '1'}]
        self.ser.in_waiting = 0
        self.ser.read.return_value = b''
        self.ser.write.return_value = None
        exec_bat.return_value = "bat 1\n@\nBattery\n$$\npylon>"
        parse_command_bat.return_value = []
        append_cell_voltage(self.ser, pwr_dicts)
        self.assertEqual(pwr_dicts, [{'Power': '1', 'Cells': []}])

    def test_update_metrics(self):
        self.ser.in_waiting = 0
        self.ser.read.return_value = b''
        self.ser.write.return_value = None
        exec_pwr.return_value = "pwr\n@\nPower\n$$\npylon>"
        parse_command_pwr.return_value = []
        append_cell_voltage.return_value = None
        update_metrics(self.ser)
        self.assertEqual(BATTERY_VOLTAGE.labels.call_count, 0)
        self.assertEqual(BATTERY_CURRENT.labels.call_count, 0)
        self.assertEqual(BATTERY_HIGHEST_CELL_VOLTAGE.labels.call_count, 0)
        self.assertEqual(BATTERY_LOWEST_CELL_VOLTAGE.labels.call_count, 0)
        self.assertEqual(BATTERY_SOC.labels.call_count, 0)
        self.assertEqual(BATTERY_STATE.labels.call_count, 0)
        self.assertEqual(BATTERY_TEMP.labels.call_count, 0)
        self.assertEqual(BATTERY_CELL_VOLTAGE.labels.call_count, 0)
        self.assertEqual(BATTERY_CELL_CURRENT.labels.call_count, 0)
        self.assertEqual(BATTERY_CELL_TEMP.labels.call_count, 0)
        self.assertEqual(BATTERY_CELL_SOC.labels.call_count, 0)
        self.assertEqual(BATTERY_CELL_COULOMB.labels.call_count, 0)
        self.assertEqual(BATTERY_CELL_STATE.labels.call_count, 0)
        self.assertEqual(BATTERY_CELL_BAL.labels.call_count, 0)
        self.assertEqual(COLLECT_DATA_FAILS.inc.call_count, 0)

class TestPrometheusExporter(unittest.TestCase):
    def test_update_metrics(self):
        ser = MagicMock()
        ser.in_waiting = 0
        ser.read.return_value = b''
        ser.write.return_value = None
        ser.decode.return_value = ''
        update_metrics(ser)

if __name__ == '__main__':
    unittest.main()
