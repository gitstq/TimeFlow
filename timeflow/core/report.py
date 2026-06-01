"""TimeFlow 报告生成."""

import json
import csv
import io
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from collections import defaultdict

from timeflow.core.tracker import TimeTracker
from timeflow.core.session import SessionManager
from timeflow.core.project import ProjectManager


class ReportGenerator:
    """报告生成器."""
    
    def __init__(self):
        """初始化报告生成器."""
        self.tracker = TimeTracker()
        self.session_manager = SessionManager()
        self.project_manager = ProjectManager()
    
    def generate(
        self,
        period: str = "today",
        project: Optional[str] = None,
        format_type: str = "table",
    ) -> Any:
        """生成报告."""
        start, end = self._get_period_range(period)
        sessions = self.session_manager.get_sessions_by_period(start, end, project)
        
        # 计算统计数据
        total_time = timedelta()
        project_times = defaultdict(timedelta)
        
        for session in sessions:
            duration = session.duration
            if duration is None and session.is_active():
                duration = datetime.now() - session.start_time
            
            if duration:
                total_time += duration
                proj_name = session.project or "未分类"
                project_times[proj_name] += duration
        
        # 构建项目细分
        project_breakdown = []
        total_seconds = total_time.total_seconds()
        
        for proj, time in sorted(project_times.items(), key=lambda x: x[1], reverse=True):
            seconds = time.total_seconds()
            percentage = (seconds / total_seconds * 100) if total_seconds > 0 else 0
            
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            
            project_breakdown.append({
                "project": proj,
                "time": f"{hours}h {minutes}m",
                "seconds": seconds,
                "percentage": percentage,
            })
        
        # 格式化总时间
        total_hours = int(total_time.total_seconds() // 3600)
        total_minutes = int((total_time.total_seconds() % 3600) // 60)
        
        report = {
            "title": self._get_period_title(period),
            "period": f"{start.strftime('%Y-%m-%d')} ~ {end.strftime('%Y-%m-%d')}",
            "total_time": f"{total_hours}h {total_minutes}m",
            "total_seconds": total_time.total_seconds(),
            "project_count": len(project_times),
            "session_count": len(sessions),
            "project_breakdown": project_breakdown,
        }
        
        if format_type == "json":
            return json.dumps(report, indent=2, ensure_ascii=False)
        elif format_type == "csv":
            return self._format_csv(report)
        else:
            return report
    
    def _get_period_range(self, period: str) -> tuple:
        """获取时间范围."""
        now = datetime.now()
        
        if period == "today":
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = now
        elif period == "yesterday":
            yesterday = now - timedelta(days=1)
            start = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
            end = yesterday.replace(hour=23, minute=59, second=59)
        elif period == "week":
            start = now - timedelta(days=7)
            end = now
        elif period == "month":
            start = now - timedelta(days=30)
            end = now
        elif period == "year":
            start = now - timedelta(days=365)
            end = now
        else:
            # 默认今天
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = now
        
        return start, end
    
    def _get_period_title(self, period: str) -> str:
        """获取周期标题."""
        titles = {
            "today": "今日报告",
            "yesterday": "昨日报告",
            "week": "本周报告",
            "month": "本月报告",
            "year": "年度报告",
        }
        return titles.get(period, "自定义报告")
    
    def _format_csv(self, report: Dict[str, Any]) -> str:
        """格式化为CSV."""
        output = io.StringIO()
        writer = csv.writer(output)
        
        # 写入标题
        writer.writerow(["TimeFlow Report", report["title"]])
        writer.writerow(["Period", report["period"]])
        writer.writerow(["Total Time", report["total_time"]])
        writer.writerow(["Projects", report["project_count"]])
        writer.writerow(["Sessions", report["session_count"]])
        writer.writerow([])
        
        # 写入项目细分
        writer.writerow(["Project", "Time", "Percentage"])
        for item in report["project_breakdown"]:
            writer.writerow([
                item["project"],
                item["time"],
                f"{item['percentage']:.1f}%",
            ])
        
        return output.getvalue()
    
    def generate_weekly_report(self, week_start: Optional[datetime] = None) -> Dict[str, Any]:
        """生成周报告."""
        if week_start is None:
            # 获取本周一
            now = datetime.now()
            week_start = now - timedelta(days=now.weekday())
            week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
        
        week_end = week_start + timedelta(days=6, hours=23, minutes=59, seconds=59)
        
        # 获取每日数据
        daily_data = []
        for i in range(7):
            day = week_start + timedelta(days=i)
            summary = self.tracker.get_daily_summary(day)
            daily_data.append(summary)
        
        # 计算总计
        total_time = timedelta()
        project_summary = defaultdict(timedelta)
        
        for day_data in daily_data:
            total_time += day_data["total_time"]
            for proj, time in day_data["project_times"].items():
                project_summary[proj] += time
        
        return {
            "week_start": week_start.strftime("%Y-%m-%d"),
            "week_end": week_end.strftime("%Y-%m-%d"),
            "total_time": str(total_time),
            "daily_breakdown": daily_data,
            "project_summary": dict(project_summary),
        }
    
    def generate_project_report(self, project: str) -> Dict[str, Any]:
        """生成项目报告."""
        summary = self.tracker.get_project_summary(project)
        
        # 获取所有会话
        sessions = [
            s for s in self.session_manager._sessions
            if s.project == project
        ]
        
        # 按日期分组
        daily_times = defaultdict(timedelta)
        for session in sessions:
            date = session.start_time.strftime("%Y-%m-%d")
            duration = session.duration or timedelta()
            daily_times[date] += duration
        
        # 计算趋势
        dates = sorted(daily_times.keys())
        trend = []
        for date in dates[-7:]:  # 最近7天
            seconds = daily_times[date].total_seconds()
            hours = seconds / 3600
            trend.append({
                "date": date,
                "hours": round(hours, 2),
            })
        
        return {
            "project": project,
            "total_hours": summary["total_hours"],
            "session_count": summary["session_count"],
            "last_activity": summary["last_activity"],
            "daily_trend": trend,
            "average_daily_hours": summary["total_hours"] / len(dates) if dates else 0,
        }
    
    def export_to_json(self, filepath: str, period: str = "month") -> None:
        """导出为JSON文件."""
        report = self.generate(period, format_type="json")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(report)
    
    def export_to_csv(self, filepath: str, period: str = "month") -> None:
        """导出为CSV文件."""
        report = self.generate(period, format_type="csv")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(report)
