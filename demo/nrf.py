import time


class Nrf:
    def __init__(self, radio):
        self.radio = radio

    def read_message(self):
        if self.radio.available():
            while self.radio.available():
                len = self.radio.getDynamicPayloadSize()
                receive_payload = self.radio.read(len)

                return receive_payload.decode('utf-8')

    def send_message(self, message):
        self.radio.stopListening()
        ok = self.radio.write(message)
        self.radio.startListening()

        return ok

    def wait_for_response(self):
        millis = lambda: int(round(time.time() * 1000))
        started_waiting_at = millis()
        timeout = False

        while (not self.radio.available()) and (not timeout):
            if (millis() - started_waiting_at) > 500:
                timeout = True

        # Describe the results
        if timeout:
            print('failed, response timed out.')
        else:
            # Grab the response, compare, and send to debugging spew
            len = self.radio.getDynamicPayloadSize()
            receive_payload = self.radio.read(len)

            return receive_payload
