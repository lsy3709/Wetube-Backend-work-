"""메인 라우트 – 프론트 전용, DB/백엔드 없음."""

from flask import Blueprint, render_template, request

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("main/index.html")


@main_bp.route("/watch/<int:video_id>")
def watch(video_id):
    return render_template("main/watch.html", video_id=video_id)


@main_bp.route("/search")
def search():
    query = request.args.get("q", "").strip()
    results_count = 10 if query else 0
    return render_template("main/search.html", query=query, results_count=results_count)


@main_bp.route("/subscriptions")
def subscriptions():
    return render_template("main/subscriptions.html")


@main_bp.route("/tag/<tag>")
def tag(tag):
    results_count = 12
    return render_template("main/tag.html", tag=tag, results_count=results_count)


@main_bp.route("/user/<username>")
def user_profile(username):
    # 프론트 전용 샘플 데이터
    sample_users = {
        "lsye": {"nickname": "lsye", "subs_count": 100, "video_count": 12, "description": "WeTube 크리에이터입니다."},
        "aaa": {"nickname": "aaa", "subs_count": 50, "video_count": 5, "description": "안녕하세요, aaa 채널입니다."},
    }
    data = sample_users.get(username, {
        "nickname": username,
        "subs_count": 0,
        "video_count": 0,
        "description": "채널 설명이 없습니다.",
    })
    return render_template("main/user_profile.html", username=username, **data)
