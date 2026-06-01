"""TimeFlow 会话管理."""

import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import asdict

from timeflow.core.models import Session
from timeflow.core.config import Config


class SessionManager:
    """会话管理器."""
    
    def __init__(self):
        """初始化会话管理器."""
        self.config = Config()
        self.sessions_file = self.config.get_sessions_file()
        self._sessions: List[Session] = []
        self._current_session: Optional[Session] = None
        self._load_sessions()
    
    def _load_sessions(self) -> None:
        """加载会话数据."""
        if self.sessions_file.exists():
            try:
                with open(self.sessions_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._sessions = [Session.from_dict(s) for s in data]
            except (json.JSONDecodeError, IOError, KeyError):
                self._sessions = []
        
        # 检查是否有活跃的会话
        for session in self._sessions:
            if session.is_active():
                self._current_session = session
                break
    
    def _save_sessions(self) -> None:
        """保存会话数据."""
        data = [s.to_dict() for s in self._sessions]
        with open(self.sessions_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def create_session(
        self,
        project: Optional[str] = None,
        task: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> Session:
        """创建新会话."""
        if self._current_session:
            raise ValueError("已有进行中的会话，请先停止当前会话")
        
        session = Session(
            id=str(uuid.uuid4())[:8],
            start_time=datetime.now(),
            project=project,
            task=task,
            tags=tags or [],
        )
        
        self._sessions.append(session)
        self._current_session = session
        self._save_sessions()
        
        return session
    
    def stop_current_session(self, note: Optional[str] = None) -> Session:
        """停止当前会话."""
        if not self._current_session:
            raise ValueError("没有进行中的会话")
        
        session = self._current_session
        session.end_time = datetime.now()
        session.note = note
        session.duration = session.calculate_duration()
        
        self._current_session = None
        self._save_sessions()
        
        return session
    
    def get_current_session(self) -> Optional[Session]:
        """获取当前会话."""
        return self._current_session
    
    def get_recent_sessions(
        self,
        limit: int = 10,
        project: Optional[str] = None,
    ) -> List[Session]:
        """获取最近的会话."""
        sessions = sorted(
            self._sessions,
            key=lambda s: s.start_time,
            reverse=True,
        )
        
        if project:
            sessions = [s for s in sessions if s.project == project]
        
        return sessions[:limit]
    
    def get_sessions_by_date(
        self,
        date: datetime,
        project: Optional[str] = None,
    ) -> List[Session]:
        """获取指定日期的会话."""
        sessions = []
        for session in self._sessions:
            if session.start_time.date() == date.date():
                if project is None or session.project == project:
                    sessions.append(session)
        return sessions
    
    def get_sessions_by_period(
        self,
        start: datetime,
        end: datetime,
        project: Optional[str] = None,
    ) -> List[Session]:
        """获取指定时间段的会话."""
        sessions = []
        for session in self._sessions:
            if start <= session.start_time <= end:
                if project is None or session.project == project:
                    sessions.append(session)
        return sessions
    
    def get_total_time(
        self,
        project: Optional[str] = None,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ) -> timedelta:
        """获取总时间."""
        total = timedelta()
        
        for session in self._sessions:
            if project and session.project != project:
                continue
            if start and session.start_time < start:
                continue
            if end and session.start_time > end:
                continue
            
            if session.duration:
                total += session.duration
            elif session.is_active():
                total += datetime.now() - session.start_time
        
        return total
    
    def delete_session(self, session_id: str) -> bool:
        """删除会话."""
        for i, session in enumerate(self._sessions):
            if session.id == session_id:
                if session.is_active():
                    self._current_session = None
                del self._sessions[i]
                self._save_sessions()
                return True
        return False
    
    def get_all_projects(self) -> List[str]:
        """获取所有项目列表."""
        projects = set()
        for session in self._sessions:
            if session.project:
                projects.add(session.project)
        return sorted(list(projects))
    
    def get_project_stats(self, project: str) -> Dict[str, Any]:
        """获取项目统计."""
        sessions = [s for s in self._sessions if s.project == project]
        total_time = timedelta()
        
        for session in sessions:
            if session.duration:
                total_time += session.duration
            elif session.is_active():
                total_time += datetime.now() - session.start_time
        
        last_activity = None
        if sessions:
            last_session = max(sessions, key=lambda s: s.start_time)
            last_activity = last_session.start_time.strftime("%Y-%m-%d %H:%M")
        
        return {
            "total_hours": total_time.total_seconds() / 3600,
            "session_count": len(sessions),
            "last_activity": last_activity,
        }
