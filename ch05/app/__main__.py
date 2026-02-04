"""WeTube 실행 진입점 – python -m app으로 실행 시 사용."""

from app import app

if __name__ == "__main__":
    print("등록된 라우트: / /auth/login /auth/register /auth/profile /studio ...")
    print("중요: 5000 포트를 쓰는 다른 프로그램(기존 Flask 등)이 있으면 먼저 종료하세요.")
    print("      그렇지 않으면 /studio/ 에서 404가 납니다.")
    app.run(debug=True, host="127.0.0.1", port=5000, use_reloader=False)
