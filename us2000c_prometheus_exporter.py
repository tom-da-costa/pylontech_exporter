from prometheus_client import start_http_server, Gauge, Enum, Counter
import time
import serial

# import json
import os
import argparse

# Create a metric to track time spent and requests made.
UPDATE_METRICS_DURATION = Gauge(
    name="metrics_retrieving_duration",
    documentation="Time spent retrieving metrics",
    namespace="pylontech",
    unit="seconds",
)
COLLECT_DATA_FAILS = Counter(
    "data_collect_fails",
    "Times The Data Collection Fails",
    namespace="pylontech",
    unit="times",
)

BATTERY_VOLTAGE = Gauge(
    "battery_voltage", "Battery Voltage", ["index"], "pylontech", "", "volts"
)
BATTERY_CURRENT = Gauge(
    "battery_current", "Battery Current", ["index"], "pylontech", "", "amperes"
)
BATTERY_HIGHEST_CELL_VOLTAGE = Gauge(
    "battery_highest_cell_voltage",
    "Battery Highest Cell Voltage",
    ["index"],
    "pylontech",
    "",
    "volts",
)
BATTERY_LOWEST_CELL_VOLTAGE = Gauge(
    "battery_lowest_cell_voltage",
    "Battery Lowest Cell Voltage",
    ["index"],
    "pylontech",
    "",
    "volts",
)
BATTERY_SOC = Gauge(
    "battery_state_of_charge",
    "Battery State of Charge Percentage (= pwr coulomb)",
    ["index"],
    "pylontech",
    "",
    "percentage",
)
BATTERY_STATE = Enum(
    "battery_state",
    "Battery State",
    ["index"],
    "pylontech",
    states=["Idle", "Charge", "Dischg"],
)
BATTERY_TEMP = Gauge(
    "battery_temperature", "Battery Temperature", ["index"], "pylontech", "", "celsius"
)

BATTERY_CELL_VOLTAGE = Gauge(
    "battery_cell_voltage",
    "Battery Cell Voltage",
    ["index", "cell"],
    "pylontech",
    "",
    "volts",
)
BATTERY_CELL_CURRENT = Gauge(
    "battery_cell_current",
    "Battery Cell Current",
    ["index", "cell"],
    "pylontech",
    "",
    "amperes",
)
BATTERY_CELL_TEMP = Gauge(
    "battery_cell_temperature",
    "Battery Cell Temperature",
    ["index", "cell"],
    "pylontech",
    "",
    "celsius",
)
BATTERY_CELL_SOC = Gauge(
    "battery_cell_state_of_charge",
    "Battery Cell State of Charge Percentage",
    ["index", "cell"],
    "pylontech",
    "",
    "percentage",
)
BATTERY_CELL_COULOMB = Gauge(
    "battery_cell_coulomb",
    "Battery Cell Coulomb (Aka Stored Energy)",
    ["index", "cell"],
    "pylontech",
    "",
    "mah",
)
BATTERY_CELL_STATE = Enum(
    "battery_cell_state",
    "Battery Cell State",
    ["index", "cell"],
    "pylontech",
    states=["Idle", "Charge", "Dischg"],
)
BATTERY_CELL_BAL = Enum(
    "battery_cell_bal_state",
    "Battery Cell BAL Properties State",
    ["index", "cell"],
    "pylontech",
    states=["N", "Y"],
)

DEBUG = False


def printDebug(msg, end="\n", start=""):
    if DEBUG:
        print("[DEBUG] " + start, end="")
        print(msg, end=end)


class PylontechUnknownCommandError(Exception):
    pass


class PylontechInvalidCommandError(Exception):
    pass


class PylontechInvalidResponseError(Exception):
    pass


class DecodeError(Exception):
    pass


def exec_cmd(ser, cmd):
    if cmd == "":
        raise PylontechInvalidCommandError("The given command is empty")
    while ser.in_waiting != 0:
        ser.read()
    ser.write(bytes(cmd + "\n", "ascii"))
    time.sleep(0.75)
    resp = ""
    while ser.in_waiting != 0:
        try:
            resp += ser.read().decode(encoding="ascii")
        except:
            raise DecodeError("Error decoding caractere")
    printDebug("raw response : " + resp)
    if "Invalid Command" in resp:
        raise PylontechInvalidCommandError(f"Invalid Command ({cmd})")
    if "Unknown Command" in resp:
        raise PylontechUnknownCommandError(f"Unknown Command ({cmd})")
    if not resp.endswith("pylon>"):
        raise PylontechInvalidResponseError(f"Reponse do not end with pylon>. resp : {resp}")
    if not "@" in resp and not "@" in resp:
        raise PylontechInvalidResponseError(f"Invalid format, not @ and $$ present in response. resp : {resp}")
    return resp

def extract_response_from_raw(raw_resp):
    raw_resp_filtered = raw_resp.replace("\r", "")
    start = raw_resp_filtered.find("@\n")
    end = raw_resp_filtered.find("\n$$")
    if start == -1 or end == -1:
        raise PylontechInvalidResponseError(f"Invalid format, not @ and $$ present in response. resp : {raw_resp}")
    return raw_resp_filtered[start:end]

def parse_pwr_response(resp):
    lines = resp.splitlines()
    lines_tokens = []
    for line in lines:
        row = line.split()
        lines_tokens.append(row)

    assert lines_tokens[0][0] == "Power"

    nbpwr = 0
    for pwr in range(0, 16):
        if lines_tokens[1 + pwr][8] != "Absent":
            nbpwr += 1
        else:
            break

    for pwr in range(0, nbpwr):
        hours = lines_tokens[1 + pwr].pop(14)
        lines_tokens[1 + pwr][13] = lines_tokens[1 + pwr][13] + " " + hours

    pwr_dicts = []
    colName = lines_tokens[0]
    nbvalues = len(colName)
    for pwr in range(0, nbpwr):
        pwr_dict = {}
        for col in range(0, nbvalues):
            pwr_dict[colName[col]] = lines_tokens[1 + pwr][col]
        pwr_dicts.append(pwr_dict)
    return pwr_dicts


def parse_bat_response(resp):
    lines = resp.replace("\r", "").splitlines()
    lines_tokens = []
    for line in lines:
        row = line.split()
        lines_tokens.append(row)

    assert lines_tokens[0][0] == "Battery"

    tmp = lines_tokens[0].pop(11)
    lines_tokens[0][10] = lines_tokens[0][10] + tmp
    tmp = lines_tokens[0].pop(9)
    lines_tokens[0][8] = lines_tokens[0][8] + tmp
    tmp = lines_tokens[0].pop(7)
    lines_tokens[0][6] = lines_tokens[0][6] + tmp
    tmp = lines_tokens[0].pop(5)
    lines_tokens[0][4] = lines_tokens[0][4] + "." + tmp

    for cell in range(0, 15):
        hours = lines_tokens[1 + cell].pop(10)
        lines_tokens[1 + cell][9] = lines_tokens[1 + cell][9] + " " + hours

    cell_dicts = []
    colName = lines_tokens[0]
    nbvalues = len(colName)
    for cell in range(0, 15):
        cell_dict = {}
        for col in range(0, nbvalues):
            cell_dict[colName[col]] = lines_tokens[1 + cell][col]
        cell_dicts.append(cell_dict)
    return cell_dicts


# Decorate function with metric.
@UPDATE_METRICS_DURATION.time()
def update_metrics(ser):
    try:
        print("1 : Get Battery stack data ... ", end="\n" if DEBUG else "")
        printDebug("1.2 : Get battery infos")
        printDebug("1.1.1 : Executing pwr command ... ")
        pwr_raw_resp = exec_cmd(ser, "pwr")
        printDebug(pwr_raw_resp, start="pwr_raw_resp = ")

        printDebug("1.1.2 : Extract response from raw response ... ")
        pwr_resp = extract_response_from_raw(pwr_raw_resp)
        printDebug(pwr_raw_resp, start="pwr_resp = ")

        printDebug("1.1.3 : Parsing pwrs raw infos ... ")
        pwr_dicts = parse_pwr_response(pwr_resp)
        printDebug(pwr_dicts, start="pwr_dicts = ")

        printDebug("1.2 : Add cells infos")
        for pwr_dict in pwr_dicts:
            idbat = pwr_dict["Power"]
            try:
                printDebug(f"1.2.1 : Get bat {idbat} infos ...")
                bat_raw_resp = exec_cmd(ser, "bat " + idbat)  # to f"bat {idbat}" ?
                printDebug(bat_raw_resp, start=f"bat_raw_resp({idbat}) = ")

                printDebug("1.1.2 : Extract response from raw response ... ")
                bat_resp = extract_response_from_raw(bat_resp)
                printDebug(bat_resp, start=f"bat_resp({idbat}) = ")

                printDebug(f"1.2.3: Parsing bat {idbat} infos ...")
                cell_dicts = parse_bat_response(bat_resp)
                printDebug(cell_dicts, start=f"cell_dicts({idbat}) = ")
                pwr_dict["Cells"] = cell_dicts
            except Exception as e:
                print(f"Error while collecting cells of battery {idbat}. Skip bat {idbat}")
                print(e)
                COLLECT_DATA_FAILS.inc()
        printDebug(pwr_dicts, start="pwr_dicts = ")
        print("Done")
        # print("Exporting infos as json for debug purpose")
        # with open("sample.json", "w") as outfile:
        #   json.dump(pwr_dicts, outfile)
        print("2 : Update prometheus metrics ... ", end="\n" if DEBUG else "")
        for pwr_dict in pwr_dicts:
            BATTERY_VOLTAGE.labels(index=pwr_dict["Power"]).set(
                float(pwr_dict["Volt"]) / 1000
            )
            BATTERY_CURRENT.labels(index=pwr_dict["Power"]).set(
                float(pwr_dict["Curr"]) / 1000
            )
            BATTERY_HIGHEST_CELL_VOLTAGE.labels(index=pwr_dict["Power"]).set(
                float(pwr_dict["Vhigh"]) / 1000
            )
            BATTERY_LOWEST_CELL_VOLTAGE.labels(index=pwr_dict["Power"]).set(
                float(pwr_dict["Vlow"]) / 1000
            )
            BATTERY_SOC.labels(index=pwr_dict["Power"]).set(
                float(pwr_dict["Coulomb"].replace("%", ""))
            )
            BATTERY_STATE.labels(index=pwr_dict["Power"]).state(pwr_dict["Base.St"])
            BATTERY_TEMP.labels(index=pwr_dict["Power"]).set(
                float(pwr_dict["Tempr"]) / 1000
            )
            if "Cells" in pwr_dict.keys():
                for cell_dict in pwr_dict["Cells"]:
                    BATTERY_CELL_VOLTAGE.labels(
                        index=pwr_dict["Power"], cell=cell_dict["Battery"]
                    ).set(float(cell_dict["Volt"]) / 1000)
                    BATTERY_CELL_CURRENT.labels(
                        index=pwr_dict["Power"], cell=cell_dict["Battery"]
                    ).set(float(cell_dict["Curr"]) / 1000)
                    BATTERY_CELL_TEMP.labels(
                        index=pwr_dict["Power"], cell=cell_dict["Battery"]
                    ).set(float(cell_dict["Tempr"]) / 1000)
                    BATTERY_CELL_SOC.labels(
                        index=pwr_dict["Power"], cell=cell_dict["Battery"]
                    ).set(float(cell_dict["SOC"].replace("%", "")))
                    BATTERY_CELL_COULOMB.labels(
                        index=pwr_dict["Power"], cell=cell_dict["Battery"]
                    ).set(float(cell_dict["Coulomb"].replace(" mAH", "")))
                    BATTERY_CELL_STATE.labels(
                        index=pwr_dict["Power"], cell=cell_dict["Battery"]
                    ).state(cell_dict["Base.State"])
                    BATTERY_CELL_BAL.labels(
                        index=pwr_dict["Power"], cell=cell_dict["Battery"]
                    ).state(cell_dict["BAL"])
        print("Done")
    except Exception as e:
        print("Error during data collection, skip the collect.")
        print(e)
        COLLECT_DATA_FAILS.inc()


if __name__ == "__main__":
    print("Starting pylontech exporter ...")
    print("Parsing CLI arguments ...", end="")
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Pylontech US2000C Prometheus Exporter"
    )
    parser.add_argument(
        "--device_path",
        dest="devicepath",
        type=str,
        default="/dev/ttyUSB0",
        help="Path to the serial device",
    )
    parser.add_argument(
        "--soft_delay",
        dest="softdelay",
        type=str,
        default="10",
        help="Soft delay between each data collection",
    )
    parser.add_argument(
        "--port",
        dest="port",
        type=str,
        default="9094",
        help="Port to expose the metrics",
    )
    parser.add_argument(
        "--debug", dest="debug", action="store_true", help="Enable debug mode"
    )
    args = parser.parse_args()
    print("Done")
    print("Configuration :")
    DEVICE_PATH = os.getenv("DEVICE_PATH", args.devicepath)
    SOFT_DELAY = int(os.getenv("SOFT_DELAY", args.softdelay))
    HTTP_PORT = int(os.getenv("HTTP_PORT", args.port))
    DEBUG = True if os.getenv("DEBUG", str(args.debug)).upper() == "TRUE" else False
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
        if (end - start) < SOFT_DELAY:
            print(f"Waiting {SOFT_DELAY - (end - start)} seconds")
            time.sleep(SOFT_DELAY - (end - start))
