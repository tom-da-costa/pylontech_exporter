from prometheus_client import start_http_server, Gauge, Enum, Summary, Counter
import time
import serial
import json
import os
import argparse

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
def printDebug(msg,end="\n",start=""):
  if DEBUG:
    print("[DEBUG] " + start,end="")
    print(msg,end=end)

class PylontechUnknownCommandError(Exception):
  pass
class PylontechInvalidCommandError(Exception):
  pass
class PylontechInvalidResponseError(Exception):
  pass
class ParsingError(Exception):
  pass

def exec_cmd(ser, cmd):
  if cmd == "":
    raise PylontechInvalidCommandError("The given command is empty")
  while(ser.in_waiting != 0):
    ser.read()
  ser.write(bytes(cmd + "\n", 'ascii'))
  time.sleep(0.5)
  resp = ""
  while(ser.in_waiting != 0):
    try:
      resp += ser.read().decode(encoding="ascii")
    except:
      raise ParsingError("Error decoding caractere")
  printDebug("raw response : " + resp)
  if "Invalid Command" in resp:
    raise PylontechInvalidCommandError("Invalid Command")
  if "Unknown Command" in resp:
    raise PylontechUnknownCommandError("Unknown Command")
  if not resp.endswith("\n$$\npylon>"):
    print(resp[-30:])
    raise PylontechInvalidResponseError("Reponse do not end with \\n$$\\npylon>")
  resp = resp[0:-10]
  return resp

def parse_command_pwr(raw_txt):
# print("Parse into array ...")
  lines = raw_txt.replace('\r','').splitlines()
  raw_array = []
  for line in lines:
    row = line.split()
    raw_array.append(row)
  print(raw_array)
# print('Done')

# print("Check Array ...", end ="")
  assert(raw_array[0][0] == 'pwr')
  assert(raw_array[1][0] == '@')
  assert(raw_array[2][0] == 'Power')
# print("Done")

# print("Get Nb Pwr ...")
  nbpwr = 0
  for pwr in range(0,16):
    if raw_array[3+pwr][8] != 'Absent':
      nbpwr += 1
    else:
      break
# print("NB Batteries = " + str(nbpwr) + "\nDone")

# print("Fix Time slit ...") # Can be improve
  for pwr in range(0,nbpwr):
    hours = raw_array[3+pwr].pop(14)
    raw_array[3+pwr][13] = raw_array[3+pwr][13] + " " + hours
# print('Done')

# print("Transform into dict ...")
  pwr_dicts=[]
  colName = raw_array[2]
  nbvalues = len(colName)
  for pwr in range(0,nbpwr):
    pwr_dict={}
    for col in range(0,nbvalues):
      pwr_dict[colName[col]]=raw_array[3+pwr][col]
    # print(pwr_dict)
    pwr_dicts.append(pwr_dict)
# print('Done')
  return pwr_dicts

def parse_command_bat(raw_txt):
# print("Parse into array ...")
  lines = raw_txt.replace('\r','').splitlines()
  raw_array = []
  for line in lines:
    row = line.split()
    raw_array.append(row)
  #print(raw_array)
# print('Done')
# print("Check Array ...", end ="")
  #assert(raw_array[0][0] == ('bat' + pwr_dict.Power))
  assert(raw_array[1][0] == '@')
  assert(raw_array[2][0] == 'Battery')
# print("Done")

  tmp = raw_array[2].pop(11)
  raw_array[2][10] = raw_array[2][10] + tmp
  tmp = raw_array[2].pop(9)
  raw_array[2][8] = raw_array[2][8] + tmp
  tmp = raw_array[2].pop(7)
  raw_array[2][6] = raw_array[2][6] + tmp
  tmp = raw_array[2].pop(5)
  raw_array[2][4] = raw_array[2][4] + "." + tmp

# print("Fix Cloulomb slit ...") # Can be improve
  for cell in range(0,15):
    hours = raw_array[3+cell].pop(10)
    raw_array[3+cell][9] = raw_array[3+cell][9] + " " + hours
# print('Done')

# print("Transform into dict ...")
  cell_dicts=[]
  colName = raw_array[2]
  nbvalues = len(colName)
  for cell in range(0,15):
    cell_dict={}
    for col in range(0,nbvalues):
      cell_dict[colName[col]]=raw_array[3+cell][col]
    # print(pwr_dict)
    cell_dicts.append(cell_dict)
# print('Done')
  return cell_dicts

# Decorate function with metric.
@UPDATE_METRICS_DURATION.time()
def update_metrics(ser):
  try:
    print("1 : Get Battery stack data ... ", end="\n" if DEBUG else "")
    printDebug("1.1.1 : Executing pwr command ... ")
    pwr_resp = exec_cmd(ser,"pwr")
    printDebug(pwr_resp,start="pwr_resp = ")
    printDebug("1.1.2 : Parsing pwrs raw infos ... ")
    pwr_dicts = parse_command_pwr(pwr_resp)
    printDebug(pwr_dicts,start="pwr_dicts = ")
    printDebug("1.2: Add cells infos")
    for pwr_dict in pwr_dicts:
      idbat = pwr_dict['Power']
      printDebug(f"Get bat {idbat} infos ...")
      bat_resp = exec_cmd(ser,'bat ' + idbat) # to f"bat {idbat}" ?
      printDebug(bat_resp,start=f"bat_resp({idbat}) = ")
      printDebug(f"Parsing bat {idbat} infos ...")
      cell_dicts = parse_command_bat(bat_resp)
      printDebug(cell_dicts,start=f"cell_dicts({idbat}) = ")
      pwr_dict['Cells'] = cell_dicts
    printDebug(pwr_dicts,start="pwr_dicts = ")
    print('Done')
    # print("Exporting infos as json for debug purpose")
    # with open("sample.json", "w") as outfile: 
    #   json.dump(pwr_dicts, outfile)
    print("2 : Update prometheus metrics ... ", end="\n" if DEBUG else "")
    for pwr_dict in pwr_dicts:
      BATTERY_VOLTAGE.labels(index=pwr_dict['Power']).set(float(pwr_dict['Volt'])/1000)
      BATTERY_CURRENT.labels(index=pwr_dict['Power']).set(float(pwr_dict['Curr'])/1000)
      BATTERY_HIGHEST_CELL_VOLTAGE.labels(index=pwr_dict['Power']).set(float(pwr_dict['Vhigh'])/1000)
      BATTERY_LOWEST_CELL_VOLTAGE.labels(index=pwr_dict['Power']).set(float(pwr_dict['Vlow'])/1000)
      BATTERY_SOC.labels(index=pwr_dict['Power']).set(float(pwr_dict['Coulomb'].replace('%','')))
      BATTERY_STATE.labels(index=pwr_dict['Power']).state(pwr_dict['Base.St'])
      BATTERY_TEMP.labels(index=pwr_dict['Power']).set(float(pwr_dict['Tempr'])/1000)
      for cell_dict in pwr_dict['Cells']:
        BATTERY_CELL_VOLTAGE.labels(index=pwr_dict['Power'],cell=cell_dict['Battery']).set(float(cell_dict['Volt'])/1000)
        BATTERY_CELL_CURRENT.labels(index=pwr_dict['Power'],cell=cell_dict['Battery']).set(float(cell_dict['Curr'])/1000)
        BATTERY_CELL_TEMP.labels(index=pwr_dict['Power'],cell=cell_dict['Battery']).set(float(cell_dict['Tempr'])/1000)
        BATTERY_CELL_SOC.labels(index=pwr_dict['Power'],cell=cell_dict['Battery']).set(float(cell_dict['SOC'].replace('%','')))
        BATTERY_CELL_COULOMB.labels(index=pwr_dict['Power'],cell=cell_dict['Battery']).set(float(cell_dict['Coulomb'].replace(' mAH','')))
        BATTERY_CELL_STATE.labels(index=pwr_dict['Power'],cell=cell_dict['Battery']).state(cell_dict['Base.State'])
        BATTERY_CELL_BAL.labels(index=pwr_dict['Power'],cell=cell_dict['Battery']).state(cell_dict['BAL'])
    print('Done')
  except Exception as e:
    print('Error during data collection, skip the collect.')
    print(e)
    COLLECT_DATA_FAILS.inc()


if __name__ == '__main__':
  print("Starting pylontech exporter ...")
  print("Parsing CLI arguments ...", end="")
  # Parse arguments
  parser = argparse.ArgumentParser(description='Pylontech US2000C Prometheus Exporter')
  parser.add_argument('--device_path', dest="devicepath", type=str, default='/dev/ttyUSB0', help='Path to the serial device')
  parser.add_argument('--soft_delay', dest="softdelay", type=str, default='10', help='Soft delay between each data collection')
  parser.add_argument('--port', dest="port", type=str, default='9094', help='Port to expose the metrics')
  parser.add_argument('--debug', dest="debug", action='store_true', help='Enable debug mode')
  args = parser.parse_args()
  print("Done")
  print("Configuration :")
  DEVICE_PATH = os.getenv('DEVICE_PATH', args.devicepath)
  SOFT_DELAY = int(os.getenv('SOFT_DELAY', args.softdelay))
  HTTP_PORT = int(os.getenv('HTTP_PORT', args.port))
  DEBUG = True if os.getenv('DEBUG', str(args.debug)).upper() == 'TRUE' else False
  print("DEVICE_PATH = " + DEVICE_PATH)
  print("SOFT_DELAY = " + str(SOFT_DELAY))
  print("HTTP_PORT = " + str(HTTP_PORT))
  print("DEBUG = " + str(DEBUG))

  # Init serial
  print("Opening Serial port ...", end="")
  ser = serial.Serial(DEVICE_PATH, baudrate=115200)
  print("Done")
  # Start up the server to expose the metrics.
  print("Starting http server ...", end="")
  start_http_server(HTTP_PORT)
  print("Done")
  # Generate some requests.
  print("pylontech exporter started ! Now starting data gathering loop ...")
  i = 0
  while True:
    start = time.time()
    print(f"Updating metrics ({i}) ...")
    update_metrics(ser)
    end = time.time()
    print(f"Update Done ({i})(in {end - start} seconds)")
    i += 1
    if (end - start) < SOFT_DELAY :
      time.sleep(SOFT_DELAY - (end - start))