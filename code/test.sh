#!/bin/bash

#python3 -m unittest discover -p "test_*" -v
pytest --cov=lib --cov=new --cov=state --cov=lib_costs --cov=lib_security --cov-report=html --disable-pytest-warnings
firefox-esr htmlcov/index.html