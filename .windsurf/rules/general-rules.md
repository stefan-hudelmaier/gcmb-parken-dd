---
trigger: always_on
---

# Instructions

* The build system is uv. Add new packages using uv add.
* The main entry point is main.py
* The project is hosted on GitHub, Docker images are published for every push to main
* The .env.template file for environment variables must be kept up to date.
* Env variables are defined in the .env file
* The following dependency must be used:
  * For publishing via MQTT: gcmb-publisher
  * HTTP client: requests
  * Unit tests: pytest
* This project is an adapter between an API and MQTT/GCMB. The specifics of the API should always
  be handled in a file called `api_client.py` containing a class called `ApiClient`. 
* There are two entrypoints. The default way is to start the endlessly running adapter, via `main.py`
  It will fetch data from the API and publish it via MQTT. The second way is to create the 
  topic-specific README files in the `gcmb` subfolder. This is done via `generate_gcmb_readmes.py`.
* The base MQTT topic is determined by environment variables: ${GCMB_ORG}/${GCMB_PROJECT}.
* topic-specific readmes in Markdown format are stored in the `gcmb` subfolder. Examples:
  * The readme for the topic ${GCMB_ORG}/${GCMB_PROJECT} is at `gcmb/README.md`
  * The readme for the topic ${GCMB_ORG}/${GCMB_PROJECT}/sometopic is at `gcmb/sometopic/README.md`
* Project-specific instructions can be found in the file project-instructions.md
* There must be unit tests for the data transformation. The `ApiClient` and the MqttPublisher 
  should be mocked. The tests for this should be done in `test_main.py`. The tests should be along
  the following lines: If this data is returned by the API, this contents gets published on these MQTT topics. 
* Frequent operations should be logged on DEBUG level
* Variables from environment variables should be initialized near the top of files (below imports)
