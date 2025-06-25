@echo off
echo 전체 애플리케이션 설정 및 시작...
echo.

echo [1/4] Python 의존성 설치...
pip install -r requirements.txt
if errorlevel 1 (
    echo 오류: Python 패키지 설치 실패
    pause
    exit /b 1
)

echo [2/4] Playwright 브라우저 설치...
playwright install chromium
if errorlevel 1 (
    echo 오류: Playwright 브라우저 설치 실패
    pause
    exit /b 1
)

echo [3/4] Node.js 의존성 설치...
npm install
if errorlevel 1 (
    echo 오류: Node.js 패키지 설치 실패
    pause
    exit /b 1
)

echo [4/4] 설치 완료!
echo.
echo 이제 다음 순서로 서버를 시작하세요:
echo 1. start_backend.bat 실행 (새 터미널에서)
echo 2. start_frontend.bat 실행 (새 터미널에서)
echo.
echo 또는 개별적으로 실행:
echo - 백엔드: cd logic && python api_server.py
echo - 프론트엔드: npm run dev
echo.
pause
