from dotenv import load_dotenv
load_dotenv()

import os
import logging
import sys
import time
from gcmb_publisher import MqttPublisher

log_level = os.environ.get('LOG_LEVEL', 'INFO')
print("Using log level", log_level)

logger = logging.getLogger()
logger.setLevel(log_level)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def main():
    mqtt_publisher = MqttPublisher(enable_watchdog=True)
    while True:
        mqtt_publisher.send_msg('hello', 'parken-dd/parken-dd/sometopic', retain=False)
        time.sleep(5)


if __name__ == '__main__':
    main()
