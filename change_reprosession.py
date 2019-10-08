#!/usr/bin/python3

import time
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

isotp_socket = isotp.socket()
isotp_socket.set_opts(txpad=CarConfig.TXPADSIZE, rxpad=CarConfig.RXPADSIZE)

aqua_patch.PatchMessageFormat()

if __name__ == '__main__':

    conn = IsoTPSocketConnection('can0', rxid=CarConfig.RXID, txid=CarConfig.TXID, tpsock=isotp_socket)

    with Client(conn, request_timeout=2, config=CarConfig.car_client_config) as client:
        try:
            client.change_session(DiagnosticSessionControl.Session.defaultSession)
            client.unlock_security_access(CarConfig.SECURITY_LEVEL)
            client.change_session(DiagnosticSessionControl.Session.programmingSession)   
            
                
            
        except NegativeResponseException as e:
            print('Server refused our request for service %s with code "%s" (0x%02x)' % (e.response.service.get_name(), e.response.code_name, e.response.code))
        except UnexpectedResponseException as e:
            print('Server sent an invalid payload : %s' % e.response.original_payload)
        except TimeoutException as e:
            pass


