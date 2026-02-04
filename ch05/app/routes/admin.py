"""관리자 라우트 – 프론트 전용, DB/백엔드 없음."""

from flask import Blueprint, render_template, redirect, url_for

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/login")
def login():
    return redirect(url_for("auth.login"))


@admin_bp.route("/")
def index():
    return render_template("admin/index.html")


@admin_bp.route("/users")
def users():
    return render_template("admin/users.html")


@admin_bp.route("/videos")
def videos():
    return render_template("admin/videos.html")


@admin_bp.route("/comments")
def comments():
    return render_template("admin/comments.html")


@admin_bp.route("/database")
def database():
    return render_template("admin/database.html")


@admin_bp.route("/query")
def query():
    return render_template("admin/query.html")


@admin_bp.route("/table/<table_name>")
def table_view(table_name):
    # 프론트 전용: 테이블별 구조 및 샘플 데이터
    TABLES = {
        "user": {
            "columns": [
                {"name": "id", "type": "INT", "key": "PK", "null": "NO"},
                {"name": "username", "type": "VARCHAR(50)", "key": "-", "null": "NO"},
                {"name": "email", "type": "VARCHAR(100)", "key": "-", "null": "YES"},
                {"name": "created_at", "type": "DATETIME", "key": "-", "null": "NO"},
            ],
            "sample": [
                {"id": 1, "username": "aaa", "email": "aaa@example.com", "created_at": "2025-01-20"},
                {"id": 2, "username": "admin", "email": "admin@example.com", "created_at": "2025-01-19"},
                {"id": 3, "username": "lsye", "email": "lsye@example.com", "created_at": "2025-01-18"},
            ],
        },
        "video": {
            "columns": [
                {"name": "id", "type": "INT", "key": "PK", "null": "NO"},
                {"name": "title", "type": "VARCHAR(200)", "key": "-", "null": "NO"},
                {"name": "user_id", "type": "INT", "key": "FK", "null": "NO"},
                {"name": "views", "type": "INT", "key": "-", "null": "NO"},
                {"name": "created_at", "type": "DATETIME", "key": "-", "null": "NO"},
            ],
            "sample": [
                {"id": 1, "title": "샘플 동영상 1", "user_id": 1, "views": 100, "created_at": "2025-01-20"},
                {"id": 2, "title": "샘플 동영상 2", "user_id": 2, "views": 200, "created_at": "2025-01-19"},
                {"id": 3, "title": "샘플 동영상 3", "user_id": 3, "views": 150, "created_at": "2025-01-18"},
            ],
        },
        "comment": {
            "columns": [
                {"name": "id", "type": "INT", "key": "PK", "null": "NO"},
                {"name": "video_id", "type": "INT", "key": "FK", "null": "NO"},
                {"name": "user_id", "type": "INT", "key": "FK", "null": "NO"},
                {"name": "content", "type": "TEXT", "key": "-", "null": "NO"},
                {"name": "created_at", "type": "DATETIME", "key": "-", "null": "NO"},
            ],
            "sample": [
                {"id": 1, "video_id": 1, "user_id": 1, "content": "좋은 영상이네요!", "created_at": "2025-01-20"},
                {"id": 2, "video_id": 1, "user_id": 2, "content": "잘 봤습니다. 구독했어요!", "created_at": "2025-01-20"},
                {"id": 3, "video_id": 2, "user_id": 3, "content": "프론트엔드 테스트 댓글입니다.", "created_at": "2025-01-19"},
            ],
        },
        "channel": {
            "columns": [
                {"name": "id", "type": "INT", "key": "PK", "null": "NO"},
                {"name": "user_id", "type": "INT", "key": "FK", "null": "NO"},
                {"name": "name", "type": "VARCHAR(100)", "key": "-", "null": "NO"},
                {"name": "subscribers", "type": "INT", "key": "-", "null": "NO"},
            ],
            "sample": [
                {"id": 1, "user_id": 1, "name": "aaa 채널", "subscribers": 50},
                {"id": 2, "user_id": 3, "name": "lsye 채널", "subscribers": 100},
            ],
        },
        "subscription": {
            "columns": [
                {"name": "id", "type": "INT", "key": "PK", "null": "NO"},
                {"name": "user_id", "type": "INT", "key": "FK", "null": "NO"},
                {"name": "channel_id", "type": "INT", "key": "FK", "null": "NO"},
                {"name": "created_at", "type": "DATETIME", "key": "-", "null": "NO"},
            ],
            "sample": [
                {"id": 1, "user_id": 1, "channel_id": 2, "created_at": "2025-01-20"},
                {"id": 2, "user_id": 2, "channel_id": 1, "created_at": "2025-01-19"},
            ],
        },
    }
    data = TABLES.get(table_name)
    if not data:
        columns = [{"name": "id", "type": "INT", "key": "PK", "null": "NO"}]
        sample_data = []
    else:
        columns = data["columns"]
        sample_data = data["sample"]
    return render_template(
        "admin/table_view.html",
        table_name=table_name,
        columns=columns,
        sample_data=sample_data,
    )
