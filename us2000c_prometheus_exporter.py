from prometheus_client import start_http_server, Gauge, Enum, Summary, Counter
import time
import serial
import json
import os
import argparse
import re

# Create a metric to track time spent and requests made.
UPDATE_METRICS_DURATION = Gauge(name='metrics_retrieving_duration', documentation='Time spent retrieving metrics', namespace='pylontech',unit='seconds')
COLLECT_DATA_FAILS = Counter('data_collect_fails','Times The Data Collection Fails',namespace='pylontech',unit='times')

BATTERY_VOLTAGE = Gauge('battery_voltage', 'Battery Voltage', ['index'], 'pylontech', '' , 'volts')
BATTERY_CURRENT = Gauge('battery_current', 'Battery Current', ['index'], 'pylontech', '' , 'amperes')
BATTERY_HIGHEST_CELL_VOLTAGE = Gauge('battery_highest_cell_voltage', 'Battery Highest Cell Voltage', ['index'], 'pylontech', '' , 'volts')
BATTERY_LOWEST_CELL_VOLTAGE = Gauge('battery_lowest_cell_voltage', 'Battery Lowest Cell Voltage', ['index'], 'pylontech', '' , 'volts')
BATTERY_SOC = Gauge('battery_state_of_charge', 'Battery State of Charge Percentage (= pwr coulomb)', ['index'], 'pylontech', '' , 'percentage')
BATTERY_STATE = Enum('battery_state', 'Battery State', ['index'], 'pylontech', states=['Idle', 'Charge', 'Dischg'])
BATTERY_TEMP = Gauge('battery_temperature', 'Battery Temperature', ['index'], 'pylontech', '' , 'celsius')

BATTERY_CELL_VOLTAGE = Gauge('battery_cell_voltage', 'Battery Cell Voltage', ['index','cell'], 'pylontech', '' , 'volts')
BATTERY_CELL_CURRENT = Gauge('battery_cell_current', 'Battery Cell Current', ['index','cell'], 'pylontech', '' , 'amperes')
BATTERY_CELL_TEMP = Gauge('battery_cell_temperature', 'Battery Cell Temperature', ['index','cell'], 'pylontech', '' , 'celsius')
BATTERY_CELL_SOC = Gauge('battery_cell_state_of_charge', 'Battery Cell State of Charge Percentage', ['index','cell'], 'pylontech', '' , 'percentage')
BATTERY_CELL_COULOMB = Gauge('battery_cell_coulomb', 'Battery Cell Coulomb (Aka Stored Energy)', ['index','cell'], 'pylontech', '' , 'mah')
BATTERY_CELL_STATE = Enum('battery_cell_state', 'Battery Cell State', ['index','cell'], 'pylontech', states=['Idle', 'Charge', 'Dischg'])
BATTERY_CELL_BAL = Enum('battery_cell_bal_state', 'Battery Cell BAL Properties State', ['index','cell'], 'pylontech', states=['N', 'Y'])

class PylontechUnknownCommandError:
  pass
class PylontechInvalidCommandError:
  pass
class EmptyStringError:
  pass
class ParsingError:
  pass
class PylontechInvalidResponseError:
  pass

class Cell:
  def __init__(self,cell_dict):
    self.addr = bat_dict['Battery']
    self.voltage = bat_dict['Volt']
    self.current = bat_dict['Curr']
    self.temp = bat_dict['Tempr']
    self.base_state = bat_dict['Base.St']
    self.voltage_status = bat_dict['Volt.St']
    self.current_status = bat_dict['Curr.St']
    self.temp_status = bat_dict['Temp.St']
    self.soc = bat_dict['SOC']
    self.coulomb = bat_dict['Coulomb']
    self.BAL = bat_dict['BAL']

class Battery:
  def __init__(self, bat_dict):
    self.addr = bat_dict['Power']
    self.voltage = bat_dict['Volt']
    self.current = bat_dict['Curr']
    self.temp = bat_dict['Tempr']
    self.temp_low = bat_dict['Tlow']
    self.temp_high = bat_dict['Thigh']
    self.voltage_low = bat_dict['Vlow']
    self.voltage_high = bat_dict['Vhigh']
    self.base_state = bat_dict['Base.St']
    self.voltage_status = bat_dict['Volt.St']
    self.current_status = bat_dict['Curr.St']
    self.temp_status = bat_dict['Temp.St']
    self.soc = bat_dict['Coulomb']
    self.time = bat_dict['Time']
    self.bv_status = bat_dict['B.V.St']
    self.bt_status = bat_dict['B.T.St']
    self.mostemp = bat_dict['MosTempr']
    self.mostemp_status = bat_dict['M.T.St']
    self.nbcells = 0
    self.cells = []
  def addCells(self, raw_bat_resp):
    if raw_bat_resp == "":
      raise EmptyStringError("Can't parse a empty string")
    if "pylon>" in raw_bat_resp:
      raise PylontechInvalidResponseError("Prompt sill present in the response (= no raw reponse)")    
    if "Command completed successfully" not in raw_bat_resp:
      raise PylontechInvalidResponseError("'Command completed successfully' absent from response")
    if not raw_bat_resp.startswith('bat'):
      raise PylontechInvalidResponseError("Wrong command")

    lines = raw_bat_resp.replace('\r','').splitlines()
    lines_array = []
    nbcolonne = -1
    for line in lines:
      row = line.split()
      if not line.startswith("Battery"):
        row = re.sub('\. ', '.', re.sub('e S', 'e.S', line)).split()
        nbcolonne = len(row)
      lines_array.append(row)

    if nbcolonne == -1 or len(lines_array) < 2 or (lines_array[1][0] != '@' and lines_array[2][0] != 'Battery') :
      raise PylontechInvalidResponseError("Header not present or not at the right place")

    # print("Fix Cloulomb slit ...") # Can be improve
    for cell in range(0,15):
      hours = lines_array[3+cell].pop(10)
      lines_array[3+cell][9] = lines_array[3+cell][9] + " " + hours
    # print('Done')

    # print("Transform into dict ...")
    cell_dicts=[]
    colName = lines_array[2]
    nbvalues = len(colName)
    for cell in range(0,15):
      cell_dict={}
      for col in range(0,nbvalues):
        cell_dict[colName[col]]=lines_array[3+cell][col]
      # print(pwr_dict)
      cell_dicts.append(cell_dict)
    # print('Done')
    self.nbcells = len(cell_dicts)

    for bat_dict in pwr_dicts:
      self.cells.append(Battery(bat_dict))
  def getCells(self):
    return cells
    

class Stack:
  def __init__(self, raw_txt):
    self.batteries = []
    if raw_txt == "":
      raise EmptyStringError("Can't parse a empty string")
    if "pylon>" in raw_txt:
      raise PylontechInvalidResponseError("Prompt sill present in the response (= no raw reponse)")
    if "Command completed successfully" not in raw_txt:
      raise PylontechInvalidResponseError("'Command completed successfully' absent from response")
    if not raw_txt.startswith('pwr'):
      raise PylontechInvalidResponseError("Wrong command")

    lines = raw_txt.replace('\r','').splitlines()
    lines_array = []
    nbcolonne = -1
    for line in lines:
      row = line.split()
      if not line.startswith("Power"):
        nbcolonne = len(row)
      lines_array.append(row)

    if nbcolonne == -1 or len(lines_array) < 3 or (lines_array[1][0] != '@' and lines_array[2][0] != 'Power') :
      raise PylontechInvalidResponseError("Header not present or not at the right place")

    nbpwr = 0
    for pwr in lines_array[3+pwr:]:
      if len(pwr) >= 8 and pwr[8] != 'Absent':
        nbpwr += 1
    self.nbbat = nbpwr

    for pwr in range(0,nbpwr):
      hours = lines_array[3+pwr].pop(14)
      lines_array[3+pwr][13] = lines_array[3+pwr][13] + " " + hours

    pwr_dicts=[]
    colName = lines_array[2]
    nbvalues = len(colName)
    for pwr in range(0,nbpwr):
      pwr_dict={}
      for col in range(0,nbvalues):
        pwr_dict[colName[col]]=lines_array[3+pwr][col]
      # print(pwr_dict)
      pwr_dicts.append(pwr_dict)
    # print('Done')

    for bat_dict in pwr_dicts:
      self.batteries.append(Battery(bat_dict))
    
  def getBats(self):
    return batteries

def exec_cmd(ser, cmd):
  if cmd == "":
    raise EmptyStringError("The given command is empty")
  while(ser.in_waiting != 0):
    ser.read()
  ser.write(bytes(cmd + "\n"))
  time.sleep(0.5)
  resp = ""
  while(ser.in_waiting != 0):
    try:
      resp += ser.read().decode(encoding="ascii")
    except:
      print("Error decoding caractere")
  if "Invalid Command" in resp:
    raise PylontecInvalidCommandError("")
  if "Unknown Command" in resp:
    raise PylontechUnknownCommandError("")
  if resp.endswith("\n$$\npylon>"):
    raise PylontechInvalidResponseError("Reponse do not end with \\n&&\\npylon>")
  resp = resp[0:-10]
  return resp

def get_stack(ser):
  resp = exec_cmd('pwr')
  stack = Stack(resp)
  for bat in stack.getBats():
    time.sleep(0.1)
    resp = exec_cmd('bat ' + bat.addr)
    bat.addCells(resp)
  return stack

# Decorate function with metric.
@UPDATE_METRICS_DURATION.time()
def update_metrics(ser):
  try:
    print("=================\nUpdate metrics")
    print("Get Battery stack data ...")
    stack = get_stack(ser)
    # print("Exporting infos as json for debug purpose")
    # with open("sample.json", "w") as outfile: 
    #   json.dump(stack.getDicts(), outfile)
    print("Update prometheus metrics ...")
    for bat in stack.getBats():
      BATTERY_VOLTAGE.labels(index=bat.addr).set(float(bat.voltage)/1000)
      BATTERY_CURRENT.labels(index=bat.addr).set(float(bat.current)/1000)
      BATTERY_HIGHEST_CELL_VOLTAGE.labels(index=bat.addr).set(float(bat.voltage_high)/1000)
      BATTERY_LOWEST_CELL_VOLTAGE.labels(index=bat.addr).set(float(bat.voltage_low)/1000)
      BATTERY_SOC.labels(index=bat.addr).set(float(bat.soc.replace('%','')))
      BATTERY_STATE.labels(index=bat.addr).state(bat.base_state)
      BATTERY_TEMP.labels(index=bat.addr).set(float(bat.temp)/1000)
      for cell in bat.getCells():
        BATTERY_CELL_VOLTAGE.labels(index=bat.addr,cell=cell.id).set(float(cell.voltage)/1000)
        BATTERY_CELL_CURRENT.labels(index=bat.addr,cell=cell.id).set(float(cell.current)/1000)
        BATTERY_CELL_TEMP.labels(index=bat.addr,cell=cell.id).set(float(cell.temp)/1000)
        BATTERY_CELL_SOC.labels(index=bat.addr,cell=cell.id).set(float(cell.soc.replace('%','')))
        BATTERY_CELL_COULOMB.labels(index=bat.addr,cell=cell.id).set(float(cell.coulomb.replace(' mAH','')))
        BATTERY_CELL_STATE.labels(index=bat.addr,cell=cell.id).state(cell.base_state)
        BATTERY_CELL_BAL.labels(index=bat.addr,cell=cell.id).state(cell.BAL)
    print('Done')
  except:
    print('Error during data collection, skip the collect.')
    COLLECT_DATA_FAILS.inc()

if __name__ == '__main__':
  # Parse arguments
  parser = argparse.ArgumentParser(description='Pylontech US2000C Prometheus Exporter')
  parser.add_argument('--device_path', dest="devicepath", type=str, default='/dev/ttyUSB0', help='Path to the serial device')
  parser.add_argument('--extra_delay', dest="extradelay", type=str, default='7', help='Extra delay between each data collection')
  parser.add_argument('--port', dest="port", type=str, default='9094', help='Port to expose the metrics')
  parser.add_argument('--debug', dest="debug", action='store_true', help='Enable debug mode')
  args = parser.parse_args()

  DEVICE_PATH = os.getenv('DEVICE_PATH', args.devicepath)
  EXTRA_DELAY = os.getenv('EXTRA_DELAY', args.extradelay)
  HTTP_PORT = os.getenv('HTTP_PORT', args.port)
  DEBUG = True if os.getenv('DEBUG', str(args.debug)).upper() == 'TRUE' else False

  # Init serial
  ser = serial.Serial(DEVICE_PATH, baudrate=115200)
  # Start up the server to expose the metrics.
  start_http_server(HTTP_PORT)
  # Generate some requests.
  while True:
    update_metrics(ser)
    time.sleep(int(EXTRA_DELAY))