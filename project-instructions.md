This project shall regularly (every 5 minutes) fetch data from parkendd and publish data to MQTT broker.

An example for using the parkendd API can be found here.

Getting all cities can be achieved using https://api.parkendd.de. This is an example response:

{
  "api_version": "1.0",
  "cities": {
    "Aachen": {
      "active_support": false,
      "attribution": null,
      "coords": {
        "lat": 50.774842,
        "lng": 6.083899
      },
      "name": "Aachen",
      "source": "https://www.apag.de/parken-in-aachen",
      "url": "http://www.aachen.de/"
    },
...
    "Zuerich": {
      "active_support": true,
      "attribution": {
        "contributor": "PLS Parkleitsystem Zürich AG",
        "license": "Creative-Commons-Null-Lizenz (CC-0)",
        "url": "http://www.plszh.ch/impressum.jsp"
      },
      "coords": {
        "lat": 47.36667,
        "lng": 8.55
      },
      "name": "Zürich",
      "source": "http://www.pls-zh.ch/plsFeed/rss",
      "url": "https://www.stadt-zuerich.ch/portal/de/index/ogd/daten/parkleitsystem.html"
    }
  },
  "reference": "https://github.com/offenesdresden/ParkAPI",
  "server_version": "0.3.686"
}


This is an example request for a specific city:

curl https://api.parkendd.de/Zuerich

{
    "last_downloaded": "2019-11-18T15:55:02",
    "last_updated": "2019-11-18T15:51:27",
    "lots": [
        {
            "address": "Seilergraben",
            "coords": {
                "lat": 47.376579,
                "lng": 8.544743
            },
            "forecast": false,
            "free": 6,
            "id": "zuerichparkgarageamcentral",
            "lot_type": "",
            "name": "Parkgarage am Central",
            "state": "open",
            "total": 50
        },
        {
            "address": "Otto-Schütz-Weg",
            "coords": {
                "lat": 47.414848,
                "lng": 8.540748
            },
            "forecast": false,
            "free": 131,
            "id": "zuerichparkhausaccu",
            "lot_type": "Parkhaus",
            "name": "Accu",
            "state": "open",
            "total": 194
        },
        {
            "address": "Badenerstrasse 380",
            "coords": {
                "lat": 47.379458,
                "lng": 8.509675
            },
            "forecast": false,
            "free": 62,
            "id": "zuerichparkhausalbisriederplatz",
            "lot_type": "Parkhaus",
            "name": "Albisriederplatz",
            "state": "open",
            "total": 66
        },
        ...
    ]
}

The following messages shall be published:

topic: parkendd/parkendd/{city}/{lot_id}/free: Scalar value from property "free"
topic: parkendd/parkendd/{city}/{lot_id}/total: Scalar value from property "total"
topic: parkendd/parkendd/{city}/{lot_id}/state: Scalar value from property "state"
topic: parkendd/parkendd/{city}/{lot_id}: The original JSON per lot
topic: parkendd/parkendd/{city}/free: The aggregated free parking spaces in the city
topic: parkendd/parkendd/{city}/total: The aggregated total parking spaces in the city

topic-specific README.md are created:

topic: parkendd/parkendd: Contents:

```
# Parken DD

List of cities:

{Per city:}

## {city}

[Details](./{city})

Total parking spaces: <Value topic="parkendd/parkendd/{city}/total" />
Free parking spaces: <Value topic="parkendd/parkendd/{city}/free" />
```

topic: parkendd/parkendd/{city}: Contents:

```

# {city}

## Lots

{per lot:}

### {lot name}

Total parking spaces: <Value topic="parkendd/parkendd/{city}/{lot_id}/total"/>
Free parking spaces: <Value topic="parkendd/parkendd/{city}/{lot_id}/free"/>

```
