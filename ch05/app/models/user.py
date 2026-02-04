"""
사용자 모델 – users 테이블 (Video FK용).
업로드 시 config.DEFAULT_USER_ID(1)가 이 테이블의 id를 참조.
"""
from datetime import datetime

from app import db


class User(db.Model):
    """사용자 – 업로드 시 user_id FK용."""

    __tablename__ = "users"

    # PK, 자동 증가
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(80), nullable=True)
    profile_image = db.Column(db.String(255), nullable=True)
    profile_image_public_id = db.Column(db.String(255), nullable=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    # 생성/수정 시 자동 설정
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
