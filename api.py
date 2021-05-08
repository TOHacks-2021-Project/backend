from main import app
from flask import jsonify

@app.route("/api/test", methods=['GET'])
def api_test():
    return "Works!"

