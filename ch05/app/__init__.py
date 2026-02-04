"""Flask 앱 팩토리 – 업로드·DB 포함."""

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# DB 확장 (create_app에서 init_app로 초기화)
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # 프로젝트 루트 기준 업로드 경로
    project_root = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    video_folder = os.path.join(project_root, "uploads", "videos")
    thumbnail_folder = os.path.join(project_root, "uploads", "thumbnails")

    app.config.from_mapping(
        SECRET_KEY="dev-frontend-only",
        # DB (SQLite)
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            "DATABASE_URL",
            f"sqlite:///{os.path.join(project_root, 'instance', 'wetube.db')}",
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        # 업로드 폴더 (config에 저장)
        VIDEO_FOLDER=video_folder,
        THUMBNAIL_FOLDER=thumbnail_folder,
        # 업로드 제한 (바이트)
        MAX_VIDEO_SIZE=2 * 1024 * 1024 * 1024,  # 2GB
        MAX_THUMBNAIL_SIZE=5 * 1024 * 1024,  # 5MB
        # 허용 확장자 (소문자)
        ALLOWED_VIDEO_EXTENSIONS={"mp4", "webm", "mov"},
        ALLOWED_THUMBNAIL_EXTENSIONS={"jpg", "jpeg", "png", "gif", "webp"},
        # 업로드 시 사용할 기본 user_id (로그인 미연동 시)
        DEFAULT_USER_ID=1,
    )

    # 업로드 폴더 생성
    os.makedirs(app.config["VIDEO_FOLDER"], exist_ok=True)
    os.makedirs(app.config["THUMBNAIL_FOLDER"], exist_ok=True)
    # DB용 instance 폴더
    instance_path = os.path.join(project_root, "instance")
    os.makedirs(instance_path, exist_ok=True)

    db.init_app(app)

    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.studio import studio_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(studio_bp)
    app.register_blueprint(admin_bp)

    # 모델 등록 후 테이블 생성
    from app import models  # noqa: F401
    from app.models import User

    with app.app_context():
        db.create_all()
        # 업로드용 기본 사용자 없으면 생성 (user_id=1)
        if User.query.get(1) is None:
            default_user = User(
                username="default",
                email="default@example.com",
                password_hash="",
            )
            db.session.add(default_user)
            db.session.commit()

    return app


# flask run / FLASK_APP=app 사용 시 동일 앱 로드
app = create_app()

# 직접 실행 시 (python -m app 또는 python app/__init__.py)
if __name__ == "__main__":
    print("등록된 라우트: / /auth/login /auth/register /auth/profile /studio ...")
    print("중요: 5000 포트를 쓰는 다른 프로그램(기존 Flask 등)이 있으면 먼저 종료하세요.")
    print("      그렇지 않으면 /studio/ 에서 404가 납니다.")
    app.run(debug=True, host="127.0.0.1", port=5000, use_reloader=False)
