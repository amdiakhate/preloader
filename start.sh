#!/bin/bash

# Create the healthy file required for Kubernetes probes
touch /tmp/healthy

# Execute the Python script
python preloader.py
