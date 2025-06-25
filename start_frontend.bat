@echo off
echo Svelte 개발 서버 시작...
echo.

echo [1/2] Node.js 의존성 확인 중...
node --version >nul 2>&1
if errorlevel 1 (
    echo 오류: Node.js가 설치되지 않았습니다.
    pause
    exit /b 1
)

echo [2/2] 개발 서버 시작 중...
echo 서버가 http://localhost:5173 에서 실행됩니다.
echo.
echo 백엔드 서버가 실행 중인지 확인하세요 (http://localhost:8000)
echo 서버를 중지하려면 Ctrl+C를 누르세요.
echo.

npm run dev
