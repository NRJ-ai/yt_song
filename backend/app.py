# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from youtubesearchpython import VideosSearch

# app = Flask(__name__)
# CORS(app)

# @app.route("/api/search")
# def search():
#     query = request.args.get("q")
#     if not query:
#         return jsonify({"error": "No query provided"}), 400

#     videos_search = VideosSearch(query, limit=5)
#     results = videos_search.result()["result"]

#     return jsonify([
#         {
#             "title": v["title"],
#             "videoId": v["id"],
#             "thumbnail": v["thumbnails"][0]["url"]
#         } for v in results
#     ])

# if __name__ == "__main__":
#     app.run(debug=True)



import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from youtubesearchpython import VideosSearch

app = Flask(__name__)
CORS(app)

def is_embeddable(video_id):
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
    response = requests.get(url)
    return response.status_code == 200

@app.route("/api/search")
def search():
    query = request.args.get("q")
    videos_search = VideosSearch(query, limit=10)
    results = videos_search.result()["result"]

    filtered = []
    for video in results:
        video_id = video.get("id")
        if video_id and is_embeddable(video_id):
            filtered.append({
                "title": video["title"],
                "videoId": video_id,
                "thumbnail": video["thumbnails"][0]["url"]
            })

    return jsonify(filtered)

if __name__ == "__main__":
    app.run(debug=True)
