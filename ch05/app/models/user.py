"""
사용자 모델 – users 테이블 (Video FK용).
업로드 시 config.DEFAULT_USER_ID(1)가 이 테이블의 id를 참조.
"""
from datetime import datetime, timezone

from app import db


def _utc_now():
    """datetime.utcnow() deprecated 대체."""
    return datetime.now(timezone.utc)


class User(db.Model):
    """사용자 – 업로드 시 user_id FK용."""

    # 테이블명. 지정하지 않으면 클래스명을 소문자로 변환한 이름 사용
    __tablename__ = "users"

    # ----- 기본 키 -----
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # ----- 계정·프로필 -----
    username = db.Column(db.String(80), nullable=False, unique=True)  # 로그인 ID, 중복 불가
    email = db.Column(db.String(120), nullable=False, unique=True)      # 이메일, 중복 불가
    password_hash = db.Column(db.String(255), nullable=False)          # 비밀번호 해시 (평문 저장 금지)
    nickname = db.Column(db.String(80), nullable=True)                # 표시용 닉네임
    profile_image = db.Column(db.String(255), nullable=True)           # 프로필 이미지 파일 경로 또는 URL
    profile_image_public_id = db.Column(db.String(255), nullable=True) # 클라우드 저장 시 public_id (예: Cloudinary)

    # ----- 권한 -----
    is_admin = db.Column(db.Boolean, nullable=False, default=False)   # 관리자 여부

    # ----- 타임스탬프 -----
    created_at = db.Column(db.DateTime, default=_utc_now)                    # 최초 생성 시각
    updated_at = db.Column(db.DateTime, default=_utc_now, onupdate=_utc_now)  # 수정 시 자동 갱신
