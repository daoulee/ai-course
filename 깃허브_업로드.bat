@echo off
chcp 65001 > nul
title AI 활용 프로그래밍 - GitHub 자동 업로드 (202230136)

echo ================================================================
echo        🚀 AI 활용 프로그래밍 1주차 과제 GitHub 업로드
echo ================================================================
echo.

set /p github_id="1. 본인의 GitHub 아이디를 입력하세요: "

if "%github_id%"=="" (
    echo 아이디가 입력되지 않았습니다. 다시 실행해주세요.
    pause
    exit /b
)

echo.
echo [1/5] Git 저장소 초기화 중...
git init

echo [2/5] 과제 파일 (README.md, baseball.py) 스테이징 중...
git add .

echo [3/5] 첫 번째 커밋 생성 중...
git commit -m "1주차: 저장소 생성, GPU 측정 결과 및 숫자 야구 게임"

echo [4/5] 브랜치 main 설정 및 원격 저장소 연결 중...
git branch -M main
git remote remove origin >nul 2>&1
git remote add origin https://github.com/%github_id%/ai-course.git

echo [5/5] GitHub으로 푸시 중... (로그인 창이 뜨면 로그인 및 승인해주세요)
git push -u origin main

echo.
if %errorlevel% equ 0 (
    echo ================================================================
    echo  🎉 축하합니다! GitHub 푸시가 성공적으로 완료되었습니다!
    echo  👉 제출할 저장소 주소: https://github.com/%github_id%/ai-course
    echo  📧 제출처: 2025106@daelim.ac.kr
    echo ================================================================
) else (
    echo ================================================================
    echo  ⚠️ 푸시 중 오류가 발생했습니다.
    echo  - GitHub에 'ai-course' 저장소가 미리 생성되어 있는지 확인해주세요.
    echo  - Git이 설치되어 있는지 확인해주세요.
    echo ================================================================
)

pause
