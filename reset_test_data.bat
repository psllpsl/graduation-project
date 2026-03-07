@echo off
chcp 65001 >nul
echo ========================================
echo   牙科修复系统 - 测试数据重置工具
echo ========================================
echo.
echo 警告：此操作将清空所有测试数据！
echo.
set /p confirm="确认清空所有数据？(y/n): "
if /i "%confirm%" neq "y" (
    echo 已取消
    pause
    exit /b
)

echo.
echo 正在清空数据...
mysql -u root -p dental_clinic -e "TRUNCATE TABLE dialogues; TRUNCATE TABLE appointments; TRUNCATE TABLE treatment_records; TRUNCATE TABLE patients; TRUNCATE TABLE knowledge_base; TRUNCATE TABLE system_config; TRUNCATE TABLE users;"

echo.
echo ========================================
echo   数据已清空，ID 将从 1 重新开始
echo ========================================
echo.
pause
