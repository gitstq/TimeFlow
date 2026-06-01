"""TimeFlow - 终端智能时间追踪与效率分析工具.

🕐 TimeFlow 是一个为开发者设计的终端时间追踪工具，帮助您：
- 自动追踪项目工作时间
- 分析终端使用习惯
- 生成生产力报告
- 管理任务与项目

Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "TimeFlow Team"
__email__ = "timeflow@example.com"
__license__ = "MIT"

from timeflow.core.tracker import TimeTracker
from timeflow.core.project import ProjectManager
from timeflow.core.session import SessionManager

__all__ = [
    "TimeTracker",
    "ProjectManager", 
    "SessionManager",
]
