from flask import Flask, request, jsonify
import uuid
from datetime import datetime

app = Flask(__name__)

posts, comments = {}, {}

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Blog API is running"}), 200

@app.route("/posts", methods=["POST"])
def create_post():
    data = request.get_json()
    if not data or "title" not in data or "content" not in data:
        return jsonify({"error": "Title and content required"}), 400
    post_id = str(uuid.uuid4())
    post = {
        "id": post_id,
        "title": data["title"],
        "content": data["content"],
        "createdAt": datetime.isoformat()
    }
    posts[post_id] = post
    return jsonify(post), 201

@app.route("/posts", methods=["GET"])
def get_posts():
    return jsonify(list(posts.values()))

@app.route("/posts/<post_id>", methods=["PUT"])
def update_post(post_id):
    data = request.get_json()
    post = posts.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    post.update({k: v for k, v in data.items() if k in ["title", "content"]})
    return jsonify(post)

@app.route("/posts/<post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = posts.pop(post_id, None)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    for cid in [c for c, v in comments.items() if v["postId"] == post_id]:
        comments.pop(cid)
    return jsonify({"message": "Post and related comments deleted", "post": post})

@app.route("/posts/<post_id>/comments", methods=["POST"])
def add_comment(post_id):
    if post_id not in posts:
        return jsonify({"error": "Post not found"}), 404
    data = request.get_json()
    if not data or "author" not in data or "text" not in data:
        return jsonify({"error": "Author and text required"}), 400
    cid = str(uuid.uuid4())
    comment = {
        "id": cid,
        "postId": post_id,
        "author": data["author"],
        "text": data["text"],
        "createdAt": datetime.isoformat()
    }
    comments[cid] = comment
    return jsonify(comment), 201

@app.route("/posts/<post_id>/comments", methods=["GET"])
def get_comments(post_id):
    return jsonify([c for c in comments.values() if c["postId"] == post_id])

@app.route("/comments/<cid>", methods=["DELETE"])
def delete_comments(cid):
    comment = comments.pop(cid, None)
    if not comment:
        return jsonify({"error": "Comment not found"}), 404
    return jsonify({"message": "Comment deleted", "comment": comment})

if __name__ == "__main__":
    app.run(debug=True)
