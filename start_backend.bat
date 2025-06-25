@echo off
echo 네이버 부동산 크롤러 시작...
echo.

echo [1/3] Python 백엔드 서버 확인 중...
cd logic
python --version >nul 2>&1
if errorlevel 1 (
    echo 오류: Python이 설치되지 않았습니다.
    pause
    exit /b 1
)

echo [2/3] Python 의존성 설치 중...
pip install -r ../requirements.txt

echo [3/3] FastAPI 서버 시작 중...
echo 서버가 http://localhost:8000 에서 실행됩니다.
echo 브라우저에서 http://localhost:5173 으로 접속하세요.
echo.
echo 서버를 중지하려면 Ctrl+C를 누르세요.
echo.

python api_server.py
