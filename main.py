from flask import Flask, request, json
from router.otakudesu import otaku

app = Flask(__name__)

@app.route("/")
def home():
    return "hello world"

app.register_blueprint(otaku)

# @app.route("/test")
# def test_route():
#     channels = scrapetube.get_channel("UCxxnxya_32jcKj4yN1_kD7A", limit=100)
#     videos = []
#     for video in channels:
#         videos.append(video) 
    
#     return {"result": videos}

app.run(port=3000, debug=False)