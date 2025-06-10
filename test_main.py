import pytest
from main import Adapter
from utils.mock_mqtt_publisher import MockMqttPublisher


@pytest.fixture
def sample_api_data():
    return {
        'cities': {
            'TestCity': {'name': 'TestCity'}
        }
    }, [
        {
            'id': 'lot1',
            'free': 5,
            'total': 10,
            'state': 'open',
            'name': 'Lot 1'
        },
        {
            'id': 'lot2',
            'free': 2,
            'total': 5,
            'state': 'closed',
            'name': 'Lot 2'
        }
    ]

def test_publish_topics_correctly(sample_api_data):
    cities_data, lots_data = sample_api_data
    api_client = type('MockApiClient', (), {})()
    api_client.get_cities = lambda: cities_data['cities']
    api_client.get_city_lots = lambda city_key: lots_data
    mqtt_publisher = MockMqttPublisher()
    base_topic = 'testorg/testproj'
    adapter = Adapter(base_topic, mqtt_publisher, api_client)

    adapter.run_once()

    # Check per-lot topics
    assert mqtt_publisher.get_payloads_by_topic(f'{base_topic}/TestCity/lot1/free') == ['5']
    assert mqtt_publisher.get_payloads_by_topic(f'{base_topic}/TestCity/lot1/total') == ['10']
    assert mqtt_publisher.get_payloads_by_topic(f'{base_topic}/TestCity/lot1/state') == ['open']
    assert mqtt_publisher.get_payloads_by_topic(f'{base_topic}/TestCity/lot2/free') == ['2']
    assert mqtt_publisher.get_payloads_by_topic(f'{base_topic}/TestCity/lot2/total') == ['5']
    assert mqtt_publisher.get_payloads_by_topic(f'{base_topic}/TestCity/lot2/state') == ['closed']
    # Check aggregates
    assert mqtt_publisher.get_payloads_by_topic(f'{base_topic}/TestCity/free') == ['7']
    assert mqtt_publisher.get_payloads_by_topic(f'{base_topic}/TestCity/total') == ['15']
    # Check lot JSON messages
    lot1_msgs = mqtt_publisher.get_messages_by_topic(f'{base_topic}/TestCity/lot1')
    lot2_msgs = mqtt_publisher.get_messages_by_topic(f'{base_topic}/TestCity/lot2')
    assert len(lot1_msgs) == 1 and len(lot2_msgs) == 1
    assert 'free' in lot1_msgs[0]['payload'] and 'free' in lot2_msgs[0]['payload']


def test_publish_global_stats(sample_api_data):
    cities_data, lots_data = sample_api_data
    api_client = type('MockApiClient', (), {})()
    api_client.get_cities = lambda: cities_data['cities']
    api_client.get_city_lots = lambda city_key: lots_data
    mqtt_publisher = MockMqttPublisher()
    base_topic = 'testorg/testproj'
    adapter = Adapter(base_topic, mqtt_publisher, api_client)

    adapter.run_once()

    # Global stats should be sum of all city stats (in this test, only one city)
    assert mqtt_publisher.get_payloads_by_topic(f'{base_topic}/stats/free') == ['7']
    assert mqtt_publisher.get_payloads_by_topic(f'{base_topic}/stats/total') == ['15']
    assert mqtt_publisher.get_payloads_by_topic(f'{base_topic}/stats/lots') == ['2']