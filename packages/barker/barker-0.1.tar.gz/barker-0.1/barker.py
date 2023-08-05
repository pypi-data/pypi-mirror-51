import hmac
import requests
import time
__version__ = "0.1"


class Webhook():
    def __init__(self, url=None, data=None, timeout=5, key=None):
        self.url = url
        self.data = data
        self.timeout = timeout
        self.key = key if key is not None else 'BARKER'
        self.headers = {}
        self.response = None

    def _calculate_hash(self):
        """ Calculate hash to include as a header. """
        self.headers['BARKER_TIMESTAMP'] = str(time.time())
        hash = hmac.new(bytes(self.key, 'utf-8'))
        hash.update(bytes(";".join((self.headers['BARKER_TIMESTAMP'], self.data)), 'utf-8'))
        self.headers['BARKER_SIGNATURE'] = hash.hexdigest()

    def send(self):
        self._calculate_hash()
        self.response = requests.post(self.url,
                                      headers=self.headers,
                                      data=self.data,
                                      timeout=self.timeout)

        return self.response

    def verify_hash(self):
        """ Verify the data matches the hash provided """
        hash = hmac.new(bytes(self.key, 'utf-8'))
        hash.update(bytes(";".join((self.headers['BARKER_TIMESTAMP'], self.data)), 'utf-8'))
        return hmac.compare_digest(self.headers['BARKER_SIGNATURE'], hash.hexdigest())
