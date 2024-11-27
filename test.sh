#!/bin/bash

echo "Ajetaan testit: robot, unittest, pylint"

bash run_robot_tests.sh

echo "Ajetaan pylint:"
poetry run pylint src

echo "Ajetaan yksikkötestit:"
poetry run pytest
