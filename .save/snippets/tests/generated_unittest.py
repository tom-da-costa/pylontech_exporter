import unittest
from unittest.mock import MagicMock, patch
from us2000c_prometheus_exporter import *
from mock_data import *
# import mock_data

class TestUS2000CPrometheusExporter(unittest.TestCase):

    def setUp(self):
        self.ser = MagicMock()

    # def test_exec_pwr(self):
    #     self.ser.in_waiting = 0
    #     self.ser.read.return_value = b''
    #     self.ser.write.return_value = None
    #     resp = exec_pwr(self.ser)
    #     self.assertEqual(resp, "")

    # def test_exec_bat(self):
    #     self.ser.in_waiting = 0
    #     self.ser.read.return_value = b''
    #     self.ser.write.return_value = None
    #     resp = exec_bat(self.ser, "addr")
    #     self.assertEqual(resp, "")

    def test_parse_command_pwr1(self):
        raw_txt = "pwr\n@\nPower\n$$\npylon>"
        result = parse_command_pwr(raw_txt)
        self.assertEqual(result, [])
    def test_parse_command_pwr2(self):
        result = parse_command_pwr(pwr_raw_txt_1)
        expected_result = [{'Power': '1', 'Volt': '51208', 'Curr': '0', 'Tempr': '28900', 'Tlow': '26200', 'Thigh': '26800', 'Vlow': '3404', 'Vhigh': '3419', 'Base.St': 'Idle', 'Volt.St': 'Normal', 'Curr.St': 'Normal', 'Temp.St': 'Normal', 'Coulomb': '100%', 'Time': '2024-07-08 00:23:30', 'B.V.St': 'Normal', 'B.T.St': 'Normal', 'MosTempr': '27500', 'M.T.St': 'Normal'}, {'Power': '2', 'Volt': '51192', 'Curr': '0', 'Tempr': '28400', 'Tlow': '26400', 'Thigh': '27000', 'Vlow': '3405', 'Vhigh': '3418', 'Base.St': 'Idle', 'Volt.St': 'Normal', 'Curr.St': 'Normal', 'Temp.St': 'Normal', 'Coulomb': '100%', 'Time': '2024-07-08 00:23:29', 'B.V.St': 'Normal', 'B.T.St': 'Normal', 'MosTempr': '27700', 'M.T.St': 'Normal'}, {'Power': '3', 'Volt': '51226', 'Curr': '0', 'Tempr': '30000', 'Tlow': '26000', 'Thigh': '27000', 'Vlow': '3400', 'Vhigh': '3418', 'Base.St': 'Idle', 'Volt.St': 'Normal', 'Curr.St': 'Normal', 'Temp.St': 'Normal', 'Coulomb': '100%', 'Time': '2024-07-08 00:23:29', 'B.V.St': 'Normal', 'B.T.St': 'Normal', 'MosTempr': '-', 'M.T.St': '-'}, {'Power': '4', 'Volt': '51201', 'Curr': '0', 'Tempr': '28200', 'Tlow': '25600', 'Thigh': '26000', 'Vlow': '3393', 'Vhigh': '3416', 'Base.St': 'Idle', 'Volt.St': 'Normal', 'Curr.St': 'Normal', 'Temp.St': 'Normal', 'Coulomb': '100%', 'Time': '2024-07-08 00:23:29', 'B.V.St': 'Normal', 'B.T.St': 'Normal', 'MosTempr': '27300', 'M.T.St': 'Normal'}, {'Power': '5', 'Volt': '51198', 'Curr': '0', 'Tempr': '28400', 'Tlow': '25500', 'Thigh': '25900', 'Vlow': '3407', 'Vhigh': '3415', 'Base.St': 'Idle', 'Volt.St': 'Normal', 'Curr.St': 'Normal', 'Temp.St': 'Normal', 'Coulomb': '100%', 'Time': '2024-07-08 00:23:30', 'B.V.St': 'Normal', 'B.T.St': 'Normal', 'MosTempr': '27000', 'M.T.St': 'Normal'}, {'Power': '6', 'Volt': '51194', 'Curr': '0', 'Tempr': '27800', 'Tlow': '24900', 'Thigh': '25000', 'Vlow': '3395', 'Vhigh': '3416', 'Base.St': 'Idle', 'Volt.St': 'Normal', 'Curr.St': 'Normal', 'Temp.St': 'Normal', 'Coulomb': '100%', 'Time': '2024-07-08 00:23:29', 'B.V.St': 'Normal', 'B.T.St': 'Normal', 'MosTempr': '26300', 'M.T.St': 'Normal'}]
        self.assertEqual(result, expected_result)
    def test_parse_command_pwr3(self):
        result = parse_command_pwr(pwr_raw_txt_2)
        expected_result = [{'Power': '1', 'Volt': '51208', 'Curr': '0', 'Tempr': '28900', 'Tlow': '26200', 'Thigh': '26800', 'Vlow': '3404', 'Vhigh': '3419', 'Base.St': 'Idle', 'Volt.St': 'Normal', 'Curr.St': 'Normal', 'Temp.St': 'Normal', 'Coulomb': '100%', 'Time': '2024-07-08 00:23:30', 'B.V.St': 'Normal', 'B.T.St': 'Normal', 'MosTempr': '27500', 'M.T.St': 'Normal'}]
        self.assertEqual(result, expected_result)
    def test_parse_command_pwr4(self):
        raw_txt = "pwr\n@\nUnknown command 'pwr' - try 'help'\n$$\npylon>"
        with self.assertRaises(AssertionError) :
            result = parse_command_pwr(raw_txt)


    def test_parse_command_bat1(self):
        raw_txt = "bat addr\n@\nBattery\n$$\npylon>"
        result = parse_command_bat(raw_txt)
        expected_result = []
        self.assertEqual(result, expected_result)
    def test_parse_command_bat2(self):
        result = parse_command_bat(bat_raw_txt_1)
        expected_result = [{'Battery': '0', 'Volt': '3416', 'Curr': '0', 'Tempr': '26500', 'Base.State': 'Idle', 'Volt.State': 'Normal', 'Curr.State': 'Normal', 'Temp.State': 'Normal', 'SOC': '100%', 'Coulomb': '49560 mAH', 'BAL': 'N'}, {'Battery': '1', 'Volt': '3403', 'Curr': '0', 'Tempr': '26500', 'Base.State': 'Idle', 'Volt.State': 'Normal', 'Curr.State': 'Normal', 'Temp.State': 'Normal', 'SOC': '100%', 'Coulomb': '49477 mAH', 'BAL': 'N'}, {'Battery': '2', 'Volt': '3414', 'Curr': '0', 'Tempr': '26500', 'Base.State': 'Idle', 'Volt.State': 'Normal', 'Curr.State': 'Normal', 'Temp.State': 'Normal', 'SOC': '100%', 'Coulomb': '49558 mAH', 'BAL': 'N'}, {'Battery': '3', 'Volt': '3413', 'Curr': '0', 'Tempr': '26500', 'Base.State': 'Idle', 'Volt.State': 'Normal', 'Curr.State': 'Normal', 'Temp.State': 'Normal', 'SOC': '100%', 'Coulomb': '49557 mAH', 'BAL': 'N'}, {'Battery': '4', 'Volt': '3413', 'Curr': '0', 'Tempr': '26500', 'Base.State': 'Idle', 'Volt.State': 'Normal', 'Curr.State': 'Normal', 'Temp.State': 'Normal', 'SOC': '100%', 'Coulomb': '49556 mAH', 'BAL': 'N'}, {'Battery': '5', 'Volt': '3405', 'Curr': '0', 'Tempr': '26800', 'Base.State': 'Idle', 'Volt.State': 'Normal', 'Curr.State': 'Normal', 'Temp.State': 'Normal', 'SOC': '100%', 'Coulomb': '49477 mAH', 'BAL': 'N'}, {'Battery': '6', 'Volt': '3412', 'Curr': '0', 'Tempr': '26800', 'Base.State': 'Idle', 'Volt.State': 'Normal', 'Curr.State': 'Normal', 'Temp.State': 'Normal', 'SOC': '100%', 'Coulomb': '49548 mAH', 'BAL': 'N'}, {'Battery': '7', 'Volt': '3418', 'Curr': '0', 'Tempr': '26800', 'Base.State': 'Idle', 'Volt.State': 'Normal', 'Curr.State': 'Normal', 'Temp.State': 'Normal', 'SOC': '100%', 'Coulomb': '49561 mAH', 'BAL': 'N'}, {'Battery': '8', 'Volt': '3418', 'Curr': '0', 'Tempr': '26800', 'Base.State': 'Idle', 'Volt.State': 'Normal', 'Curr.State': 'Normal', 'Temp.State': 'Normal', 'SOC': '100%', 'Coulomb': '49562 mAH', 'BAL': 'N'}, {'Battery': '9', 'Volt': '3415', 'Curr': '0', 'Tempr': '26800', 'Base.State': 'Idle', 'Volt.State': 'Normal', 'Curr.State': 'Normal', 'Temp.State': 'Normal', 'SOC': '100%', 'Coulomb': '49556 mAH', 'BAL': 'N'}, {'Battery': '10', 'Volt': '3413', 'Curr': '0', 'Tempr': '26200', 'Base.State': 'Idle', 'Volt.State': 'Normal', 'Curr.State': 'Normal', 'Temp.State': 'Normal', 'SOC': '100%', 'Coulomb': '49555 mAH', 'BAL': 'N'}, {'Battery': '11', 'Volt': '3411', 'Curr': '0', 'Tempr': '26200', 'Base.State': 'Idle', 'Volt.State': 'Normal', 'Curr.State': 'Normal', 'Temp.State': 'Normal', 'SOC': '100%', 'Coulomb': '49555 mAH', 'BAL': 'N'}, {'Battery': '12', 'Volt': '3415', 'Curr': '0', 'Tempr': '26200', 'Base.State': 'Idle', 'Volt.State': 'Normal', 'Curr.State': 'Normal', 'Temp.State': 'Normal', 'SOC': '100%', 'Coulomb': '49556 mAH', 'BAL': 'N'}, {'Battery': '13', 'Volt': '3414', 'Curr': '0', 'Tempr': '26200', 'Base.State': 'Idle', 'Volt.State': 'Normal', 'Curr.State': 'Normal', 'Temp.State': 'Normal', 'SOC': '100%', 'Coulomb': '49557 mAH', 'BAL': 'N'}, {'Battery': '14', 'Volt': '3413', 'Curr': '0', 'Tempr': '26200', 'Base.State': 'Idle', 'Volt.State': 'Normal', 'Curr.State': 'Normal', 'Temp.State': 'Normal', 'SOC': '100%', 'Coulomb': '49555 mAH', 'BAL': 'N'}]
        self.assertEqual(result, expected_result)
    def test_parse_command_bat3(self):
        result = parse_command_bat(bat_raw_txt_2)
        expected_result = [{'Battery': '0', 'Volt': '3414', 'Curr': '0', 'Tempr': '26000', 'Base.State': 'Idle', 'Volt.State': 'Normal', 'Curr.State': 'Normal', 'Temp.State': 'Normal', 'SOC': '100%', 'Coulomb': '49788 mAH', 'BAL': 'N'}, {'Battery': '1', 'Volt': '3414', 'Curr': '0', 'Tempr': '26000', 'Base.State': 'Idle', 'Volt.State': 'Normal', 'Curr.State': 'Normal', 'Temp.State': 'Normal', 'SOC': '100%', 'Coulomb': '49788 mAH', 'BAL': 'N'}, {'Battery': '2', 'Volt': '3414', 'Curr': '0', 'Tempr': '26000', 'Base.State': 'Idle', 'Volt.State': 'Normal', 'Curr.State': 'Normal', 'Temp.State': 'Normal', 'SOC': '100%', 'Coulomb': '49788 mAH', 'BAL': 'N'}, {'Battery': '3', 'Volt': '3415', 'Curr': '0', 'Tempr': '26000', 'Base.State': 'Idle', 'Volt.State': 'Normal', 'Curr.State': 'Normal', 'Temp.State': 'Normal', 'SOC': '100%', 'Coulomb': '49788 mAH', 'BAL': 'N'}, {'Battery': '4', 'Volt': '3414', 'Curr': '0', 'Tempr': '26000', 'Base.State': 'Idle', 'Volt.State': 'Normal', 'Curr.State': 'Normal', 'Temp.State': 'Normal', 'SOC': '100%', 'Coulomb': '49788 mAH', 'BAL': 'N'}, {'Battery': '5', 'Volt': '3413', 'Curr': '0', 'Tempr': '25900', 'Base.State': 'Idle', 'Volt.State': 'Normal', 'Curr.State': 'Normal', 'Temp.State': 'Normal', 'SOC': '100%', 'Coulomb': '49787 mAH', 'BAL': 'N'}, {'Battery': '6', 'Volt': '3415', 'Curr': '0', 'Tempr': '25900', 'Base.State': 'Idle', 'Volt.State': 'Normal', 'Curr.State': 'Normal', 'Temp.State': 'Normal', 'SOC': '100%', 'Coulomb': '49788 mAH', 'BAL': 'N'}, {'Battery': '7', 'Volt': '3414', 'Curr': '0', 'Tempr': '25900', 'Base.State': 'Idle', 'Volt.State': 'Normal', 'Curr.State': 'Normal', 'Temp.State': 'Normal', 'SOC': '100%', 'Coulomb': '49788 mAH', 'BAL': 'N'}, {'Battery': '8', 'Volt': '3414', 'Curr': '0', 'Tempr': '25900', 'Base.State': 'Idle', 'Volt.State': 'Normal', 'Curr.State': 'Normal', 'Temp.State': 'Normal', 'SOC': '100%', 'Coulomb': '49788 mAH', 'BAL': 'N'}, {'Battery': '9', 'Volt': '3414', 'Curr': '0', 'Tempr': '25900', 'Base.State': 'Idle', 'Volt.State': 'Normal', 'Curr.State': 'Normal', 'Temp.State': 'Normal', 'SOC': '100%', 'Coulomb': '49788 mAH', 'BAL': 'N'}, {'Battery': '10', 'Volt': '3414', 'Curr': '0', 'Tempr': '25600', 'Base.State': 'Idle', 'Volt.State': 'Normal', 'Curr.State': 'Normal', 'Temp.State': 'Normal', 'SOC': '100%', 'Coulomb': '49788 mAH', 'BAL': 'N'}, {'Battery': '11', 'Volt': '3414', 'Curr': '0', 'Tempr': '25600', 'Base.State': 'Idle', 'Volt.State': 'Normal', 'Curr.State': 'Normal', 'Temp.State': 'Normal', 'SOC': '100%', 'Coulomb': '49788 mAH', 'BAL': 'N'}, {'Battery': '12', 'Volt': '3414', 'Curr': '0', 'Tempr': '25600', 'Base.State': 'Idle', 'Volt.State': 'Normal', 'Curr.State': 'Normal', 'Temp.State': 'Normal', 'SOC': '100%', 'Coulomb': '49788 mAH', 'BAL': 'N'}, {'Battery': '13', 'Volt': '3415', 'Curr': '0', 'Tempr': '25600', 'Base.State': 'Idle', 'Volt.State': 'Normal', 'Curr.State': 'Normal', 'Temp.State': 'Normal', 'SOC': '100%', 'Coulomb': '49788 mAH', 'BAL': 'N'}, {'Battery': '14', 'Volt': '3393', 'Curr': '0', 'Tempr': '25600', 'Base.State': 'Idle', 'Volt.State': 'Normal', 'Curr.State': 'Normal', 'Temp.State': 'Normal', 'SOC': '100%', 'Coulomb': '49688 mAH', 'BAL': 'N'}]
        self.assertEqual(result, expected_result)
    def test_parse_command_bat4(self):
        with self.assertRaises(AssertionError) :
            result = parse_command_bat(bat_raw_txt_3)
    def test_parse_command_bat5(self):
        with self.assertRaises(AssertionError) :
            result = parse_command_bat(bat_raw_txt_4)

    # def test_append_cell_voltage(self):
    #     pwr_dicts = [{'Power': '1'}]
    #     self.ser.in_waiting = 0
    #     self.ser.read.return_value = b''
    #     self.ser.write.return_value = None
    #     exec_bat.return_value = "bat 1\n@\nBattery\n$$\npylon>"
    #     parse_command_bat.return_value = []
    #     append_cell_voltage(self.ser, pwr_dicts)
    #     self.assertEqual(pwr_dicts, [{'Power': '1', 'Cells': []}])

    # def test_update_metrics(self):
    #     self.ser.in_waiting = 0
    #     self.ser.read.return_value = b''
    #     self.ser.write.return_value = None
    #     exec_pwr.return_value = "pwr\n@\nPower\n$$\npylon>"
    #     parse_command_pwr.return_value = []
    #     append_cell_voltage.return_value = None
    #     update_metrics(self.ser)
    #     self.assertEqual(BATTERY_VOLTAGE.labels.call_count, 0)
    #     self.assertEqual(BATTERY_CURRENT.labels.call_count, 0)
    #     self.assertEqual(BATTERY_HIGHEST_CELL_VOLTAGE.labels.call_count, 0)
    #     self.assertEqual(BATTERY_LOWEST_CELL_VOLTAGE.labels.call_count, 0)
    #     self.assertEqual(BATTERY_SOC.labels.call_count, 0)
    #     self.assertEqual(BATTERY_STATE.labels.call_count, 0)
    #     self.assertEqual(BATTERY_TEMP.labels.call_count, 0)
    #     self.assertEqual(BATTERY_CELL_VOLTAGE.labels.call_count, 0)
    #     self.assertEqual(BATTERY_CELL_CURRENT.labels.call_count, 0)
    #     self.assertEqual(BATTERY_CELL_TEMP.labels.call_count, 0)
    #     self.assertEqual(BATTERY_CELL_SOC.labels.call_count, 0)
    #     self.assertEqual(BATTERY_CELL_COULOMB.labels.call_count, 0)
    #     self.assertEqual(BATTERY_CELL_STATE.labels.call_count, 0)
    #     self.assertEqual(BATTERY_CELL_BAL.labels.call_count, 0)
    #     self.assertEqual(COLLECT_DATA_FAILS.inc.call_count, 0)

# class TestPrometheusExporter(unittest.TestCase):
#     def test_update_metrics(self):
#         ser = MagicMock()
#         ser.in_waiting = 0
#         ser.read.return_value = b''
#         ser.write.return_value = None
#         ser.decode.return_value = ''
#         update_metrics(ser)

if __name__ == '__main__':
    unittest.main()
