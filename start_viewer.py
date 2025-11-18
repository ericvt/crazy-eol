#!/usr/bin/env python3
"""
Simple HTTP server to view the pivot table visualization
"""
import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers to allow file access
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

# Change to the script directory
os.chdir(Path(__file__).parent)

# Check if files exist
if not os.path.exists('pivot_viewer.html'):
    print("❌ Error: pivot_viewer.html not found!")
    exit(1)

if not os.path.exists('data_pivot.csv'):
    print("❌ Error: data_pivot.csv not found!")
    print("Please run process_pipeline.py first to generate the CSV file.")
    exit(1)

print(f"🌐 Starting web server on http://localhost:{PORT}")
print(f"📊 Opening pivot table viewer in your browser...")
print(f"\n✨ Press Ctrl+C to stop the server\n")

# Start server in a thread and open browser
with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    # Open browser
    webbrowser.open(f'http://localhost:{PORT}/pivot_viewer.html')
    
    # Serve forever
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
