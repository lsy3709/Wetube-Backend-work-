# Studio 라우트 – 동영상 관리·업로드

import os
import uuid

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for

from app import db
from app.models import Video

studio_bp = Blueprint("studio", __name__, url_prefix="/studio")


def _allowed_file(filename, allowed_extensions):
    """파일 확장자가 허용 목록에 있는지 검사 (빈 filename·None 처리)."""
    if not filename or "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[-1].lower()
    return ext in allowed_extensions


def _save_upload_file(file_storage, save_dir, allowed_extensions, max_size):
    """
    업로드 파일 검증 후 저장.
    반환: (저장된 파일명, None) 또는 (None, 에러메시지)
    """
    if not file_storage or not file_storage.filename:
        return None, "파일이 선택되지 않았습니다."

    filename = file_storage.filename
    if not _allowed_file(filename, allowed_extensions):
        return None, f"허용되지 않는 파일 형식입니다. 허용: {', '.join(sorted(allowed_extensions))}"

    file_storage.seek(0, os.SEEK_END)
    size = file_storage.tell()
    file_storage.seek(0)
    if size > max_size:
        max_mb = max_size // (1024 * 1024)
        return None, f"파일 크기가 너무 큽니다. 최대 {max_mb}MB까지 업로드할 수 있습니다."

    ext = filename.rsplit(".", 1)[-1].lower()
    safe_filename = f"{uuid.uuid4().hex}.{ext}"
    save_path = os.path.join(save_dir, safe_filename)
    try:
        file_storage.save(save_path)
    except OSError as e:
        return None, f"파일 저장 중 오류가 발생했습니다: {e}"
    return safe_filename, None


@studio_bp.route("/")
@studio_bp.route("")  # /studio (끝 슬래시 없음)도 처리
def index():
    return render_template("studio/index.html")


@studio_bp.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return render_template("studio/upload.html")

    # POST: 폼 데이터 수신
    title = (request.form.get("title") or "").strip()
    description = (request.form.get("description") or "").strip()
    video_file = request.files.get("video")
    thumbnail_file = request.files.get("thumbnail")

    # 제목 필수
    if not title:
        flash("제목을 입력해주세요.", "error")
        return render_template("studio/upload.html", title=title, description=description), 400

    if len(title) > 200:
        flash("제목은 200자 이하여야 합니다.", "error")
        return render_template("studio/upload.html", title=title, description=description), 400

    # 비디오 파일 검증 후 저장
    video_folder = current_app.config["VIDEO_FOLDER"]
    allowed_video = current_app.config["ALLOWED_VIDEO_EXTENSIONS"]
    max_video_size = current_app.config["MAX_VIDEO_SIZE"]
    video_filename, video_error = _save_upload_file(
        video_file, video_folder, allowed_video, max_video_size
    )
    if video_error:
        flash(video_error, "error")
        return render_template("studio/upload.html", title=title, description=description), 400

    # 썸네일(선택) 검증 후 저장
    thumbnail_filename = None
    if thumbnail_file and thumbnail_file.filename:
        thumb_folder = current_app.config["THUMBNAIL_FOLDER"]
        allowed_thumb = current_app.config["ALLOWED_THUMBNAIL_EXTENSIONS"]
        max_thumb_size = current_app.config["MAX_THUMBNAIL_SIZE"]
        thumbnail_filename, thumb_error = _save_upload_file(
            thumbnail_file, thumb_folder, allowed_thumb, max_thumb_size
        )
        if thumb_error:
            # 비디오는 이미 저장됐으므로 저장된 비디오 파일 삭제 후 에러 반환
            try:
                os.remove(os.path.join(video_folder, video_filename))
            except OSError:
                pass
            flash(thumb_error, "error")
            return render_template("studio/upload.html", title=title, description=description), 400

    # DB에 Video 저장
    user_id = current_app.config.get("DEFAULT_USER_ID", 1)
    try:
        video = Video(
            title=title,
            description=description or None,
            video_path=video_filename,
            thumbnail_path=thumbnail_filename,
            user_id=user_id,
        )
        db.session.add(video)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        # 저장된 파일 정리
        try:
            os.remove(os.path.join(video_folder, video_filename))
        except OSError:
            pass
        if thumbnail_filename:
            try:
                os.remove(os.path.join(current_app.config["THUMBNAIL_FOLDER"], thumbnail_filename))
            except OSError:
                pass
        flash(f"DB 저장 중 오류가 발생했습니다: {e}", "error")
        return render_template("studio/upload.html", title=title, description=description), 500

    flash("동영상이 업로드되었습니다.", "success")
    return redirect(url_for("studio.index"))


@studio_bp.route("/edit/<int:video_id>")
def edit(video_id):
    return render_template("studio/edit.html", video_id=video_id)
