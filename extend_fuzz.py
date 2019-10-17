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
            client.change_session(0x61)   

            client.unlock_security_access(CarConfig.SECURITY_LEVEL)
            
            for cnt in range(0x11, 0xff - 0x11):
                conn.send(b"\x3e\x01")
                payload = conn.wait_frame(timeout=0.1)
                conn.send(cnt.to_bytes(1, "little") + b"\x01")
                payload = conn.wait_frame(timeout=0.1)

        except NegativeResponseException as e:
            print('Server refused our request for service %s with code "%s" (0x%02x)' % (e.response.service.get_name(), e.response.code_name, e.response.code))
        except UnexpectedResponseException as e:
            print('Server sent an invalid payload : %s' % e.response.original_payload)
        except TimeoutException as e:
            pass