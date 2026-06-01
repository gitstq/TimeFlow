"""TimeFlow TUI 应用."""

from datetime import datetime
from typing import Optional

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.reactive import reactive
from textual.widgets import (
    Header,
    Footer,
    Static,
    Button,
    DataTable,
    Label,
    ProgressBar,
    Input,
    ListView,
    ListItem,
)

from timeflow.core.tracker import TimeTracker
from timeflow.core.project import ProjectManager
from timeflow.core.report import ReportGenerator


class TimerDisplay(Static):
    """计时器显示组件."""
    
    elapsed = reactive(timedelta_zero := __import__('datetime').timedelta())
    
    def __init__(self):
        super().__init__()
        self.tracker = TimeTracker()
        self._start_time: Optional[datetime] = None
    
    def on_mount(self):
        """组件挂载时."""
        self.update_timer = self.set_interval(1, self.update_time)
        self.update_time()
    
    def update_time(self):
        """更新时间显示."""
        session = self.tracker.get_current_session()
        if session:
            duration = datetime.now() - session.start_time
            hours, remainder = divmod(int(duration.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            self.update(f"[bold green]{hours:02d}:{minutes:02d}:{seconds:02d}[/]")
        else:
            self.update("[dim]00:00:00[/]")


class StatusPanel(Static):
    """状态面板."""
    
    def compose(self) -> ComposeResult:
        """组合组件."""
        yield Label("[bold cyan]🕐 TimeFlow[/bold cyan]", id="title")
        yield Label("状态: [dim]未追踪[/dim]", id="status")
        yield TimerDisplay(id="timer")
        yield Label("", id="project")
        yield Label("", id="task")


class QuickActions(Static):
    """快速操作面板."""
    
    def compose(self) -> ComposeResult:
        """组合组件."""
        yield Button("▶️ 开始", id="btn_start", variant="success")
        yield Button("⏹️ 停止", id="btn_stop", variant="error")
        yield Button("📊 报告", id="btn_report", variant="primary")
        yield Button("📁 项目", id="btn_projects", variant="primary")


class RecentSessions(Static):
    """最近会话列表."""
    
    def compose(self) -> ComposeResult:
        """组合组件."""
        yield Label("[bold]📜 最近记录[/bold]")
        yield DataTable(id="sessions_table")
    
    def on_mount(self):
        """挂载时加载数据."""
        table = self.query_one("#sessions_table", DataTable)
        table.add_columns("时间", "项目", "任务", "时长")
        self.refresh_data()
    
    def refresh_data(self):
        """刷新数据."""
        tracker = TimeTracker()
        sessions = tracker.get_recent_sessions(10)
        
        table = self.query_one("#sessions_table", DataTable)
        table.clear()
        
        for session in sessions:
            start_str = session.start_time.strftime("%m-%d %H:%M")
            project = session.project or "未分类"
            task = session.task or "-"
            
            if session.duration:
                hours, remainder = divmod(int(session.duration.total_seconds()), 3600)
                minutes = remainder // 60
                duration_str = f"{hours}h{minutes:02d}m"
            else:
                duration_str = "进行中"
            
            table.add_row(start_str, project, task, duration_str)


class TimeFlowTUI(App):
    """TimeFlow TUI 应用."""
    
    CSS = """
    Screen {
        align: center middle;
    }
    
    #main_container {
        width: 100%;
        height: 100%;
        padding: 1;
    }
    
    #left_panel {
        width: 30%;
        height: 100%;
        border: solid green;
        padding: 1;
    }
    
    #center_panel {
        width: 40%;
        height: 100%;
        border: solid blue;
        padding: 1;
    }
    
    #right_panel {
        width: 30%;
        height: 100%;
        border: solid yellow;
        padding: 1;
    }
    
    #title {
        text-align: center;
        text-style: bold;
    }
    
    #status {
        text-align: center;
        margin: 1 0;
    }
    
    #timer {
        text-align: center;
        text-style: bold;
        color: green;
        margin: 1 0;
    }
    
    #project, #task {
        text-align: center;
        margin: 1 0;
    }
    
    Button {
        margin: 1 0;
        width: 100%;
    }
    
    DataTable {
        width: 100%;
        height: 100%;
    }
    """
    
    BINDINGS = [
        ("q", "quit", "退出"),
        ("s", "start", "开始"),
        ("e", "stop", "停止"),
        ("r", "refresh", "刷新"),
    ]
    
    def __init__(self):
        super().__init__()
        self.tracker = TimeTracker()
        self.project_manager = ProjectManager()
        self.report_generator = ReportGenerator()
    
    def compose(self) -> ComposeResult:
        """组合界面."""
        yield Header(show_clock=True)
        
        with Horizontal(id="main_container"):
            with Vertical(id="left_panel"):
                yield StatusPanel()
                yield QuickActions()
            
            with Vertical(id="center_panel"):
                yield RecentSessions()
            
            with Vertical(id="right_panel"):
                yield Label("[bold]📈 今日统计[/bold]")
                yield Label(id="today_stats")
        
        yield Footer()
    
    def on_mount(self):
        """应用挂载时."""
        self.update_status()
        self.update_today_stats()
    
    def update_status(self):
        """更新状态显示."""
        status_panel = self.query_one(StatusPanel)
        session = self.tracker.get_current_session()
        
        status_label = status_panel.query_one("#status", Label)
        project_label = status_panel.query_one("#project", Label)
        task_label = status_panel.query_one("#task", Label)
        
        if session:
            status_label.update("状态: [bold green]🟢 追踪中[/bold green]")
            project_label.update(f"项目: [cyan]{session.project or '未分类'}[/cyan]")
            task_label.update(f"任务: [yellow]{session.task or '默认任务'}[/yellow]")
        else:
            status_label.update("状态: [dim]⚪ 未追踪[/dim]")
            project_label.update("")
            task_label.update("")
    
    def update_today_stats(self):
        """更新今日统计."""
        summary = self.tracker.get_daily_summary()
        stats_label = self.query_one("#today_stats", Label)
        
        total_time = summary["total_time"]
        hours = int(total_time.total_seconds() // 3600)
        minutes = int((total_time.total_seconds() % 3600) // 60)
        
        text = f"总时长: [green]{hours}h {minutes}m[/green]\n"
        text += f"会话数: [cyan]{summary['session_count']}[/cyan]\n\n"
        
        if summary["project_times"]:
            text += "[bold]项目分布:[/bold]\n"
            for proj, time in sorted(
                summary["project_times"].items(),
                key=lambda x: x[1],
                reverse=True,
            )[:5]:
                h = int(time.total_seconds() // 3600)
                m = int((time.total_seconds() % 3600) // 60)
                text += f"  • {proj}: {h}h{m:02d}m\n"
        
        stats_label.update(text)
    
    def action_start(self):
        """开始追踪动作."""
        try:
            self.tracker.start_session()
            self.update_status()
            self.notify("✓ 开始追踪", severity="information")
        except Exception as e:
            self.notify(f"✗ {e}", severity="error")
    
    def action_stop(self):
        """停止追踪动作."""
        try:
            self.tracker.stop_session()
            self.update_status()
            
            # 刷新最近会话列表
            recent = self.query_one(RecentSessions)
            recent.refresh_data()
            
            # 刷新今日统计
            self.update_today_stats()
            
            self.notify("✓ 停止追踪", severity="information")
        except Exception as e:
            self.notify(f"✗ {e}", severity="error")
    
    def action_refresh(self):
        """刷新动作."""
        recent = self.query_one(RecentSessions)
        recent.refresh_data()
        self.update_today_stats()
        self.update_status()
        self.notify("✓ 已刷新", severity="information")
    
    def on_button_pressed(self, event: Button.Pressed):
        """按钮按下事件."""
        button_id = event.button.id
        
        if button_id == "btn_start":
            self.action_start()
        elif button_id == "btn_stop":
            self.action_stop()
        elif button_id == "btn_report":
            self.notify("报告功能开发中...", severity="information")
        elif button_id == "btn_projects":
            self.notify("项目管理功能开发中...", severity="information")
    
    def run(self):
        """运行应用."""
        super().run()
