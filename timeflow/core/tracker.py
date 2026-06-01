"""TimeFlow 追踪器主类."""

from typing import List, Optional
from datetime import datetime, timedelta

from timeflow.core.session import SessionManager
from timeflow.core.project import ProjectManager
from timeflow.core.config import Config
from timeflow.core.models import Session


class TimeTracker:
    """时间追踪器主类."""
    
    def __init__(self, config: Optional[Config] = None):
        """初始化追踪器."""
        self.config = config or Config()
        self.session_manager = SessionManager(self.config)
        self.project_manager = ProjectManager(self.config)
    
    def start_session(
        self,
        project: Optional[str] = None,
        task: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> Session:
        """开始新会话."""
        # 如果没有指定项目，尝试自动检测
        if project is None:
            project = self._detect_project()
        
        # 确保项目存在
        if project:
            self.project_manager.get_or_create_project(project)
        
        return self.session_manager.create_session(project, task, tags)
    
    def stop_session(self, note: Optional[str] = None) -> Session:
        """停止当前会话."""
        session = self.session_manager.stop_current_session(note)
        
        # 更新项目统计
        if session.project and session.duration:
            self.project_manager.update_project_time(
                session.project,
                session.duration.total_seconds(),
            )
        
        return session
    
    def get_current_session(self) -> Optional[Session]:
        """获取当前会话."""
        return self.session_manager.get_current_session()
    
    def get_recent_sessions(
        self,
        limit: int = 10,
        project: Optional[str] = None,
    ) -> List[Session]:
        """获取最近的会话."""
        return self.session_manager.get_recent_sessions(limit, project)
    
    def is_tracking(self) -> bool:
        """检查是否正在追踪."""
        return self.session_manager.get_current_session() is not None
    
    def get_current_duration(self) -> Optional[timedelta]:
        """获取当前会话持续时间."""
        session = self.session_manager.get_current_session()
        if session:
            return datetime.now() - session.start_time
        return None
    
    def _detect_project(self) -> Optional[str]:
        """自动检测项目."""
        # 首先尝试从配置文件检测
        project = self.project_manager.detect_project_from_files()
        if project:
            return project
        
        # 然后尝试从Git检测
        project = self.project_manager.detect_project_from_path()
        if project:
            return project
        
        return None
    
    def switch_project(self, new_project: str) -> Session:
        """切换到新项目."""
        # 停止当前会话
        if self.is_tracking():
            self.stop_session("切换项目")
        
        # 开始新会话
        return self.start_session(project=new_project)
    
    def switch_task(self, new_task: str) -> Session:
        """切换到新任务."""
        current = self.get_current_session()
        project = current.project if current else None
        
        # 停止当前会话
        if self.is_tracking():
            self.stop_session("切换任务")
        
        # 开始新会话
        return self.start_session(project=project, task=new_task)
    
    def get_daily_summary(self, date: Optional[datetime] = None) -> dict:
        """获取每日摘要."""
        if date is None:
            date = datetime.now()
        
        sessions = self.session_manager.get_sessions_by_date(date)
        
        total_time = timedelta()
        project_times = {}
        
        for session in sessions:
            duration = session.duration
            if duration is None and session.is_active():
                duration = datetime.now() - session.start_time
            
            if duration:
                total_time += duration
                
                project = session.project or "未分类"
                if project not in project_times:
                    project_times[project] = timedelta()
                project_times[project] += duration
        
        return {
            "date": date.strftime("%Y-%m-%d"),
            "total_time": total_time,
            "session_count": len(sessions),
            "project_times": project_times,
        }
    
    def get_project_summary(self, project: str) -> dict:
        """获取项目摘要."""
        stats = self.project_manager.get_project_stats(project)
        sessions = [
            s for s in self.session_manager._sessions
            if s.project == project
        ]
        
        recent_sessions = sorted(
            sessions,
            key=lambda s: s.start_time,
            reverse=True,
        )[:5]
        
        return {
            "project": project,
            "total_hours": stats.get("total_hours", 0),
            "session_count": stats.get("session_count", 0),
            "last_activity": stats.get("last_activity"),
            "recent_sessions": [
                {
                    "date": s.start_time.strftime("%Y-%m-%d"),
                    "task": s.task,
                    "duration": str(s.duration) if s.duration else "进行中",
                }
                for s in recent_sessions
            ],
        }
