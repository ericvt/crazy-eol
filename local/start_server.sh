#!/bin/bash
cd "$(dirname "$0")"
echo "Starting local web server..."
echo "Open your browser to:"
echo "  - http://localhost:8000/local/tenant_branch_TransFlavors.html"
echo "  - http://localhost:8000/local/branch_culture.html"
echo "  - http://localhost:8000/local/pivot_viewer.html"
echo "Press Ctrl+C to stop the server"
python3 -m http.server 8000
