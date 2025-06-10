from dotenv import load_dotenv
load_dotenv()

import os
import logging
import sys
import time
from gcmb_publisher import MqttPublisher
from api_client import ApiClient
import json

log_level = os.environ.get('LOG_LEVEL', 'INFO')
print("Using log level", log_level)

logger = logging.getLogger()
logger.setLevel(log_level)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class Adapter:
    def __init__(self, base_topic, mqtt_publisher, api_client, logger=logger):
        self.base_topic = base_topic
        self.mqtt_publisher = mqtt_publisher
        self.api_client = api_client
        self.logger = logger

    def run_once(self):
        self.logger.debug("Fetching cities from API client...")
        cities = self.api_client.get_cities()
        global_free = 0
        global_total = 0
        global_lots = 0
        for city_key, city_info in cities.items():
            city_name = city_info.get("name", city_key)
            lots = self.api_client.get_city_lots(city_key)
            city_free = 0
            city_total = 0
            for lot in lots:
                lot_id = lot.get("id")
                if not lot_id:
                    continue
                free = lot.get("free")
                total = lot.get("total")
                state = lot.get("state")
                # Publish per-lot topics
                if free is not None:
                    topic = f"{self.base_topic}/{city_key}/{lot_id}/free"
                    self.mqtt_publisher.send_msg(str(free), topic, retain=False)
                    self.logger.debug(f"Published {free} to {topic}")
                    city_free += free if isinstance(free, int) else 0
                if total is not None:
                    topic = f"{self.base_topic}/{city_key}/{lot_id}/total"
                    self.mqtt_publisher.send_msg(str(total), topic, retain=False)
                    self.logger.debug(f"Published {total} to {topic}")
                    city_total += total if isinstance(total, int) else 0
                if state is not None:
                    topic = f"{self.base_topic}/{city_key}/{lot_id}/state"
                    self.mqtt_publisher.send_msg(str(state), topic, retain=False)
                    self.logger.debug(f"Published {state} to {topic}")
                # Publish original JSON per lot
                topic = f"{self.base_topic}/{city_key}/{lot_id}"
                self.mqtt_publisher.send_msg(json.dumps(lot, ensure_ascii=False), topic, retain=False)
                self.logger.debug(f"Published lot JSON to {topic}")
            # Publish city aggregates
            topic_free = f"{self.base_topic}/{city_key}/free"
            topic_total = f"{self.base_topic}/{city_key}/total"
            self.mqtt_publisher.send_msg(str(city_free), topic_free, retain=False)
            self.mqtt_publisher.send_msg(str(city_total), topic_total, retain=False)
            self.logger.debug(f"Published city aggregates: free={city_free}, total={city_total} for {city_key}")
            global_free += city_free
            global_total += city_total
            global_lots += len(lots)
        # Publish global aggregates
        topic_global_free = f"{self.base_topic}/stats/free"
        topic_global_total = f"{self.base_topic}/stats/total"
        topic_global_lots = f"{self.base_topic}/stats/lots"
        self.mqtt_publisher.send_msg(str(global_free), topic_global_free, retain=False)
        self.mqtt_publisher.send_msg(str(global_total), topic_global_total, retain=False)
        self.mqtt_publisher.send_msg(str(global_lots), topic_global_lots, retain=False)
        self.logger.debug(f"Published global stats: free={global_free}, total={global_total}, lots={global_lots}")

def main():
    GCMB_ORG = os.environ.get('GCMB_ORG', 'parken-dd')
    GCMB_PROJECT = os.environ.get('GCMB_PROJECT', 'parken-dd')
    BASE_TOPIC = f"{GCMB_ORG}/{GCMB_PROJECT}"
    mqtt_publisher = MqttPublisher(enable_watchdog=True)
    api_client = ApiClient()
    adapter = Adapter(BASE_TOPIC, mqtt_publisher, api_client, logger=logger)
    while True:
        try:
            adapter.run_once()
        except Exception as e:
            logger.error(f"Error in adapter loop: {e}")
        time.sleep(300)  # 5 minutes

if __name__ == '__main__':
    main()
