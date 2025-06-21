import pytest
from us2000c_prometheus_exporter import extract_response_from_raw, PylontechInvalidResponseError

@pytest.fixture
def pwr_raw_resps():
    pwr_raw_resps = []
    pwr_raw_resps.append("""pwr
@
Power Volt   Curr   Tempr  Tlow   Thigh  Vlow   Vhigh  Base.St  Volt.St  Curr.St  Temp.St  Coulomb  Time                 B.V.St   B.T.St   MosTempr M.T.St  
1     51208  0      28900  26200  26800  3404   3419   Idle     Normal   Normal   Normal   100%     2024-07-08 00:23:30  Normal   Normal  27500    Normal  
2     51192  0      28400  26400  27000  3405   3418   Idle     Normal   Normal   Normal   100%     2024-07-08 00:23:29  Normal   Normal  27700    Normal  
3     51226  0      30000  26000  27000  3400   3418   Idle     Normal   Normal   Normal   100%     2024-07-08 00:23:29  Normal   Normal   -        -       
4     51201  0      28200  25600  26000  3393   3416   Idle     Normal   Normal   Normal   100%     2024-07-08 00:23:29  Normal   Normal  27300    Normal  
5     51198  0      28400  25500  25900  3407   3415   Idle     Normal   Normal   Normal   100%     2024-07-08 00:23:30  Normal   Normal  27000    Normal  
6     51194  0      27800  24900  25000  3395   3416   Idle     Normal   Normal   Normal   100%     2024-07-08 00:23:29  Normal   Normal  26300    Normal  
7     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
8     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
9     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
10    -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
11    -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
12    -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
13    -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
14    -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
15    -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
16    -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
Command completed successfully
$$
pylon>""")
    pwr_raw_resps.append("""pwr
@
Power Volt   Curr   Tempr  Tlow   Thigh  Vlow   Vhigh  Base.St  Volt.St  Curr.St  Temp.St  Coulomb  Time                 B.V.St   B.T.St   MosTempr M.T.St  
1     51208  0      28900  26200  26800  3404   3419   Idle     Normal   Normal   Normal   100%     2024-07-08 00:23:30  Normal   Normal  27500    Normal  
2     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -     
3     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -     
4     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -     
5     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -     
6     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -     
7     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
8     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
9     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
10    -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
11    -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
12    -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
13    -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
14    -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
15    -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
16    -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
Command completed successfully
$$
pylon>""")
    return pwr_raw_resps

@pytest.fixture
def bat_raw_resps():
    bat_raw_resps = []
    bat_raw_resps.append("""bat 1
@
Battery  Volt     Curr     Tempr    Base State   Volt. State  Curr. State  Temp. State  SOC          Coulomb      BAL         
0        3416     0        26500    Idle         Normal       Normal       Normal       100%         49560 mAH      N
1        3403     0        26500    Idle         Normal       Normal       Normal       100%         49477 mAH      N
2        3414     0        26500    Idle         Normal       Normal       Normal       100%         49558 mAH      N
3        3413     0        26500    Idle         Normal       Normal       Normal       100%         49557 mAH      N
4        3413     0        26500    Idle         Normal       Normal       Normal       100%         49556 mAH      N
5        3405     0        26800    Idle         Normal       Normal       Normal       100%         49477 mAH      N
6        3412     0        26800    Idle         Normal       Normal       Normal       100%         49548 mAH      N
7        3418     0        26800    Idle         Normal       Normal       Normal       100%         49561 mAH      N
8        3418     0        26800    Idle         Normal       Normal       Normal       100%         49562 mAH      N
9        3415     0        26800    Idle         Normal       Normal       Normal       100%         49556 mAH      N
10       3413     0        26200    Idle         Normal       Normal       Normal       100%         49555 mAH      N
11       3411     0        26200    Idle         Normal       Normal       Normal       100%         49555 mAH      N
12       3415     0        26200    Idle         Normal       Normal       Normal       100%         49556 mAH      N
13       3414     0        26200    Idle         Normal       Normal       Normal       100%         49557 mAH      N
14       3413     0        26200    Idle         Normal       Normal       Normal       100%         49555 mAH      N
Command completed successfully
$$
pylon>""")
    bat_raw_resps.append("""bat 4
@
Battery  Volt     Curr     Tempr    Base State   Volt. State  Curr. State  Temp. State  SOC          Coulomb      BAL         
0        3414     0        26000    Idle         Normal       Normal       Normal       100%         49788 mAH      N
1        3414     0        26000    Idle         Normal       Normal       Normal       100%         49788 mAH      N
2        3414     0        26000    Idle         Normal       Normal       Normal       100%         49788 mAH      N
3        3415     0        26000    Idle         Normal       Normal       Normal       100%         49788 mAH      N
4        3414     0        26000    Idle         Normal       Normal       Normal       100%         49788 mAH      N
5        3413     0        25900    Idle         Normal       Normal       Normal       100%         49787 mAH      N
6        3415     0        25900    Idle         Normal       Normal       Normal       100%         49788 mAH      N
7        3414     0        25900    Idle         Normal       Normal       Normal       100%         49788 mAH      N
8        3414     0        25900    Idle         Normal       Normal       Normal       100%         49788 mAH      N
9        3414     0        25900    Idle         Normal       Normal       Normal       100%         49788 mAH      N
10       3414     0        25600    Idle         Normal       Normal       Normal       100%         49788 mAH      N
11       3414     0        25600    Idle         Normal       Normal       Normal       100%         49788 mAH      N
12       3414     0        25600    Idle         Normal       Normal       Normal       100%         49788 mAH      N
13       3415     0        25600    Idle         Normal       Normal       Normal       100%         49788 mAH      N
14       3393     0        25600    Idle         Normal       Normal       Normal       100%         49688 mAH      N
Command completed successfully
$$
pylon>""")
    bat_raw_resps.append("""bat 20 
@
Invalid command or fail to excute.
Usage:
Battery data show - bat [pwr][index]
$$
pylon>""")
    bat_raw_resps.append("""bit 1
@
Unknown command 'bit' - try 'help'
$$
pylon>""")
    bat_raw_resps.append("""toto 1
@
Unknown command 'toto' - try 'help'
$""")
    return bat_raw_resps

# @pytest.mark.parametrize("index", [1, 2,])
def test_response_extraction_pwr_1(pwr_raw_resps):
    pwr_resp = extract_response_from_raw(pwr_raw_resps[1])
    expected_result = """Power Volt   Curr   Tempr  Tlow   Thigh  Vlow   Vhigh  Base.St  Volt.St  Curr.St  Temp.St  Coulomb  Time                 B.V.St   B.T.St   MosTempr M.T.St  
1     51208  0      28900  26200  26800  3404   3419   Idle     Normal   Normal   Normal   100%     2024-07-08 00:23:30  Normal   Normal  27500    Normal  
2     51192  0      28400  26400  27000  3405   3418   Idle     Normal   Normal   Normal   100%     2024-07-08 00:23:29  Normal   Normal  27700    Normal  
3     51226  0      30000  26000  27000  3400   3418   Idle     Normal   Normal   Normal   100%     2024-07-08 00:23:29  Normal   Normal   -        -       
4     51201  0      28200  25600  26000  3393   3416   Idle     Normal   Normal   Normal   100%     2024-07-08 00:23:29  Normal   Normal  27300    Normal  
5     51198  0      28400  25500  25900  3407   3415   Idle     Normal   Normal   Normal   100%     2024-07-08 00:23:30  Normal   Normal  27000    Normal  
6     51194  0      27800  24900  25000  3395   3416   Idle     Normal   Normal   Normal   100%     2024-07-08 00:23:29  Normal   Normal  26300    Normal  
7     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
8     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
9     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
10    -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
11    -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
12    -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
13    -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
14    -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
15    -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
16    -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
Command completed successfully"""
    assert pwr_resp == expected_result

def test_response_extraction_pwr_2(pwr_raw_resps):
    pwr_resp = extract_response_from_raw(pwr_raw_resps[2])
    expected_result = """Power Volt   Curr   Tempr  Tlow   Thigh  Vlow   Vhigh  Base.St  Volt.St  Curr.St  Temp.St  Coulomb  Time                 B.V.St   B.T.St   MosTempr M.T.St  
1     51208  0      28900  26200  26800  3404   3419   Idle     Normal   Normal   Normal   100%     2024-07-08 00:23:30  Normal   Normal  27500    Normal  
2     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -     
3     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -     
4     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -     
5     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -     
6     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -     
7     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
8     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
9     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
10    -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
11    -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
12    -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
13    -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
14    -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
15    -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
16    -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
Command completed successfully"""
    assert pwr_resp == expected_result

def test_response_extraction_bat_1(bat_raw_resps):
    bat_resp = extract_response_from_raw(bat_raw_resps[1])
    expected_result = """Battery  Volt     Curr     Tempr    Base State   Volt. State  Curr. State  Temp. State  SOC          Coulomb      BAL         
0        3416     0        26500    Idle         Normal       Normal       Normal       100%         49560 mAH      N
1        3403     0        26500    Idle         Normal       Normal       Normal       100%         49477 mAH      N
2        3414     0        26500    Idle         Normal       Normal       Normal       100%         49558 mAH      N
3        3413     0        26500    Idle         Normal       Normal       Normal       100%         49557 mAH      N
4        3413     0        26500    Idle         Normal       Normal       Normal       100%         49556 mAH      N
5        3405     0        26800    Idle         Normal       Normal       Normal       100%         49477 mAH      N
6        3412     0        26800    Idle         Normal       Normal       Normal       100%         49548 mAH      N
7        3418     0        26800    Idle         Normal       Normal       Normal       100%         49561 mAH      N
8        3418     0        26800    Idle         Normal       Normal       Normal       100%         49562 mAH      N
9        3415     0        26800    Idle         Normal       Normal       Normal       100%         49556 mAH      N
10       3413     0        26200    Idle         Normal       Normal       Normal       100%         49555 mAH      N
11       3411     0        26200    Idle         Normal       Normal       Normal       100%         49555 mAH      N
12       3415     0        26200    Idle         Normal       Normal       Normal       100%         49556 mAH      N
13       3414     0        26200    Idle         Normal       Normal       Normal       100%         49557 mAH      N
14       3413     0        26200    Idle         Normal       Normal       Normal       100%         49555 mAH      N
Command completed successfully"""
    assert bat_resp == expected_result

def test_response_extraction_bat_2(bat_raw_resps):
    bat_resp = extract_response_from_raw(bat_raw_resps[2])
    expected_result = """Battery  Volt     Curr     Tempr    Base State   Volt. State  Curr. State  Temp. State  SOC          Coulomb      BAL         
0        3414     0        26000    Idle         Normal       Normal       Normal       100%         49788 mAH      N
1        3414     0        26000    Idle         Normal       Normal       Normal       100%         49788 mAH      N
2        3414     0        26000    Idle         Normal       Normal       Normal       100%         49788 mAH      N
3        3415     0        26000    Idle         Normal       Normal       Normal       100%         49788 mAH      N
4        3414     0        26000    Idle         Normal       Normal       Normal       100%         49788 mAH      N
5        3413     0        25900    Idle         Normal       Normal       Normal       100%         49787 mAH      N
6        3415     0        25900    Idle         Normal       Normal       Normal       100%         49788 mAH      N
7        3414     0        25900    Idle         Normal       Normal       Normal       100%         49788 mAH      N
8        3414     0        25900    Idle         Normal       Normal       Normal       100%         49788 mAH      N
9        3414     0        25900    Idle         Normal       Normal       Normal       100%         49788 mAH      N
10       3414     0        25600    Idle         Normal       Normal       Normal       100%         49788 mAH      N
11       3414     0        25600    Idle         Normal       Normal       Normal       100%         49788 mAH      N
12       3414     0        25600    Idle         Normal       Normal       Normal       100%         49788 mAH      N
13       3415     0        25600    Idle         Normal       Normal       Normal       100%         49788 mAH      N
14       3393     0        25600    Idle         Normal       Normal       Normal       100%         49688 mAH      N
Command completed successfully"""
    assert bat_resp == expected_result

def test_response_extraction_bat_3(bat_raw_resps):
    bat_resp = extract_response_from_raw(bat_raw_resps[3])
    expected_result = """Invalid command or fail to excute.
Usage:
Battery data show - bat [pwr][index]"""
    assert bat_resp == expected_result

def test_response_extraction_bat_4(bat_raw_resps):
    bat_resp = extract_response_from_raw(bat_raw_resps[4])
    expected_result = """Unknown command 'bit' - try 'help'"""
    assert bat_resp == expected_result

def test_response_extraction_bat_5(bat_raw_resps):
    with pytest.raises(PylontechInvalidResponseError):
        extract_response_from_raw(bat_raw_resps[5])

