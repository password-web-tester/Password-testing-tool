# main.py - Entry point for Android
from app import app
import threading
import webbrowser
import time
import os

def open_browser():
    """Open browser after server starts"""
    time.sleep(2)
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    # Start browser in background
    threading.Thread(target=open_browser).start()
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
