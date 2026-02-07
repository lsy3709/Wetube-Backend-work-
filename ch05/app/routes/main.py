"""메인 라우트 – DB·미디어 연동."""

from sqlalchemy import func, or_

from flask import Blueprint, current_app, render_template, request, send_from_directory

from app import db
from app.models import Tag, User, Video
from app.models.video import video_tags

main_bp = Blueprint("main", __name__)


def _get_popular_tags(limit=12):
    """동영상이 연결된 태그를 비디오 수 기준으로 정렬해 반환."""
    return (
        db.session.query(Tag)
        .join(video_tags)
        .group_by(Tag.id)
        .order_by(func.count(video_tags.c.video_id).desc())
        .limit(limit)
        .all()
    )


# ----- 업로드된 미디어 서빙 (비디오·썸네일 URL) -----
@main_bp.route("/media/videos/<path:filename>")
def media_video(filename):
    """업로드된 비디오 파일 응답."""
    return send_from_directory(current_app.config["VIDEO_FOLDER"], filename)


@main_bp.route("/media/thumbnails/<path:filename>")
def media_thumbnail(filename):
    """업로드된 썸네일 이미지 응답."""
    return send_from_directory(current_app.config["THUMBNAIL_FOLDER"], filename)


@main_bp.route("/")
def index():
    category = request.args.get("category", "all")
    sort = request.args.get("sort", "latest")
    tag_filter = request.args.get("tag", "").strip()

    q = Video.query
    if category != "all":
        q = q.filter(Video.category == category)
    if tag_filter:
        tag_obj = Tag.query.filter_by(name=tag_filter).first()
        if tag_obj:
            q = q.join(video_tags).filter(video_tags.c.tag_id == tag_obj.id)
        else:
            q = q.filter(Video.id < 0)
    if sort == "popular":
        q = q.order_by(Video.likes.desc(), Video.views.desc())
    elif sort == "views":
        q = q.order_by(Video.views.desc())
    else:
        q = q.order_by(Video.created_at.desc())
    videos = q.limit(24).all()
    popular_tags = _get_popular_tags()
    return render_template(
        "main/index.html",
        videos=videos,
        popular_tags=popular_tags,
        current_tag=tag_filter or None,
    )


@main_bp.route("/watch/<int:video_id>")
def watch(video_id):
    video = Video.query.get_or_404(video_id)
    user = db.session.get(User, video.user_id) if video.user_id else None
    channel_name = user.username if user else "default"
    related = Video.query.filter(Video.id != video_id).order_by(Video.created_at.desc()).limit(10).all()
    return render_template("main/watch.html", video=video, channel_name=channel_name, related_videos=related)


@main_bp.route("/search")
def search():
    query = request.args.get("q", "").strip()
    if query:
        pattern = f"%{query}%"
        videos = (
            Video.query.filter(
                or_(Video.title.ilike(pattern), (Video.description.isnot(None) & Video.description.ilike(pattern)))
            )
            .order_by(Video.created_at.desc())
            .limit(20)
            .all()
        )
        results_count = len(videos)
    else:
        videos = []
        results_count = 0
    return render_template("main/search.html", query=query, videos=videos, results_count=results_count)


@main_bp.route("/subscriptions")
def subscriptions():
    return render_template("main/subscriptions.html")


@main_bp.route("/tag/<tag_name>")
def tag(tag_name):
    tag_obj = Tag.query.filter_by(name=tag_name).first()
    if tag_obj is None:
        videos = []
        results_count = 0
    else:
        videos = tag_obj.videos.order_by(Video.created_at.desc()).limit(24).all()
        results_count = tag_obj.videos.count()
    popular_tags = _get_popular_tags()
    return render_template(
        "main/tag.html",
        tag=tag_name,
        videos=videos,
        results_count=results_count,
        popular_tags=popular_tags,
    )


@main_bp.route("/user/<username>")
def user_profile(username):
    # DB에 해당 username 유저가 있으면 사용, 없으면 샘플 데이터
    user = User.query.filter_by(username=username).first()
    if user:
        video_count = Video.query.filter_by(user_id=user.id).count()
        data = {
            "nickname": user.nickname or user.username,
            "subs_count": 0,
            "video_count": video_count,
            "description": "채널 설명",
        }
    else:
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
