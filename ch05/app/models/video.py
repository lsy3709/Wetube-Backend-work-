# 비디오 모델 – videos 테이블

from datetime import datetime

from app import db


class Video(db.Model):
    """업로드된 동영상 정보."""

    __tablename__ = "videos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    video_path = db.Column(db.String(500), nullable=False)
    thumbnail_path = db.Column(db.String(500), nullable=True)
    category = db.Column(db.String(50), nullable=True)
    duration = db.Column(db.Integer, nullable=True)
    views = db.Column(db.Integer, nullable=False, default=0)
    likes = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    video_public_id = db.Column(db.String(255), nullable=True)
    thumbnail_public_id = db.Column(db.String(255), nullable=True)
