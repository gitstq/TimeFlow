"""TimeFlow CLI 主入口模块."""

from typing import Optional
from datetime import datetime, timedelta

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

from timeflow.core.tracker import TimeTracker
from timeflow.core.project import ProjectManager
from timeflow.core.report import ReportGenerator
from timeflow.core.config import Config
from timeflow.tui.app import TimeFlowTUI

app = typer.Typer(
    name="timeflow",
    help="🕐 TimeFlow - 终端智能时间追踪与效率分析工具",
    add_completion=False,
    rich_markup_mode="rich",
)
console = Console()

# 全局选项
@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None, "--version", "-v", help="显示版本信息", is_eager=True
    ),
) -> None:
    """TimeFlow - 终端智能时间追踪与效率分析工具."""
    if version:
        from timeflow import __version__
        console.print(f"[bold cyan]TimeFlow[/bold cyan] 版本: [green]{__version__}[/green]")
        raise typer.Exit()


@app.command(name="start")
def start_tracking(
    project: Optional[str] = typer.Argument(None, help="项目名称"),
    task: Optional[str] = typer.Option(None, "--task", "-t", help="任务名称"),
    tags: Optional[str] = typer.Option(None, "--tags", help="标签（逗号分隔）"),
) -> None:
    """🚀 开始时间追踪."""
    tracker = TimeTracker()
    tag_list = tags.split(",") if tags else []
    
    try:
        session = tracker.start_session(project, task, tag_list)
        project_name = session.project or "未分类"
        task_name = session.task or "默认任务"
        
        console.print(Panel(
            f"[bold green]✓ 开始追踪[/bold green]\n"
            f"项目: [cyan]{project_name}[/cyan]\n"
            f"任务: [yellow]{task_name}[/yellow]\n"
            f"开始时间: [dim]{session.start_time.strftime('%Y-%m-%d %H:%M:%S')}[/dim]",
            title="🕐 TimeFlow",
            border_style="green",
        ))
    except Exception as e:
        console.print(f"[bold red]✗ 错误:[/bold red] {e}")
        raise typer.Exit(1)


@app.command(name="stop")
def stop_tracking(
    note: Optional[str] = typer.Option(None, "--note", "-n", help="备注信息"),
) -> None:
    """⏹️ 停止时间追踪."""
    tracker = TimeTracker()
    
    try:
        session = tracker.stop_session(note)
        duration = session.duration
        
        if duration:
            hours, remainder = divmod(int(duration.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            duration_str = "未知"
        
        console.print(Panel(
            f"[bold yellow]⏹️ 停止追踪[/bold yellow]\n"
            f"项目: [cyan]{session.project or '未分类'}[/cyan]\n"
            f"任务: [yellow]{session.task or '默认任务'}[/yellow]\n"
            f"持续时间: [green]{duration_str}[/green]\n"
            f"结束时间: [dim]{session.end_time.strftime('%Y-%m-%d %H:%M:%S') if session.end_time else 'N/A'}[/dim]",
            title="🕐 TimeFlow",
            border_style="yellow",
        ))
    except Exception as e:
        console.print(f"[bold red]✗ 错误:[/bold red] {e}")
        raise typer.Exit(1)


@app.command(name="status")
def show_status() -> None:
    """📊 显示当前追踪状态."""
    tracker = TimeTracker()
    session = tracker.get_current_session()
    
    if session:
        duration = datetime.now() - session.start_time
        hours, remainder = divmod(int(duration.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        console.print(Panel(
            f"[bold green]🟢 追踪中[/bold green]\n"
            f"项目: [cyan]{session.project or '未分类'}[/cyan]\n"
            f"任务: [yellow]{session.task or '默认任务'}[/yellow]\n"
            f"已用时: [green]{hours:02d}:{minutes:02d}:{seconds:02d}[/green]\n"
            f"开始时间: [dim]{session.start_time.strftime('%Y-%m-%d %H:%M:%S')}[/dim]",
            title="🕐 TimeFlow",
            border_style="green",
        ))
    else:
        console.print(Panel(
            "[bold dim]⚪ 未追踪[/bold dim]\n"
            "当前没有进行中的时间追踪\n"
            "使用 [cyan]timeflow start[/cyan] 开始追踪",
            title="🕐 TimeFlow",
            border_style="dim",
        ))


@app.command(name="projects")
def list_projects(
    detailed: bool = typer.Option(False, "--detailed", "-d", help="显示详细信息"),
) -> None:
    """📁 列出所有项目."""
    pm = ProjectManager()
    projects = pm.list_projects()
    
    if not projects:
        console.print("[yellow]暂无项目，开始追踪时会自动创建。[/yellow]")
        return
    
    table = Table(
        title="📁 项目列表",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan",
    )
    table.add_column("项目名称", style="cyan")
    table.add_column("总时长", style="green")
    table.add_column("会话数", style="yellow")
    
    if detailed:
        table.add_column("最后活动", style="dim")
        table.add_column("标签", style="magenta")
    
    for proj in projects:
        stats = pm.get_project_stats(proj.name)
        total_hours = stats.get("total_hours", 0)
        session_count = stats.get("session_count", 0)
        
        hours = int(total_hours)
        minutes = int((total_hours - hours) * 60)
        
        row = [
            proj.name,
            f"{hours}h {minutes}m",
            str(session_count),
        ]
        
        if detailed:
            last_activity = stats.get("last_activity", "从未")
            tags = ", ".join(proj.tags) if proj.tags else "无"
            row.extend([last_activity, tags])
        
        table.add_row(*row)
    
    console.print(table)


@app.command(name="report")
def generate_report(
    period: str = typer.Option("today", "--period", "-p", help="报告周期 (today/week/month/year)"),
    project: Optional[str] = typer.Option(None, "--project", help="指定项目"),
    format_type: str = typer.Option("table", "--format", "-f", help="输出格式 (table/json/csv)"),
) -> None:
    """📈 生成时间报告."""
    rg = ReportGenerator()
    
    try:
        report = rg.generate(period, project, format_type)
        
        if format_type == "json":
            console.print(report)
        elif format_type == "csv":
            console.print(report)
        else:
            # 表格格式
            console.print(Panel(
                f"[bold cyan]📈 {report['title']}[/bold cyan]\n"
                f"周期: [yellow]{report['period']}[/yellow]\n"
                f"总时长: [green]{report['total_time']}[/green]\n"
                f"项目数: [cyan]{report['project_count']}[/cyan]\n"
                f"会话数: [magenta]{report['session_count']}[/magenta]",
                border_style="cyan",
            ))
            
            if report.get("project_breakdown"):
                table = Table(title="项目详情", box=box.ROUNDED)
                table.add_column("项目", style="cyan")
                table.add_column("时长", style="green")
                table.add_column("占比", style="yellow")
                
                for item in report["project_breakdown"]:
                    table.add_row(
                        item["project"],
                        item["time"],
                        f"{item['percentage']:.1f}%"
                    )
                
                console.print(table)
    except Exception as e:
        console.print(f"[bold red]✗ 错误:[/bold red] {e}")
        raise typer.Exit(1)


@app.command(name="log")
def show_log(
    limit: int = typer.Option(10, "--limit", "-n", help="显示条目数"),
    project: Optional[str] = typer.Option(None, "--project", "-p", help="筛选项目"),
) -> None:
    """📜 查看追踪日志."""
    tracker = TimeTracker()
    sessions = tracker.get_recent_sessions(limit, project)
    
    if not sessions:
        console.print("[yellow]暂无追踪记录。[/yellow]")
        return
    
    table = Table(
        title=f"📜 最近 {len(sessions)} 条记录",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan",
    )
    table.add_column("时间", style="dim", width=16)
    table.add_column("项目", style="cyan")
    table.add_column("任务", style="yellow")
    table.add_column("时长", style="green")
    table.add_column("备注", style="white")
    
    for session in sessions:
        start_str = session.start_time.strftime("%m-%d %H:%M")
        
        if session.duration:
            hours, remainder = divmod(int(session.duration.total_seconds()), 3600)
            minutes = remainder // 60
            duration_str = f"{hours}h{minutes:02d}m"
        else:
            duration_str = "进行中"
        
        table.add_row(
            start_str,
            session.project or "未分类",
            session.task or "-",
            duration_str,
            session.note or "",
        )
    
    console.print(table)


@app.command(name="tui")
def launch_tui() -> None:
    """🖥️ 启动交互式 TUI 界面."""
    try:
        tui = TimeFlowTUI()
        tui.run()
    except Exception as e:
        console.print(f"[bold red]✗ TUI 启动失败:[/bold red] {e}")
        console.print("[dim]尝试使用命令行模式: timeflow --help[/dim]")
        raise typer.Exit(1)


@app.command(name="config")
def manage_config(
    key: Optional[str] = typer.Argument(None, help="配置项名称"),
    value: Optional[str] = typer.Argument(None, help="配置值"),
    list_all: bool = typer.Option(False, "--list", "-l", help="列出所有配置"),
) -> None:
    """⚙️ 管理配置."""
    config = Config()
    
    if list_all:
        settings = config.get_all()
        table = Table(title="⚙️ 配置项", box=box.ROUNDED)
        table.add_column("配置项", style="cyan")
        table.add_column("值", style="green")
        
        for k, v in settings.items():
            table.add_row(k, str(v))
        
        console.print(table)
    elif key and value:
        config.set(key, value)
        console.print(f"[green]✓ 已设置 {key} = {value}[/green]")
    elif key:
        val = config.get(key)
        console.print(f"[cyan]{key}[/cyan] = [green]{val}[/green]")
    else:
        console.print("[yellow]请提供配置项或使用 --list 查看所有配置[/yellow]")


if __name__ == "__main__":
    app()
