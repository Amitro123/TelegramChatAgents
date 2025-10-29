# ========================================
# FIX 7: Add Health Check Endpoint (Bonus)
# Create new file: health.py
# ========================================

"""
Optional: Add a simple health check endpoint
to monitor if bot is running

Run this in a separate thread or process
"""

from flask import Flask, jsonify
from threading import Thread
import time

app = Flask(__name__)

bot_status = {
    "running": True,
    "start_time": time.time(),
    "last_message": None,
    "total_messages": 0
}

@app.route('/health')
def health():
    uptime = int(time.time() - bot_status["start_time"])
    return jsonify({
        "status": "healthy" if bot_status["running"] else "unhealthy",
        "uptime_seconds": uptime,
        "total_messages": bot_status["total_messages"]
    })

def run_health_server():
    app.run(host='0.0.0.0', port=8080)

# Start in background:
# health_thread = Thread(target=run_health_server, daemon=True)
# health_thread.start()
