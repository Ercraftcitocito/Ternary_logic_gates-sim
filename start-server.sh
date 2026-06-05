#!/bin/bash

# Start the Ternary Logic Gate Simulator on Linux

echo ""
echo "============================================"
echo "   Ternary Logic Gate Simulator"
echo "============================================"
echo ""
echo "Starting server..."
echo ""
echo "Open your browser to: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Try python3 first, then python
if command -v python3 &> /dev/null; then
    python3 -m http.server 8000
elif command -v python &> /dev/null; then
    python -m http.server 8000
else
    echo "Error: Python is not installed"
    echo "Please install Python 3 to run this server"
    exit 1
fi
