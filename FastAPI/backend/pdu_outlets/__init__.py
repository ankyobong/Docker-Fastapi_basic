import logging
from functools import wraps
from easysnmp import Session
from easysnmp import snmp_set, snmp_get, snmp_walk


################################################################################
pdu_path = {
    '1': '.1.3.6.1.4.1.13742.6.4.1.2.1.2.1.1',
    '2': '.1.3.6.1.4.1.13742.6.4.1.2.1.2.1.2',
    '3': '.1.3.6.1.4.1.13742.6.4.1.2.1.2.1.3',
    '4': '.1.3.6.1.4.1.13742.6.4.1.2.1.2.1.4',
    '5': '.1.3.6.1.4.1.13742.6.4.1.2.1.2.1.5',
    '6': '.1.3.6.1.4.1.13742.6.4.1.2.1.2.1.6',
    '7': '.1.3.6.1.4.1.13742.6.4.1.2.1.2.1.7',
    '8': '.1.3.6.1.4.1.13742.6.4.1.2.1.2.1.8',
    '9': '.1.3.6.1.4.1.13742.6.4.1.2.1.2.1.9',
    '10': '.1.3.6.1.4.1.13742.6.4.1.2.1.2.1.10',
    '11': '.1.3.6.1.4.1.13742.6.4.1.2.1.2.1.11',
    '12': '.1.3.6.1.4.1.13742.6.4.1.2.1.2.1.12',
    '13': '.1.3.6.1.4.1.13742.6.4.1.2.1.2.1.13',
    '14': '.1.3.6.1.4.1.13742.6.4.1.2.1.2.1.14',
    '15': '.1.3.6.1.4.1.13742.6.4.1.2.1.2.1.15',
    '16': '.1.3.6.1.4.1.13742.6.4.1.2.1.2.1.16',
    '17': '.1.3.6.1.4.1.13742.6.4.1.2.1.2.1.17',
    '18': '.1.3.6.1.4.1.13742.6.4.1.2.1.2.1.18',
    '19': '.1.3.6.1.4.1.13742.6.4.1.2.1.2.1.19',
    '20': '.1.3.6.1.4.1.13742.6.4.1.2.1.2.1.20',
    '21': '.1.3.6.1.4.1.13742.6.4.1.2.1.2.1.21',
    '22': '.1.3.6.1.4.1.13742.6.4.1.2.1.2.1.22',
    '23': '.1.3.6.1.4.1.13742.6.4.1.2.1.2.1.23',
    '24': '.1.3.6.1.4.1.13742.6.4.1.2.1.2.1.24'
}
pdu_status = '.1.3.6.1.4.1.13742.6.4.1.2.1.2.1.'


################################################################################
class SnmpHandler:
    # ==========================================================================
    def __init__(self, host, port, community_read='public',
                 community_write='private', version=2):
        self.host = host
        self.port = port
        self.address = (host, port)
        self.community_read = community_read
        self.community_write = community_write
        self.version = version

    # ==========================================================================
    def result(self):
        @wraps(self)
        def func(*args, **kwargs):
            try:
                result = self(*args, **kwargs)
                ok, value, message = (True, result, '')
            except Exception as e:
                logging.exception(msg=str(e), exc_info=e)
                ok, value, message = (False, None, str(e))
            if not ok:
                logging.error(f'code: {ok} message: {message}')
            return ok, value, message

        return func

    # ==========================================================================
    @result
    def get(self, items: list):
        result = list()
        for oid in items:
            r = snmp_get(oid, hostname=self.host,
                         community=self.community_read, version=self.version)
            result.append((oid, r.value))
        return result

    # ==========================================================================
    @result
    def bulk(self):
        r = snmp_walk(pdu_status, hostname=self.host,
                      community=self.community_read, version=self.version)
        values = [(f'{v.oid.rpartition(".")[2]}', v.value) for v in r]
        return values

    # ==========================================================================
    @result
    def set(self, oid: str, value, data_type='i'):
        """
        :param oid: 'PDU2-MIB::externalSensorType.1.1'
        :param value: 8
        :param data_type:
        :return:
        """
        s = Session(hostname=self.host,
                    community=self.community_write,
                    version=self.version)
        r = s.set(pdu_path[oid], value, data_type)
        r2 = s.get(pdu_path[oid])
        return r2.value


if __name__ == '__main__':
    s = SnmpHandler('10.0.0.50', 161)
    s.bulk()
    print(s)
