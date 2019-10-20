# AQUA ENGINE ECU HACK TOOL
Tool created to hack Aqua ECM (Engine Control Module).  

If you have any comments or questions please do it on Twitter DM (@shutingrz).  
https://twitter.com/shutingrz

## TargetECU
- Brand: TOYOTA AQUA (PriusC)
- Model number: NHP-10
- Year: 2013
- ECM model number: 89661-52U90
- CalibrationID : 352N4100 / A4701000


## INSTALL
### library
```
$ git clone https://github.com/shutingrz/aqua-engine-ecu-hack
$ cd aqua-engine-ecu-hack
$ pip3 install -r ./requirements.txt
```

### config
Rename config.py.sample to config.py
```
$ cp config.py.sample config.py
```

And open config.py and fix 'security_algo_params'.
```
$ vi config.py
```

Please refer to the URL and change '\xXX\xXX\xXX\xXX' to the PriusEffectiveKey value.  
https://github.com/andrewraharjo/CAN-Bus-Hack_Prius_Focus/blob/master/ecomcat_api/config.py  
> 'security_algo_params'		: dict(xorkey=b'\xXX\xXX\xXX\xXX')

## Tools

### get_seed.py
Get seed of SecurityAccess and print console. (default: 10000 times)

### brute_key_xor.py
Crack to SecurityAccess (Only 4bytes XOR).

### check_key_timing.py
Sample of timing attack to SecurityAccess.

### brute_targetdata.py
Crack to TargetData of target calibration.