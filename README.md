# Parken DD Adapter

This project provides a Python-based adapter for publishing real-time parking data from various European 
cities. The adapter fetches open parking data (such as available spaces, lot status, and metadata) 
from the excellent[Parken DD](https://parkendd.de) project and publishes it to [gcmb.io](https://gcmb.io/parken-dd/parken-dd).

## Features

* Fetches live parking data from multiple European cities via Parken DD
* Publishes data to gcmb.io

## Setup

1. Clone this repository.
2. Copy `.env.template` to `.env` and configure your environment variables (API keys, endpoints, etc).
3. Install dependencies via `uv sync`.

## Usage

(using [just(https://github.com/casey/just)])

* Run the adapter: `just run`
* Run tests: `just tests`

## License

This project is provided under the MIT License.

## Acknowledgements

- Data sourced from the [Parken DD project](https://parkendd.de)
- Adapter developed for integration with [gcmb.io](https://gcmb.io)
