"""인증 라우트 – 로그인/회원가입 페이지만. DB·백엔드 없음."""

from flask import Blueprint, render_template

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login")
def login():
    return render_template("auth/login.html")


@auth_bp.route("/register")
def register():
    return render_template("auth/register.html")


@auth_bp.route("/profile")
def profile():
    return render_template("auth/profile.html")
