import unittest
from us2000c_prometheus_exporter import *
from mocked_data import *
from unittest.mock import MagicMock, patch


class TestUS2000CPrometheusExporter(unittest.TestCase):
  def test_get_bats_dict_from_pwr1(self):
    result = get_bats_dict_from_pwr(pwr_raw_txt_1)
    self.assertEqual(result, pwr_raw_txt_1_expected_result)
  def test_get_bats_dict_from_pwr2(self):
    result = get_bats_dict_from_pwr(pwr_raw_txt_2)
    self.assertEqual(result, pwr_raw_txt_2_expected_result)
  def test_get_bats_dict_from_pwr3(self):
    with self.assertRaises(PylontechUnknownCommandError) :
        get_bats_dict_from_pwr(pwr_raw_txt_3)
  def test_get_bats_dict_from_pwr4(self):
    with self.assertRaises(PylontechInvalidResponseError) :
        get_bats_dict_from_pwr(pwr_raw_txt_4)


  # def test_get_cells_dict_from_bat1(self):
  #   result = get_cells_dict_from_bat(bat_raw_txt_1)
  #   self.assertEqual(result,bat_raw_txt_1_expected_result)
  # def test_get_cells_dict_from_bat2(self):
  #   result = get_cells_dict_from_bat(bat_raw_txt_2)
  #   self.assertEqual(result,bat_raw_txt_2_expected_result)
  def test_get_cells_dict_from_bat3(self):
    with self.assertRaises(PylontechInvalidCommandError) :
      get_cells_dict_from_bat(bat_raw_txt_3)
  def test_get_cells_dict_from_bat4(self):
    with self.assertRaises(PylontechUnknownCommandError) :
      get_cells_dict_from_bat(bat_raw_txt_4)
  def test_get_cells_dict_from_bat5(self):
    with self.assertRaises(PylontechInvalidResponseError) :
      get_cells_dict_from_bat(bat_raw_txt_5)


if __name__ == '__main__':
    unittest.main()