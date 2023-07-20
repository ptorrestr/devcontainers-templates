#!/bin/bash
cd $(dirname "$0")
source test-utils.sh

# Template specific tests
check "dbt" type -p dbt > /dev/null

# Report result
reportResults