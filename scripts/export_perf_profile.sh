#!/bin/sh

# Command prefix
EXEC_COMMAND="kubectl"

# Handle difference between docker exec and kubectl exec
DASH_DASH=""

if [ $EXEC_COMMAND = "kubectl" ]; then
    DASH_DASH="--"
fi

# How long to profile
DEFAULT_TIMEOUT="10"

# Get container ID from args
CONTAINER="$1"

if [ -z "$CONTAINER" ]; then
    echo "Must specify container ID. Exiting."
    exit
fi

if [ -z "$2" ]; then
    TIMEOUT="$DEFAULT_TIMEOUT"
else
    TIMEOUT="$2"
fi

echo "Running perf in container $CONTAINER for $TIMEOUT seconds..."

# Run a profile for n seconds
"$EXEC_COMMAND" exec "$CONTAINER" "$DASH_DASH" timeout "$TIMEOUT" ./perf record -a -F 999 -g -p 1 -o perf.data

# Convert with perf script
"$EXEC_COMMAND" exec "$CONTAINER" "$DASH_DASH" ./perf script -i perf.data > profile.txt

echo "Created profile.txt"
