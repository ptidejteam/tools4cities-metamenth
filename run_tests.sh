#!/bin/bash

# Define the directories containing the test files
PROJECT_DIR=$(dirname "$(readlink -f "$0")")
TEST_DIR="$PROJECT_DIR/tests/"

TEST_DIRS="energy_system measurement_instruments structure transducer subsystem visitors"

# Initialize a variable to track the overall exit status
OVERALL_EXIT_CODE=0

# Run the tests and generate coverage report
for dir in $TEST_DIRS; do
  echo "Running tests in $TEST_DIR$dir..."
  coverage run -m unittest discover -s "$TEST_DIR$dir" -p "test_*.py"

  # Capture the exit status of the current test run
  TEST_EXIT_CODE=$?

  # Check if the test run failed
  if [ $TEST_EXIT_CODE -ne 0 ]; then
    echo "Tests in $TEST_DIR$dir failed with exit code $TEST_EXIT_CODE"
    # Update the overall exit status
    OVERALL_EXIT_CODE=$TEST_EXIT_CODE
  fi
done

# Exit with the overall exit status
exit $OVERALL_EXIT_CODE


# Generate coverage report
# coverage report --omit="*/tests/*"
