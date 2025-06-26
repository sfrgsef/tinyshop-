@echo off
chcp 65001 >nul
echo ========================================
echo 百度搜索自动化测试
echo ========================================
echo.

echo 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

echo 正在检查依赖包...
python -c "import selenium, pytest" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  警告：缺少依赖包，正在安装...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ 错误：依赖包安装失败
        pause
        exit /b 1
    )
)

echo.
echo 开始运行测试...
echo.

python run_tests.py

echo.
echo 测试完成！
pause 