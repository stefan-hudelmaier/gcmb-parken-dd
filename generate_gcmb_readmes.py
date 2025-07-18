import os
import json
from api_client import ApiClient

gcmb_dir = os.path.join(os.path.dirname(__file__), 'gcmb')

CITY_README_TEMPLATE = '''
# {city}

## Free parking spaces per Lot

<WorldMap>
{lot_markers}
</WorldMap>

## Lots
{lots}
'''

LOT_TEMPLATE = '''
### {lot_name}

* Total parking spaces: <Value topic="{base_topic}/{city}/{lot_id}/total"/>
* Free parking spaces: <Value topic="{base_topic}/{city}/{lot_id}/free"/>
'''

TOP_LEVEL_README_TEMPLATE = '''
# Parken DD

<WorldMap>
{city_markers}
</WorldMap>

List of cities:
{cities}
'''

CITY_LIST_ITEM_TEMPLATE = '''
## {city}

[Details](./{city})

* Total parking spaces: <Value topic="{base_topic}/{city}/total"/>
* Free parking spaces: <Value topic="{base_topic}/{city}/free"/>
'''

MAP_MARKER_TEMPLATE = '  <Marker lat="{lat}" lon="{lon}" labelTopic="{label_topic}" linkTopic="{link_topic}">{city}</Marker>'
LOT_MARKER_TEMPLATE = '  <Marker lat="{lat}" lon="{lon}" labelTopic="{label_topic}" linkTopic="{link_topic}">{lot}</Marker>'

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
    # cities = {k: v for k, v in cities.items() if k == 'Zuerich'}
    cities_md = []
    city_markers_md = []
    for city_key, city_info in cities.items():
        print(f"Processing {city_key}")
        city_dir = os.path.join(gcmb_dir, city_key)
        ensure_dir(city_dir)
        lots = api_client.get_city_lots(city_key)
        lat = city_info.get('coords').get('lat')
        lon = city_info.get('coords').get('lng')
        lots_md = []
        lot_markers_md = []
        for lot in lots:
            lot_id = lot.get('id', '')
            lot_name = lot.get('name', lot_id)
            lots_md.append(LOT_TEMPLATE.format(
                lot_name=lot_name,
                base_topic=base_topic, 
                city=city_key, 
                lot_id=lot_id
            ))
            coords = lot.get('coords')
            if coords is None:
                continue
            lat, lon = lot.get('coords', {}).get('lat'), lot.get('coords', {}).get('lng')
            if lat is None or lon is None:
                continue
            lot_markers_md.append(MAP_MARKER_TEMPLATE.format(
                lat=lat,
                lon=lon,
                label_topic=f"{base_topic}/{city_key}/{lot_id}/free",
                link_topic=f"{base_topic}/{city_key}/{lot_id}"
            ))
        city_md = CITY_README_TEMPLATE.format(city=city_key, lots='\n'.join(lots_md), lot_markers='\n'.join(lot_markers_md))
        with open(os.path.join(city_dir, 'README.md'), 'w', encoding='utf-8') as f:
            f.write(city_md)
        cities_md.append(CITY_LIST_ITEM_TEMPLATE.format(
            city=city_key,
            base_topic=base_topic))
        city_markers_md.append(MAP_MARKER_TEMPLATE.format(
            lat=lat,
            lon=lon,
            label_topic=f"{base_topic}/{city_key}/free",
            link_topic=f"{base_topic}/{city_key}"
        ))

    with open(os.path.join(gcmb_dir, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(TOP_LEVEL_README_TEMPLATE.format(cities='\n'.join(cities_md), city_markers='\n'.join(city_markers_md)))

if __name__ == '__main__':
    generate_gcmb_readmes()
