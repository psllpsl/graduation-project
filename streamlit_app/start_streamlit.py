"""
牙科修复复诊系统 - Streamlit 后台启动脚本
功能：
1. 检查是否已有 Streamlit 进程在运行
2. 如果有，先停止旧进程
3. 启动新的 Streamlit 服务
"""

import os
import sys
import subprocess
import time

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Streamlit 默认端口
STREAMLIT_PORT = 8501


def find_streamlit_process():
    """查找已运行的 Streamlit 进程"""
    try:
        # 使用 tasklist 查找 streamlit 进程
        result = subprocess.run(
            'tasklist /FI "IMAGENAME eq python.exe" /FO CSV /NH',
            shell=True,
            capture_output=True,
            text=True,
            encoding='gbk'
        )
        
        if result.stdout:
            # 检查命令行参数中是否包含 streamlit run app.py
            result_cmd = subprocess.run(
                'wmic process where "name=\'python.exe\'" get CommandLine,ProcessId /format:csv',
                shell=True,
                capture_output=True,
                text=True,
                encoding='gbk'
            )
            
            if result_cmd.stdout:
                for line in result_cmd.stdout.strip().split('\n'):
                    if 'streamlit' in line.lower() and 'app.py' in line.lower():
                        # 提取 PID
                        parts = line.split(',')
                        for part in parts:
                            if part.isdigit():
                                return int(part)
        
        return None
        
    except Exception as e:
        print(f"[警告] 查找进程失败：{e}")
        return None


def kill_process(pid):
    """杀死指定进程"""
    try:
        print(f"[提示] 正在停止 Streamlit 进程 (PID: {pid})...")
        subprocess.run(
            f'taskkill /F /PID {pid}',
            shell=True,
            capture_output=True,
            text=True,
            encoding='gbk'
        )
        time.sleep(1)  # 等待进程完全停止
        print(f"[OK] 已停止旧进程 (PID: {pid})")
        return True
    except Exception as e:
        print(f"[警告] 停止进程失败：{e}")
        return False


def check_port_available(port):
    """检查端口是否可用"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('0.0.0.0', port))
        sock.close()
        return True
    except OSError:
        return False


def kill_process_on_port(port):
    """杀死占用端口的进程"""
    try:
        # 查找占用端口的进程
        result = subprocess.run(
            f'netstat -ano | findstr :{port}',
            shell=True,
            capture_output=True,
            text=True,
            encoding='gbk'
        )
        
        if result.stdout:
            for line in result.stdout.strip().split('\n'):
                if f':{port}' in line:
                    parts = line.split()
                    if parts[-1].isdigit():
                        pid = parts[-1]
                        print(f"[提示] 端口 {port} 被进程 {pid} 占用")
                        subprocess.run(
                            f'taskkill /F /PID {pid}',
                            shell=True,
                            capture_output=True,
                            text=True,
                            encoding='gbk'
                        )
                        print(f"[OK] 已释放端口 {port}")
                        return True
        
        return False
        
    except Exception as e:
        print(f"[警告] 无法释放端口：{e}")
        return False


def check_and_cleanup():
    """检查并清理旧进程"""
    print("=" * 60)
    print("  Streamlit 医护管理后台 - 启动检查")
    print("=" * 60)
    print()
    
    # 1. 查找 Streamlit 进程
    pid = find_streamlit_process()
    
    if pid:
        print(f"[提示] 检测到已运行的 Streamlit 进程 (PID: {pid})")
        kill_process(pid)
    else:
        print("[OK] 未检测到已运行的 Streamlit 进程")
    
    # 2. 检查端口是否被占用
    print()
    if not check_port_available(STREAMLIT_PORT):
        print(f"[提示] 端口 {STREAMLIT_PORT} 被占用，尝试释放...")
        if kill_process_on_port(STREAMLIT_PORT):
            print(f"[OK] 端口 {STREAMLIT_PORT} 已释放")
        else:
            print(f"[警告] 无法释放端口 {STREAMLIT_PORT}")
    else:
        print(f"[OK] 端口 {STREAMLIT_PORT} 可用")
    
    print()


def start_streamlit():
    """启动 Streamlit 服务"""
    print("=" * 60)
    print("  正在启动 Streamlit 应用...")
    print("=" * 60)
    print()
    print("访问地址：http://localhost:8501")
    print("按 Ctrl+C 停止服务")
    print()
    
    # 激活虚拟环境
    activate_script = os.path.join(BASE_DIR, 'venv', 'Scripts', 'activate.bat')
    
    if not os.path.exists(activate_script):
        print(f"[错误] 虚拟环境不存在：{activate_script}")
        print("请先创建虚拟环境并安装依赖")
        input("按回车键退出...")
        sys.exit(1)
    
    # 使用 subprocess 启动 streamlit
    try:
        # 启动新窗口
        subprocess.Popen(
            f'cmd /k "{activate_script} && streamlit run app.py"',
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        print("[OK] Streamlit 已在新窗口启动")
        print()
        
    except Exception as e:
        print(f"[错误] 启动失败：{e}")
        input("按回车键退出...")
        sys.exit(1)


def main():
    """主函数"""
    try:
        # 1. 检查并清理旧进程
        check_and_cleanup()
        
        # 2. 启动新服务
        start_streamlit()
        
        # 3. 倒计时关闭当前窗口
        print()
        print("=" * 60)
        print("  窗口将在 5 秒后自动关闭...")
        print("=" * 60)
        
        for i in range(5, 0, -1):
            print(f"  倒计时：{i} 秒")
            time.sleep(1)
        
        print()
        print("[OK] 窗口已关闭")
        
    except KeyboardInterrupt:
        print("\n")
        print("操作已取消")
    except Exception as e:
        print(f"\n[错误] 启动失败：{e}")
        import traceback
        traceback.print_exc()
        input("按回车键退出...")
        sys.exit(1)


if __name__ == "__main__":
    main()
