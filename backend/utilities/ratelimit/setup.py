'''
/utilities/ratelimit/setup.py
-> rate limiting setup using Flask-Limiter
'''

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# ==================================================
# global vars
# ==================================================

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per minute", "5000 per hour"],
    storage_uri="memory://",
    strategy="moving-window"
)

# ==================================================
# initialize on app context
# ==================================================

def initRateLimiter(app):

    limiter.init_app(app)

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return {
            "error": "Rate limit exceeded",
            "message": "Too many requests. Please try again later."
        }, 429
