"""TimeFlow 数据模型."""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import json


@dataclass
class Session:
    """时间追踪会话模型."""
    
    id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    project: Optional[str] = None
    task: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    note: Optional[str] = None
    duration: Optional[timedelta] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典."""
        return {
            "id": self.id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "project": self.project,
            "task": self.task,
            "tags": self.tags,
            "note": self.note,
            "duration_seconds": self.duration.total_seconds() if self.duration else None,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Session":
        """从字典创建."""
        return cls(
            id=data["id"],
            start_time=datetime.fromisoformat(data["start_time"]),
            end_time=datetime.fromisoformat(data["end_time"]) if data.get("end_time") else None,
            project=data.get("project"),
            task=data.get("task"),
            tags=data.get("tags", []),
            note=data.get("note"),
            duration=timedelta(seconds=data["duration_seconds"]) if data.get("duration_seconds") else None,
        )
    
    def calculate_duration(self) -> Optional[timedelta]:
        """计算持续时间."""
        if self.end_time:
            return self.end_time - self.start_time
        return None
    
    def is_active(self) -> bool:
        """检查会话是否活跃."""
        return self.end_time is None


@dataclass
class Project:
    """项目模型."""
    
    name: str
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    total_time: timedelta = field(default_factory=timedelta)
    session_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典."""
        return {
            "name": self.name,
            "description": self.description,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "total_time_seconds": self.total_time.total_seconds(),
            "session_count": self.session_count,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Project":
        """从字典创建."""
        return cls(
            name=data["name"],
            description=data.get("description"),
            tags=data.get("tags", []),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            total_time=timedelta(seconds=data.get("total_time_seconds", 0)),
            session_count=data.get("session_count", 0),
        )


@dataclass
class DailyStats:
    """每日统计模型."""
    
    date: datetime
    total_time: timedelta
    project_times: Dict[str, timedelta] = field(default_factory=dict)
    command_count: int = 0
    session_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典."""
        return {
            "date": self.date.strftime("%Y-%m-%d"),
            "total_time_seconds": self.total_time.total_seconds(),
            "project_times": {
                k: v.total_seconds() for k, v in self.project_times.items()
            },
            "command_count": self.command_count,
            "session_count": self.session_count,
        }


@dataclass
class WeeklyReport:
    """周报告模型."""
    
    week_start: datetime
    week_end: datetime
    total_time: timedelta
    daily_breakdown: List[DailyStats] = field(default_factory=list)
    project_summary: Dict[str, timedelta] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典."""
        return {
            "week_start": self.week_start.strftime("%Y-%m-%d"),
            "week_end": self.week_end.strftime("%Y-%m-%d"),
            "total_time_seconds": self.total_time.total_seconds(),
            "daily_breakdown": [d.to_dict() for d in self.daily_breakdown],
            "project_summary": {
                k: v.total_seconds() for k, v in self.project_summary.items()
            },
        }
