from udsoncan.services import *

@classmethod
def _Rewrite_make_request(cls):
    from udsoncan import Request
    return Request(service=cls, subfunction=0x02)

def PatchMessageFormat():
    TesterPresent.make_request = _Rewrite_make_request