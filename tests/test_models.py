"""测试数据模型."""

import pytest
from datetime import datetime, timedelta

from timeflow.core.models import Session, Project, DailyStats


class TestSession:
    """测试 Session 模型."""
    
    def test_session_creation(self):
        """测试会话创建."""
        session = Session(
            id="test123",
            start_time=datetime(2025, 1, 1, 10, 0, 0),
            project="TestProject",
            task="TestTask",
            tags=["tag1", "tag2"],
        )
        
        assert session.id == "test123"
        assert session.project == "TestProject"
        assert session.task == "TestTask"
        assert len(session.tags) == 2
        assert session.is_active()
    
    def test_session_duration(self):
        """测试会话持续时间计算."""
        start = datetime(2025, 1, 1, 10, 0, 0)
        end = datetime(2025, 1, 1, 11, 30, 0)
        
        session = Session(
            id="test123",
            start_time=start,
            end_time=end,
        )
        session.duration = session.calculate_duration()
        
        assert session.duration == timedelta(hours=1, minutes=30)
        assert not session.is_active()
    
    def test_session_to_dict(self):
        """测试会话序列化."""
        session = Session(
            id="test123",
            start_time=datetime(2025, 1, 1, 10, 0, 0),
            project="TestProject",
            tags=["tag1"],
        )
        
        data = session.to_dict()
        
        assert data["id"] == "test123"
        assert data["project"] == "TestProject"
        assert data["tags"] == ["tag1"]
        assert "start_time" in data
    
    def test_session_from_dict(self):
        """测试会话反序列化."""
        data = {
            "id": "test123",
            "start_time": "2025-01-01T10:00:00",
            "end_time": "2025-01-01T11:00:00",
            "project": "TestProject",
            "task": "TestTask",
            "tags": ["tag1"],
            "note": "Test note",
            "duration_seconds": 3600,
        }
        
        session = Session.from_dict(data)
        
        assert session.id == "test123"
        assert session.project == "TestProject"
        assert session.duration == timedelta(hours=1)


class TestProject:
    """测试 Project 模型."""
    
    def test_project_creation(self):
        """测试项目创建."""
        project = Project(
            name="TestProject",
            description="Test description",
            tags=["python", "cli"],
        )
        
        assert project.name == "TestProject"
        assert project.description == "Test description"
        assert len(project.tags) == 2
        assert project.session_count == 0
    
    def test_project_to_dict(self):
        """测试项目序列化."""
        project = Project(
            name="TestProject",
            description="Test description",
            tags=["tag1"],
        )
        
        data = project.to_dict()
        
        assert data["name"] == "TestProject"
        assert data["description"] == "Test description"
        assert "created_at" in data
    
    def test_project_from_dict(self):
        """测试项目反序列化."""
        data = {
            "name": "TestProject",
            "description": "Test description",
            "tags": ["tag1"],
            "created_at": "2025-01-01T10:00:00",
            "updated_at": "2025-01-01T10:00:00",
            "total_time_seconds": 3600,
            "session_count": 5,
        }
        
        project = Project.from_dict(data)
        
        assert project.name == "TestProject"
        assert project.total_time == timedelta(hours=1)
        assert project.session_count == 5


class TestDailyStats:
    """测试 DailyStats 模型."""
    
    def test_daily_stats_creation(self):
        """测试每日统计创建."""
        stats = DailyStats(
            date=datetime(2025, 1, 1),
            total_time=timedelta(hours=8),
            command_count=100,
            session_count=5,
        )
        
        assert stats.date == datetime(2025, 1, 1)
        assert stats.total_time == timedelta(hours=8)
        assert stats.command_count == 100
        assert stats.session_count == 5
    
    def test_daily_stats_to_dict(self):
        """测试每日统计序列化."""
        stats = DailyStats(
            date=datetime(2025, 1, 1),
            total_time=timedelta(hours=8),
            project_times={"ProjectA": timedelta(hours=4)},
        )
        
        data = stats.to_dict()
        
        assert data["date"] == "2025-01-01"
        assert data["total_time_seconds"] == 28800
        assert "ProjectA" in data["project_times"]
