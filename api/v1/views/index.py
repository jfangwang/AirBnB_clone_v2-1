#!/usr/bin/python3
"""index file"""

from api.v1.views import app_views


@app_views.route("/status")
def status:
    """status"""
    return {"status": "OK"}