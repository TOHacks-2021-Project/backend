from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/testcrash")
def testcrash():
    raise Exception("Test Exception")

@app.route("/api/test", methods=['GET'])
def api_test():
    return "Works!"

if __name__ == "__main__":
    print(app.url_map)
    app.run(port=5050, debug=True)
