"""TimeFlow 配置管理."""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
from platformdirs import user_config_dir, user_data_dir


class Config:
    """配置管理类."""
    
    APP_NAME = "timeflow"
    APP_AUTHOR = "timeflow"
    
    DEFAULT_CONFIG = {
        "auto_track": True,
        "idle_threshold": 300,  # 5分钟无操作视为空闲
        "pomodoro_duration": 25,  # 番茄钟时长（分钟）
        "pomodoro_break": 5,  # 休息时长（分钟）
        "data_format": "json",
        "default_project": None,
        "theme": "default",
        "enable_notifications": True,
        "track_commands": True,
        "track_directories": True,
    }
    
    def __init__(self):
        """初始化配置."""
        self.config_dir = Path(user_config_dir(self.APP_NAME, self.APP_AUTHOR))
        self.data_dir = Path(user_data_dir(self.APP_NAME, self.APP_AUTHOR))
        self.config_file = self.config_dir / "config.json"
        
        # 确保目录存在
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置."""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    # 合并默认配置
                    merged = self.DEFAULT_CONFIG.copy()
                    merged.update(config)
                    return merged
            except (json.JSONDecodeError, IOError):
                return self.DEFAULT_CONFIG.copy()
        return self.DEFAULT_CONFIG.copy()
    
    def _save_config(self) -> None:
        """保存配置."""
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self._config, f, indent=2, ensure_ascii=False)
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项."""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """设置配置项."""
        self._config[key] = value
        self._save_config()
    
    def get_all(self) -> Dict[str, Any]:
        """获取所有配置."""
        return self._config.copy()
    
    def reset(self) -> None:
        """重置为默认配置."""
        self._config = self.DEFAULT_CONFIG.copy()
        self._save_config()
    
    def get_data_dir(self) -> Path:
        """获取数据目录."""
        return self.data_dir
    
    def get_sessions_file(self) -> Path:
        """获取会话数据文件路径."""
        return self.data_dir / "sessions.json"
    
    def get_projects_file(self) -> Path:
        """获取项目数据文件路径."""
        return self.data_dir / "projects.json"
    
    def get_stats_file(self) -> Path:
        """获取统计数据文件路径."""
        return self.data_dir / "stats.json"
