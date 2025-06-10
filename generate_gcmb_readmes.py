import os
import json
from api_client import ApiClient

gcmb_dir = os.path.join(os.path.dirname(__file__), 'gcmb')

CITY_README_TEMPLATE = '''# {city}\n\n## Lots\n\n{lots}\n'''
LOT_TEMPLATE = '''### {lot_name}\n\n* Total parking spaces: <Value topic="{base_topic}/{city}/{lot_id}/total"/>\n* Free parking spaces: <Value topic="{base_topic}/{city}/{lot_id}/free"/>\n'''
TOPIC_README_TEMPLATE = '''# Parken DD\n\nList of cities:\n\n{cities}\n'''
CITY_LINK_TEMPLATE = '## {city}\n\n[Details](./{city})\n\n* Total parking spaces: <Value topic="{base_topic}/{city}/total"/>\n* Free parking spaces: <Value topic="{base_topic}/{city}/free"/>\n'

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def generate_gcmb_readmes(base_topic=None):
    api_client = ApiClient()
    if base_topic is None:
        org = os.environ.get('GCMB_ORG', 'parken-dd')
        proj = os.environ.get('GCMB_PROJECT', 'parken-dd')
        base_topic = f"{org}/{proj}"
    cities = api_client.get_cities()
    cities_md = []
    for city_key, city_info in cities.items():
        city_dir = os.path.join(gcmb_dir, city_key)
        ensure_dir(city_dir)
        lots = api_client.get_city_lots(city_key)
        lots_md = []
        for lot in lots:
            lots_md.append(LOT_TEMPLATE.format(
                lot_name=lot.get('name', lot.get('id', '')), 
                base_topic=base_topic, 
                city=city_key, 
                lot_id=lot.get('id', '')
            ))
        city_md = CITY_README_TEMPLATE.format(city=city_key, lots='\n'.join(lots_md))
        with open(os.path.join(city_dir, 'README.md'), 'w', encoding='utf-8') as f:
            f.write(city_md)
        cities_md.append(CITY_LINK_TEMPLATE.format(
            city=city_key, base_topic=base_topic
        ))
    with open(os.path.join(gcmb_dir, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(TOPIC_README_TEMPLATE.format(cities='\n'.join(cities_md)))

if __name__ == '__main__':
    generate_gcmb_readmes()
