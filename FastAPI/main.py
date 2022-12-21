from fastapi import FastAPI
from backend.pdu_outlets import SnmpHandler

app = FastAPI()


@app.get('/')
def read_root():
    return {"Hello": "World"}


@app.post('/pdu/{pdu_id}:{port}/{outlet_num}/{value}')
async def pdu_control(pdu_id: str, port: int, outlet_num: str, value: int):
    snmp_handler = SnmpHandler(pdu_id, port)
    snmp_handler.set(outlet_num, value)
    return value
