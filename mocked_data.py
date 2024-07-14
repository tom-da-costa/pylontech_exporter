pwr_raw_txt_1 = """pwr
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
Command completed successfully"""

pwr_raw_txt_1_expected_result = [
  {'Power': '1', 'Volt': '51208', 'Curr': '0', 'Tempr': '28900', 'Tlow': '26200', 'Thigh': '26800', 'Vlow': '3404', 'Vhigh': '3419', 'Base.St': 'Idle', 'Volt.St': 'Normal', 'Curr.St': 'Normal', 'Temp.St': 'Normal', 'Coulomb': '100%', 'Time': '2024-07-08 00:23:30', 'B.V.St': 'Normal', 'B.T.St': 'Normal', 'MosTempr': '27500', 'M.T.St': 'Normal'},
  {'Power': '2', 'Volt': '51192', 'Curr': '0', 'Tempr': '28400', 'Tlow': '26400', 'Thigh': '27000', 'Vlow': '3405', 'Vhigh': '3418', 'Base.St': 'Idle', 'Volt.St': 'Normal', 'Curr.St': 'Normal', 'Temp.St': 'Normal', 'Coulomb': '100%', 'Time': '2024-07-08 00:23:29', 'B.V.St': 'Normal', 'B.T.St': 'Normal', 'MosTempr': '27700', 'M.T.St': 'Normal'},
  {'Power': '3', 'Volt': '51226', 'Curr': '0', 'Tempr': '30000', 'Tlow': '26000', 'Thigh': '27000', 'Vlow': '3400', 'Vhigh': '3418', 'Base.St': 'Idle', 'Volt.St': 'Normal', 'Curr.St': 'Normal', 'Temp.St': 'Normal', 'Coulomb': '100%', 'Time': '2024-07-08 00:23:29', 'B.V.St': 'Normal', 'B.T.St': 'Normal', 'MosTempr': '-', 'M.T.St': '-'},
  {'Power': '4', 'Volt': '51201', 'Curr': '0', 'Tempr': '28200', 'Tlow': '25600', 'Thigh': '26000', 'Vlow': '3393', 'Vhigh': '3416', 'Base.St': 'Idle', 'Volt.St': 'Normal', 'Curr.St': 'Normal', 'Temp.St': 'Normal', 'Coulomb': '100%', 'Time': '2024-07-08 00:23:29', 'B.V.St': 'Normal', 'B.T.St': 'Normal', 'MosTempr': '27300', 'M.T.St': 'Normal'},
  {'Power': '5', 'Volt': '51198', 'Curr': '0', 'Tempr': '28400', 'Tlow': '25500', 'Thigh': '25900', 'Vlow': '3407', 'Vhigh': '3415', 'Base.St': 'Idle', 'Volt.St': 'Normal', 'Curr.St': 'Normal', 'Temp.St': 'Normal', 'Coulomb': '100%', 'Time': '2024-07-08 00:23:30', 'B.V.St': 'Normal', 'B.T.St': 'Normal', 'MosTempr': '27000', 'M.T.St': 'Normal'},
  {'Power': '6', 'Volt': '51194', 'Curr': '0', 'Tempr': '27800', 'Tlow': '24900', 'Thigh': '25000', 'Vlow': '3395', 'Vhigh': '3416', 'Base.St': 'Idle', 'Volt.St': 'Normal', 'Curr.St': 'Normal', 'Temp.St': 'Normal', 'Coulomb': '100%', 'Time': '2024-07-08 00:23:29', 'B.V.St': 'Normal', 'B.T.St': 'Normal', 'MosTempr': '26300', 'M.T.St': 'Normal'}
]

pwr_raw_txt_2 = """pwr
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
Command completed successfully"""

pwr_raw_txt_2_expected_result = [
      {
        'Power': '1',
        'Volt': '51208',
        'Curr': '0',
        'Tempr': '28900',
        'Tlow': '26200',
        'Thigh': '26800',
        'Vlow': '3404',
        'Vhigh': '3419',
        'Base.St': 'Idle',
        'Volt.St': 'Normal',
        'Curr.St': 'Normal',
        'Temp.St': 'Normal',
        'Coulomb': '100%',
        'Time':'2024-07-08 00:23:30',
        'B.V.St': 'Normal',
        'B.T.St': 'Normal',
        'MosTempr': '27500',
        'M.T.St': 'Normal'
      }
    ]

pwr_raw_txt_3 = "pwr\n@\nUnknown command 'pwr' - try 'help'"

pwr_raw_txt_4 = "pwr\n@\nPower"


bat_raw_txt_1 = """bat 1
@
Battery  Volt     Curr     Tempr    Base State   Volt. State  Curr. State  Temp. State  SOC          Coulomb      BAL         
0        3416     0        26500    Idle         Normal       Normal       Normal       100%         49560 mAH      N
1        3403     0        26500    Idle         Normal       Normal       Normal       100%         49477 mAH      N
2        3414     0        26500    Idle         Normal       Normal       Normal       100%         49558 mAH      N
3        3413     0        26500    Idle         Normal       Normal       Normal       100 %         49557 mAH      N
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

bat_raw_txt_1_expected_result = ["TODO"]

bat_raw_txt_2 = """bat 4
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
Command completed successfully"""

bat_raw_txt_2_expected_result = ["TODO"]

bat_raw_txt_3 = """bat 20 
@
Invalid command or fail to excute.
Usage:
Battery data show - bat [pwr][index]"""

bat_raw_txt_4 = "bit 1\n@\nUnknown command 'bit' - try 'help'"

bat_raw_txt_5 = "bat addr\n@\nBattery"
