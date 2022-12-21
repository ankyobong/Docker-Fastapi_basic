import os
import yaml
import time
from fastapi import FastAPI
from pdu_outlets import SnmpHandler


_DIR = os.path.abspath(os.path.dirname(__file__))
ip_info = os.path.join(_DIR, 'pdu_outlets', 'ip_info.yaml')
with open(ip_info) as f:
    config = yaml.safe_load(f)

app = FastAPI()


@app.get('/pdu/{rackid}/{path}')
def pdu_status(rackid: str, path: int):
    snmp_handler = SnmpHandler(config[rackid][path], 161)
    result = snmp_handler.bulk()
    return result


@app.post('/pdu/{rackid}/{path}/{outlet_num}/{value}')
async def pdu_control(rackid: str, path: int, outlet_num: str, value: int):
    snmp_handler = SnmpHandler(config[rackid][path], 161)
    if value == 1:
        time.sleep(0.2)
    result = snmp_handler.set(outlet_num, value)
    return result
