# streamlit/metrics/metrics_server.py
from flask import Flask, Response
from prometheus_client import Counter, generate_latest, CollectorRegistry
import threading
import logging

# Configure logging for debugging and monitoring
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Initialize Flask app
flask_app = Flask(__name__)

# Custom registry for Streamlit metrics
registry = CollectorRegistry()
REQUESTS_TOTAL = Counter(
    "streamlit_requests_total",
    "Total Streamlit requests",
    registry=registry
)

@flask_app.route("/metrics", methods=["GET"])
def metrics():
    """
    Expose Prometheus metrics for Streamlit usage.
    CSRF protection is not required as this is a read-only GET endpoint
    used solely by Prometheus for scraping, with no authentication or state changes.
    """
    logger.debug("Serving metrics request")
    return Response(generate_latest(registry), mimetype="text/plain")

def run_flask():
    """Run the Flask metrics server in a separate thread."""
    logger.info("Starting Flask metrics server on port 8005")
    flask_app.run(host="0.0.0.0", port=8005, use_reloader=False, debug=False)

# Start Flask in a daemon thread
threading.Thread(target=run_flask, daemon=True).start()