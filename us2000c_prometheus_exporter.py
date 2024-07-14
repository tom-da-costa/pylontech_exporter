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

DEBUG = False

def printDebug(msg):
  if DEBUG:
    print(msg)

class PylontechUnknownCommandError(Exception):
  pass
class PylontechInvalidCommandError(Exception):
  pass
class EmptyStringError(Exception):
  pass
class ParsingError(Exception):
  pass
class PylontechInvalidResponseError(Exception):
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
  def print(self):
    offset = "\t\t"
    print(offset + "Cell:" + self.addr, end=", ")
    print(offset + "Voltage:" + self.voltage, end=", ")
    print(offset + "Current:" + self.current, end=", ")
    print(offset + "Temp:" + self.temp, end=", ")
    print(offset + "Base_State:" + self.base_state, end=", ")
    print(offset + "Voltage_Status:" + self.voltage_status, end=", ")
    print(offset + "Current_status:" + self.current_status, end=", ")
    print(offset + "Temp_Status:" + self.temp_status, end=", ")
    print(offset + "State_Of_Charge:" + self.soc, end=", ")
    print(offset + "Coulomb:" + self.coulomb, end=", ")
    print(offset + "BAL:" + self.BAL)

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
  def addCells(self, cell_dicts):
    self.nbcells = len(cell_dicts)
    for cell_dict in cell_dicts:
      self.cells.append(Cell(cell_dict))
  def getCells(self):
    return cells
  def print(self):
    offset = "\t"
    print(offset + "Batterie:" + self.addr, end=", ")
    print(offset + "Voltage:" + self.voltage, end=", ")
    print(offset + "Current:" + self.current, end=", ")
    print(offset + "Temp:" + self.temp, end=", ")
    print(offset + "Temp_Low:" + self.temp_low, end=", ")
    print(offset + "Temp_High:" + self.temp_high, end=", ")
    print(offset + "Voltage_Low:" + self.voltage_low, end=", ")
    print(offset + "Voltage_High:" + self.voltage_high, end=", ")
    print(offset + "Base_State:" + self.base_state, end=", ")
    print(offset + "Voltage_Status:" + self.voltage_status, end=", ")
    print(offset + "Current_status:" + self.current_status, end=", ")
    print(offset + "Temp_Status:" + self.temp_status, end=", ")
    print(offset + "State_Of_Charge:" + self.soc, end=", ")
    print(offset + "Time:" + self.time, end=", ")
    print(offset + "Bv_Status:" + self.bv_status, end=", ")
    print(offset + "Bt_Status:" + self.bt_status, end=", ")
    print(offset + "MosTemp:" + self.mostemp, end=", ")
    print(offset + "MosTemp_Status:" + self.mostemp_status, end=", ")
    print(offset + "Cells:" + self.nbcells)
    for cell in self.cells:
      cell.print()
    
class Stack:
  def __init__(self, bat_dicts):
    self.batteries = []
    for bat_dict in bat_dicts:
      self.batteries.append(Battery(bat_dict))
  def getBats(self):
    return batteries
  def print(self):
    print("Stack :")
    for bat in self.batteries:
      bat.print()

def get_cells_dict_from_bat(raw_bat_resp):
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
  return cell_dicts

def get_bats_dict_from_pwr(raw_pwr_resp):
  if raw_pwr_resp == "":
    raise EmptyStringError("Can't parse a empty string")
  if "pylon>" in raw_pwr_resp:
    raise PylontechInvalidResponseError("Prompt sill present in the response (= no raw reponse)")
  if "Command completed successfully" not in raw_pwr_resp:
    raise PylontechInvalidResponseError("'Command completed successfully' absent from response")
  if not raw_pwr_resp.startswith('pwr'):
    raise PylontechInvalidCommandError("Wrong command")

  lines = raw_pwr_resp.replace('\r','').splitlines()
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
  for pwr in lines_array[3:]:
    if len(pwr) >= 8 and pwr[8] != 'Absent':
      nbpwr += 1

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
  return pwr_dicts

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
    raise PylontecInvalidCommandError("Invalid Command")
  if "Unknown Command" in resp:
    raise PylontechUnknownCommandError("Unknown Command")
  if resp.endswith("\n$$\npylon>"):
    raise PylontechInvalidResponseError("Reponse do not end with \\n&&\\npylon>")
  resp = resp[0:-10]
  return resp

def get_stack(ser, getcells):
  resp = exec_cmd(ser, 'pwr')
  printDebug("pwr = " + resp)
  bat_dicts = get_bats_dict_from_pwr(resp)
  stack = Stack(bat_dicts)
  if DEBUG:
    stack.print()
  if getcells:
    for bat in stack.getBats():
      time.sleep(0.1)
      printDebug("Adding cell " + bat.addr)
      try:
        resp = exec_cmd(ser, 'bat ' + bat.addr)
        printDebug('bat ' + bat.addr + ' : ' + resp)
        cell_dicts = get_cells_dict_from_bat(resp)
        printDebug('bat ' + bat.addr + ' dicts : ' + cell_dicts)
        bat.addCells(cell_dicts)
      except:
        print("Failed to add bat " + bat.addr)
  if DEBUG:
    stack.print()
  return stack

# Decorate function with metric.
@UPDATE_METRICS_DURATION.time()
def update_metrics(ser):
  try:
    printDebug("1 : Get Battery stack data ...")
    stack = get_stack(ser)
    # print("Exporting infos as json for debug purpose")
    # with open("sample.json", "w") as outfile: 
    #   json.dump(stack.getDicts(), outfile)

    printDebug("2 : Update prometheus metrics ... ", end="")
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
    printDebug('Done')
  except:
    print('Error during data collection, skip the collect.')
    COLLECT_DATA_FAILS.inc()

if __name__ == '__main__':
  print("Starting pylontech exporter ...")
  print("Parsing CLI arguments ...", end="")
  # Parse arguments
  parser = argparse.ArgumentParser(description='Pylontech US2000C Prometheus Exporter')
  parser.add_argument('--device_path', dest="devicepath", type=str, default='/dev/ttyUSB0', help='Path to the serial device')
  parser.add_argument('--extra_delay', dest="extradelay", type=str, default='7', help='Extra delay between each data collection')
  parser.add_argument('--port', dest="port", type=str, default='9094', help='Port to expose the metrics')
  parser.add_argument('--debug', dest="debug", action='store_true', help='Enable debug mode')
  args = parser.parse_args()
  print("Done")
  print("Configuration :")
  DEVICE_PATH = os.getenv('DEVICE_PATH', args.devicepath)
  EXTRA_DELAY = os.getenv('EXTRA_DELAY', args.extradelay)
  HTTP_PORT = os.getenv('HTTP_PORT', args.port)
  DEBUG = True if os.getenv('DEBUG', str(args.debug)).upper() == 'TRUE' else False
  print("DEVICE_PATH = " + DEVICE_PATH)
  print("EXTRA_DELAY = " + EXTRA_DELAY)
  print("HTTP_PORT = " + HTTP_PORT)
  print("DEBUG = " + str(DEBUG))

  # Init serial
  print("Opening Serial port ...", end="")
  ser = serial.Serial(DEVICE_PATH, baudrate=115200)
  print("Done")
  # Start up the server to expose the metrics.
  print("Starting http server ...", end="")
  start_http_server(HTTP_PORT)
  # Generate some requests.
  print("Done")
  print("pylontech exporter started ! Now starting data gathering loop ...")
  i = 0
  while True:
    print("Updating metrics (" + i + ") ...", end=("" if not DEBUG else "\n"))
    update_metrics(ser)
    print("Done" if not DEBUG else f"Done ({i})")
    i += 1
    time.sleep(int(EXTRA_DELAY))