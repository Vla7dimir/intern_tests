#!/bin/bash
set -e

if [ -d "venv" ]; then
    source venv/bin/activate
fi

pytest
