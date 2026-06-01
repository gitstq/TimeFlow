"""TimeFlow 项目管理."""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

from timeflow.core.models import Project
from timeflow.core.config import Config


class ProjectManager:
    """项目管理器."""
    
    def __init__(self):
        """初始化项目管理器."""
        self.config = Config()
        self.projects_file = self.config.get_projects_file()
        self._projects: Dict[str, Project] = {}
        self._load_projects()
    
    def _load_projects(self) -> None:
        """加载项目数据."""
        if self.projects_file.exists():
            try:
                with open(self.projects_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for name, proj_data in data.items():
                        self._projects[name] = Project.from_dict(proj_data)
            except (json.JSONDecodeError, IOError, KeyError):
                self._projects = {}
    
    def _save_projects(self) -> None:
        """保存项目数据."""
        data = {name: proj.to_dict() for name, proj in self._projects.items()}
        with open(self.projects_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def create_project(
        self,
        name: str,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> Project:
        """创建新项目."""
        if name in self._projects:
            raise ValueError(f"项目 '{name}' 已存在")
        
        project = Project(
            name=name,
            description=description,
            tags=tags or [],
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        
        self._projects[name] = project
        self._save_projects()
        
        return project
    
    def get_project(self, name: str) -> Optional[Project]:
        """获取项目."""
        return self._projects.get(name)
    
    def update_project(
        self,
        name: str,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> Optional[Project]:
        """更新项目."""
        if name not in self._projects:
            return None
        
        project = self._projects[name]
        if description is not None:
            project.description = description
        if tags is not None:
            project.tags = tags
        
        project.updated_at = datetime.now()
        self._save_projects()
        
        return project
    
    def delete_project(self, name: str) -> bool:
        """删除项目."""
        if name in self._projects:
            del self._projects[name]
            self._save_projects()
            return True
        return False
    
    def list_projects(self) -> List[Project]:
        """列出所有项目."""
        return sorted(self._projects.values(), key=lambda p: p.name)
    
    def get_or_create_project(self, name: str) -> Project:
        """获取或创建项目."""
        if name in self._projects:
            return self._projects[name]
        return self.create_project(name)
    
    def update_project_time(
        self,
        name: str,
        duration_seconds: float,
        increment_session: bool = True,
    ) -> None:
        """更新项目时间统计."""
        if name not in self._projects:
            self.create_project(name)
        
        from datetime import timedelta
        project = self._projects[name]
        project.total_time += timedelta(seconds=duration_seconds)
        if increment_session:
            project.session_count += 1
        project.updated_at = datetime.now()
        
        self._save_projects()
    
    def get_project_stats(self, name: str) -> Dict[str, Any]:
        """获取项目统计."""
        from datetime import timedelta
        
        if name not in self._projects:
            return {
                "total_hours": 0,
                "session_count": 0,
                "last_activity": None,
            }
        
        project = self._projects[name]
        total_hours = project.total_time.total_seconds() / 3600
        
        return {
            "total_hours": total_hours,
            "session_count": project.session_count,
            "last_activity": project.updated_at.strftime("%Y-%m-%d %H:%M"),
        }
    
    def search_projects(self, query: str) -> List[Project]:
        """搜索项目."""
        query = query.lower()
        results = []
        
        for project in self._projects.values():
            if query in project.name.lower():
                results.append(project)
            elif project.description and query in project.description.lower():
                results.append(project)
            elif any(query in tag.lower() for tag in project.tags):
                results.append(project)
        
        return sorted(results, key=lambda p: p.name)
    
    def detect_project_from_path(self, path: Optional[str] = None) -> Optional[str]:
        """从路径检测项目."""
        import os
        from pathlib import Path
        
        if path is None:
            path = os.getcwd()
        
        path_obj = Path(path)
        
        # 尝试从Git仓库获取项目名称
        git_dir = path_obj / ".git"
        if git_dir.exists():
            try:
                config_file = git_dir / "config"
                if config_file.exists():
                    content = config_file.read_text()
                    for line in content.split("\n"):
                        if "url" in line.lower():
                            # 从URL提取项目名称
                            parts = line.split("/")
                            if parts:
                                name = parts[-1].replace(".git", "").strip()
                                if name:
                                    return name
            except IOError:
                pass
        
        # 使用目录名作为项目名
        return path_obj.name
    
    def detect_project_from_files(self, path: Optional[str] = None) -> Optional[str]:
        """从配置文件检测项目."""
        import os
        from pathlib import Path
        
        if path is None:
            path = os.getcwd()
        
        path_obj = Path(path)
        
        # 检查常见的项目配置文件
        config_files = {
            "package.json": lambda p: self._read_json_field(p, "name"),
            "pyproject.toml": lambda p: self._read_toml_field(p, "project", "name"),
            "Cargo.toml": lambda p: self._read_toml_field(p, "package", "name"),
            "pom.xml": lambda p: self._read_xml_field(p, "artifactId"),
            "build.gradle": lambda p: self._read_gradle_field(p, "rootProject.name"),
        }
        
        for filename, extractor in config_files.items():
            file_path = path_obj / filename
            if file_path.exists():
                try:
                    name = extractor(file_path)
                    if name:
                        return name
                except Exception:
                    continue
        
        return None
    
    def _read_json_field(self, path: Path, field: str) -> Optional[str]:
        """读取JSON字段."""
        import json
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get(field)
        except (json.JSONDecodeError, IOError):
            return None
    
    def _read_toml_field(self, path: Path, section: str, field: str) -> Optional[str]:
        """读取TOML字段."""
        try:
            content = path.read_text()
            in_section = False
            for line in content.split("\n"):
                stripped = line.strip()
                if stripped == f"[{section}]":
                    in_section = True
                elif stripped.startswith("[") and stripped.endswith("]"):
                    in_section = False
                elif in_section and stripped.startswith(f"{field} ="):
                    value = stripped.split("=", 1)[1].strip().strip('"').strip("'")
                    return value
        except IOError:
            pass
        return None
    
    def _read_xml_field(self, path: Path, field: str) -> Optional[str]:
        """读取XML字段."""
        try:
            content = path.read_text()
            import re
            pattern = f"<{field}>([^<]+)</{field}>"
            match = re.search(pattern, content)
            if match:
                return match.group(1).strip()
        except IOError:
            pass
        return None
    
    def _read_gradle_field(self, path: Path, field: str) -> Optional[str]:
        """读取Gradle字段."""
        try:
            content = path.read_text()
            import re
            pattern = f'{field}\\s*=\\s*["\']([^"\']+)["\']'
            match = re.search(pattern, content)
            if match:
                return match.group(1).strip()
        except IOError:
            pass
        return None
