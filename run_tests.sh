#!/bin/bash

# Define the directories containing the test files
PROJECT_DIR=$(dirname "$(readlink -f "$0")")
TEST_DIR="$PROJECT_DIR/tests/"

TEST_DIRS="measurement_instruments structure transducer subsystem energy_system"

# Run the tests and generate coverage report
for dir in $TEST_DIRS; do
  echo "Running tests in $TEST_DIR$dir..."
  coverage run -m unittest discover -s "$TEST_DIR$dir" -p "test_*.py"
done

# Generate coverage report
coverage report --omit="*/tests/*"
