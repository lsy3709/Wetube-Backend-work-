"""관리자 라우트 – DB 실데이터 연동, Flask-Login 인증."""

from pathlib import Path

from flask import Blueprint, current_app, redirect, render_template, request, send_file, url_for
from flask_login import current_user, login_required
from sqlalchemy.orm import joinedload

from app import db
from app.models import User, Video

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def _admin_required(f):
    """관리자 권한 필수. 비로그인 → 로그인, 일반 유저 → 403."""
    from functools import wraps

    @wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login", next=url_for("admin.index")))
        if not current_user.is_admin:
            return render_template("errors/403.html"), 403
        return f(*args, **kwargs)

    return wrapped


@admin_bp.route("/login")
def login():
    return redirect(url_for("auth.login"))


@admin_bp.route("/")
@login_required
@_admin_required
def index():
    """관리자 대시보드 – DB 실통계."""
    stats = {
        "user_count": User.query.count(),
        "video_count": Video.query.count(),
        "channel_count": User.query.count(),  # 사용자 = 채널
        "comment_count": 0,  # Comment 모델 미구현 시 0
    }
    try:
        from sqlalchemy import text

        r = db.session.execute(text("SELECT COUNT(*) FROM comments")).scalar()
        stats["comment_count"] = int(r) if r else 0
    except Exception:
        pass
    return render_template("admin/index.html", stats=stats)


@admin_bp.route("/users")
@login_required
@_admin_required
def users():
    """회원 관리 – DB users 테이블 연동. q 파라미터로 검색."""
    from sqlalchemy import or_

    page = request.args.get("page", 1, type=int)
    q_param = (request.args.get("q") or "").strip()
    if page < 1:
        page = 1

    query = User.query
    if q_param:
        pattern = f"%{q_param}%"
        query = query.filter(
            or_(
                User.username.ilike(pattern),
                User.email.ilike(pattern),
                User.nickname.ilike(pattern),
            )
        )
    pagination = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=15
    )
    return render_template("admin/users.html", users=pagination)


@admin_bp.route("/videos")
@login_required
@_admin_required
def videos():
    """동영상 관리 – DB videos 테이블 연동. q 파라미터로 제목/업로더 검색."""
    from sqlalchemy import or_

    page = request.args.get("page", 1, type=int)
    q_param = (request.args.get("q") or "").strip()
    if page < 1:
        page = 1

    query = Video.query.options(joinedload(Video.user))
    if q_param:
        pattern = f"%{q_param}%"
        query = query.join(Video.user).filter(
            or_(
                Video.title.ilike(pattern),
                User.username.ilike(pattern),
            )
        )
    pagination = query.order_by(Video.created_at.desc()).paginate(
        page=page, per_page=15
    )
    return render_template("admin/videos.html", videos=pagination)


@admin_bp.route("/comments")
@login_required
@_admin_required
def comments():
    return render_template("admin/comments.html")


@admin_bp.route("/database")
@login_required
@_admin_required
def database():
    return render_template("admin/database.html")


@admin_bp.route("/api-preview")
@login_required
@_admin_required
def api_preview():
    """REST API 데이터 미리보기 화면. JS에서 /api/videos, /api/tags/popular 호출."""
    return render_template("admin/api_preview.html")


@admin_bp.route("/db-verify")
@login_required
@_admin_required
def db_verify():
    """
    DB 검증 리포트 화면. scripts/db_verify.py 실행 후 생성된 리포트를 표시.
    리포트 없으면 안내 페이지.
    """
    report_path = Path(current_app.instance_path) / "db_verify_report.html"
    if report_path.exists():
        return send_file(str(report_path), mimetype="text/html")
    return render_template("admin/db_verify_placeholder.html")


@admin_bp.route("/query")
@login_required
@_admin_required
def query():
    return render_template("admin/query.html")


@admin_bp.route("/table/<table_name>")
@login_required
@_admin_required
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
