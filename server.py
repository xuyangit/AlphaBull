from flask import Flask
from flask import render_template
from flask import send_from_directory
from flask import make_response
from flask import request
from flask import redirect
from flask import jsonify
from  getHotStocks import getHotStocks

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def hotStocks():
    xueqiuRes, tweetRes, followRes = getHotStocks()
    return render_template("Home.html", data={
        "xueqiu": xueqiuRes,
        "follow": followRes,
        "tweet": tweetRes
    })

if __name__ == "__main__":
    app.run(port=8000, host="58.196.143.65")
