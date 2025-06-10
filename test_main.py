import pytest
from unittest.mock import MagicMock
from main import Adapter

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
    api_client = MagicMock()
    api_client.get_cities.return_value = cities_data['cities']
    api_client.get_city_lots.return_value = lots_data
    mqtt_publisher = MagicMock()
    base_topic = 'testorg/testproj'
    adapter = Adapter(base_topic, mqtt_publisher, api_client)

    adapter.run_once()

    calls = mqtt_publisher.send_msg.call_args_list
    # Check topic and payloads for scalar values
    topics_payloads = [(c[0][1], c[0][0]) for c in calls if c[0][1].endswith(('free','total','state'))]
    # Check JSON lot messages
    json_lot_calls = [c for c in calls if c[0][1].endswith('/lot1') or c[0][1].endswith('/lot2')]
    assert any('lot1' in c[0][1] for c in json_lot_calls)
    assert any('lot2' in c[0][1] for c in json_lot_calls)
    # Check aggregates
    assert (f'{base_topic}/TestCity/free', '7') in topics_payloads
    assert (f'{base_topic}/TestCity/total', '15') in topics_payloads