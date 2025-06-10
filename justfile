run:
    uv run python main.py

test:
    uv run python -m pytest test_main.py -v

generate-gcmb-readmes:
    uv run python generate_gcmb_readmes.py

test-coverage:
    coverage run -m unittest test_main.py
    coverage report -m
