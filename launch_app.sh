#!/bin/bash
# LuminaLane AI Launcher
# This script uses relative paths to ensure portability.

BASEDIR=$(dirname "$0")
source "$BASEDIR/venv/bin/activate"
python "$BASEDIR/gui_app.py"
