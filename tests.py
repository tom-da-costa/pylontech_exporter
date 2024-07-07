import unittest
from us2000c_prometheus_exporter import *
from mock_data import *
from unittest.mock import MagicMock, patch


class TestUS2000CPrometheusExporter(unittest.TestCase):
  def test_get_bat_dict_from_pwr1(self):
    result = get_bat_dict_from_pwr(pwr_raw_txt_1)
    expected_result = [{'Power': '1', 'Volt': '51208', 'Curr': '0', 'Tempr': '28900', 'Tlow': '26200', 'Thigh': '26800', 'Vlow': '3404', 'Vhigh': '3419', 'Base.St': 'Idle', 'Volt.St': 'Normal', 'Curr.St': 'Normal', 'Temp.St': 'Normal', 'Coulomb': '100%', 'Time': '2024-07-08 00:23:30', 'B.V.St': 'Normal', 'B.T.St': 'Normal', 'MosTempr': '27500', 'M.T.St': 'Normal'}, {'Power': '2', 'Volt': '51192', 'Curr': '0', 'Tempr': '28400', 'Tlow': '26400', 'Thigh': '27000', 'Vlow': '3405', 'Vhigh': '3418', 'Base.St': 'Idle', 'Volt.St': 'Normal', 'Curr.St': 'Normal', 'Temp.St': 'Normal', 'Coulomb': '100%', 'Time': '2024-07-08 00:23:29', 'B.V.St': 'Normal', 'B.T.St': 'Normal', 'MosTempr': '27700', 'M.T.St': 'Normal'}, {'Power': '3', 'Volt': '51226', 'Curr': '0', 'Tempr': '30000', 'Tlow': '26000', 'Thigh': '27000', 'Vlow': '3400', 'Vhigh': '3418', 'Base.St': 'Idle', 'Volt.St': 'Normal', 'Curr.St': 'Normal', 'Temp.St': 'Normal', 'Coulomb': '100%', 'Time': '2024-07-08 00:23:29', 'B.V.St': 'Normal', 'B.T.St': 'Normal', 'MosTempr': '-', 'M.T.St': '-'}, {'Power': '4', 'Volt': '51201', 'Curr': '0', 'Tempr': '28200', 'Tlow': '25600', 'Thigh': '26000', 'Vlow': '3393', 'Vhigh': '3416', 'Base.St': 'Idle', 'Volt.St': 'Normal', 'Curr.St': 'Normal', 'Temp.St': 'Normal', 'Coulomb': '100%', 'Time': '2024-07-08 00:23:29', 'B.V.St': 'Normal', 'B.T.St': 'Normal', 'MosTempr': '27300', 'M.T.St': 'Normal'}, {'Power': '5', 'Volt': '51198', 'Curr': '0', 'Tempr': '28400', 'Tlow': '25500', 'Thigh': '25900', 'Vlow': '3407', 'Vhigh': '3415', 'Base.St': 'Idle', 'Volt.St': 'Normal', 'Curr.St': 'Normal', 'Temp.St': 'Normal', 'Coulomb': '100%', 'Time': '2024-07-08 00:23:30', 'B.V.St': 'Normal', 'B.T.St': 'Normal', 'MosTempr': '27000', 'M.T.St': 'Normal'}, {'Power': '6', 'Volt': '51194', 'Curr': '0', 'Tempr': '27800', 'Tlow': '24900', 'Thigh': '25000', 'Vlow': '3395', 'Vhigh': '3416', 'Base.St': 'Idle', 'Volt.St': 'Normal', 'Curr.St': 'Normal', 'Temp.St': 'Normal', 'Coulomb': '100%', 'Time': '2024-07-08 00:23:29', 'B.V.St': 'Normal', 'B.T.St': 'Normal', 'MosTempr': '26300', 'M.T.St': 'Normal'}]
    self.assertEqual(result, expected_result)
  def test_get_bat_dict_from_pwr2(self):
    result = get_bat_dict_from_pwr(pwr_raw_txt_2)
    expected_result = [{'Power': '1', 'Volt': '51208', 'Curr': '0', 'Tempr': '28900', 'Tlow': '26200', 'Thigh': '26800', 'Vlow': '3404', 'Vhigh': '3419', 'Base.St': 'Idle', 'Volt.St': 'Normal', 'Curr.St': 'Normal', 'Temp.St': 'Normal', 'Coulomb': '100%', 'Time': '2024-07-08 00:23:30', 'B.V.St': 'Normal', 'B.T.St': 'Normal', 'MosTempr': '27500', 'M.T.St': 'Normal'}]
    self.assertEqual(result, expected_result)
  def test_get_bat_dict_from_pwr3(self):
    with self.assertRaises(PylontechUnknownCommandError) :
        get_bat_dict_from_pwr(pwr_raw_txt_3)



if __name__ == '__main__':
    unittest.main()