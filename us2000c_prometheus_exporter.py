from prometheus_client import start_http_server, Gauge, Enum, Summary, Counter
import time
import serial
import json
import os

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

def exec_pwr(ser):
  while(ser.in_waiting != 0):
    ser.read()
  ser.write(b'pwr\n')
  time.sleep(0.5)
  resp = ""
  while(ser.in_waiting != 0):
    try:
      resp += ser.read().decode(encoding="ascii")
    except:
      print("Error decoding caractere -> skip")
  return resp

def exec_bat(addr):
  while(ser.in_waiting != 0):
    ser.read()
  ser.write(bytes("bat " + addr + "\n", 'ascii'))
  time.sleep(0.5)
  resp = ""
  while(ser.in_waiting != 0):
    try:
      resp += ser.read().decode(encoding="ascii")
    except:
      print("Error decoding caractere -> skip")
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
  assert(raw_array[-2][0] == '$$')
  assert(raw_array[-1][0] == 'pylon>')
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
  assert(raw_array[-2][0] == '$$')
  assert(raw_array[-1][0] == 'pylon>')
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


def append_cell_voltage(ser,pwr_dicts):
  for pwr_dict in pwr_dicts:
    print("Process bat " + pwr_dict['Power'])
    resp = exec_bat(ser,pwr_dict['Power'])
    cell_dicts = parse_command_bat(resp)
    pwr_dict['Cells'] = cell_dicts

# Decorate function with metric.
@UPDATE_METRICS_DURATION.time()
def update_metrics(ser):
  try:
    print("=================\nGetting pwrs raw infos")
    resp = exec_pwr(ser)
    #print(resp)
    print("Parsing pwrs raw infos")
    pwr_dicts = parse_command_pwr(resp)
    #print(pwr_dicts)
    print("Add cells infos")
    append_cell_voltage(ser,pwr_dicts)
  # print(pwr_dicts)
    print("Exporting infos as json for debug purpose")
    with open("sample.json", "w") as outfile: 
      json.dump(pwr_dicts, outfile)
    print("Update prometheus metrics")
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
  except:
    print('Error during data collection, skip the collect.')
    COLLECT_DATA_FAILS.inc()


if __name__ == '__main__':
  device_path = os.getenv('DEVICE_PATH', '/dev/ttyUSB0')
  extra_delay = os.getenv('EXTRA_DELAY', '7')
  # Init serial
  ser = serial.Serial(device_path, baudrate=115200)
  # Start up the server to expose the metrics.
  scan_times = 0
  start_http_server(9094)
  # Generate some requests.
  while True:
    update_metrics(ser)
    time.sleep(int(extra_delay))