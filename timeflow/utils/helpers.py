"""TimeFlow 辅助函数."""

import os
import subprocess
from datetime import datetime, timedelta
from typing import Optional


def format_duration(duration: Optional[timedelta]) -> str:
    """格式化持续时间."""
    if duration is None:
        return "00:00:00"
    
    total_seconds = int(duration.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def format_duration_human(duration: Optional[timedelta]) -> str:
    """格式化为人类可读的持续时间."""
    if duration is None:
        return "0分钟"
    
    total_seconds = int(duration.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}小时")
    if minutes > 0:
        parts.append(f"{minutes}分钟")
    
    return "".join(parts) if parts else "0分钟"


def format_datetime(dt: Optional[datetime]) -> str:
    """格式化日期时间."""
    if dt is None:
        return "N/A"
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def format_date(dt: Optional[datetime]) -> str:
    """格式化日期."""
    if dt is None:
        return "N/A"
    return dt.strftime("%Y-%m-%d")


def format_time(dt: Optional[datetime]) -> str:
    """格式化时间."""
    if dt is None:
        return "N/A"
    return dt.strftime("%H:%M:%S")


def get_project_from_git(path: Optional[str] = None) -> Optional[str]:
    """从Git获取项目名称."""
    try:
        if path:
            cwd = path
        else:
            cwd = os.getcwd()
        
        # 获取远程URL
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=5,
        )
        
        if result.returncode == 0:
            url = result.stdout.strip()
            # 从URL提取项目名称
            # 处理 HTTPS: https://github.com/user/repo.git
            # 处理 SSH: git@github.com:user/repo.git
            
            if ".git" in url:
                url = url.replace(".git", "")
            
            if "/" in url:
                parts = url.split("/")
                return parts[-1]
            elif ":" in url:
                parts = url.split(":")
                if "/" in parts[-1]:
                    return parts[-1].split("/")[-1]
                return parts[-1]
        
        # 如果没有远程URL，使用目录名
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=5,
        )
        
        if result.returncode == 0:
            toplevel = result.stdout.strip()
            return os.path.basename(toplevel)
        
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
        pass
    
    return None


def get_current_branch(path: Optional[str] = None) -> Optional[str]:
    """获取当前Git分支."""
    try:
        cwd = path or os.getcwd()
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=5,
        )
        
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
        pass
    
    return None


def truncate_string(s: str, max_length: int = 50) -> str:
    """截断字符串."""
    if len(s) <= max_length:
        return s
    return s[:max_length - 3] + "..."


def parse_time_string(time_str: str) -> Optional[int]:
    """解析时间字符串为秒数.
    
    支持格式:
    - 1h30m -> 5400
    - 90m -> 5400
    - 1.5h -> 5400
    """
    time_str = time_str.lower().strip()
    total_seconds = 0
    
    # 处理小时
    if "h" in time_str:
        parts = time_str.split("h")
        try:
            hours = float(parts[0])
            total_seconds += int(hours * 3600)
            time_str = parts[1] if len(parts) > 1 else ""
        except ValueError:
            return None
    
    # 处理分钟
    if "m" in time_str:
        parts = time_str.split("m")
        try:
            minutes = float(parts[0])
            total_seconds += int(minutes * 60)
        except ValueError:
            return None
    
    # 纯数字视为分钟
    if total_seconds == 0:
        try:
            total_seconds = int(float(time_str) * 60)
        except ValueError:
            return None
    
    return total_seconds


def get_terminal_size() -> tuple:
    """获取终端大小."""
    try:
        import shutil
        return shutil.get_terminal_size()
    except Exception:
        return (80, 24)


def is_interactive() -> bool:
    """检查是否在交互式环境."""
    import sys
    return sys.stdin.isatty() and sys.stdout.isatty()
