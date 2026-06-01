# 🤝 贡献指南

感谢您对 TimeFlow 项目的关注！我们欢迎各种形式的贡献。

## 📋 贡献方式

### 1. 提交 Issue

- 🐛 **Bug 报告** - 如果发现bug，请提交Issue并描述复现步骤
- 💡 **功能建议** - 有新功能想法？欢迎提交Feature Request
- 📖 **文档改进** - 发现文档问题或可以改进的地方

### 2. 提交 Pull Request

#### 开发流程

1. **Fork 仓库**
   ```bash
   git clone https://github.com/your-username/TimeFlow.git
   cd TimeFlow
   ```

2. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/bug-description
   ```

3. **安装开发依赖**
   ```bash
   pip install -e ".[dev]"
   ```

4. **编写代码**
   - 遵循 PEP 8 规范
   - 添加类型注解
   - 编写测试用例

5. **代码检查**
   ```bash
   # 格式化代码
   black timeflow tests
   
   # 代码检查
   ruff check timeflow tests
   
   # 类型检查
   mypy timeflow
   
   # 运行测试
   pytest
   ```

6. **提交更改**
   ```bash
   git add .
   git commit -m "feat: 描述你的更改"
   git push origin feature/your-feature-name
   ```

7. **创建 Pull Request**
   - 填写清晰的标题和描述
   - 关联相关的 Issue
   - 等待代码审查

## 📝 提交规范

我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

| 类型 | 说明 |
|------|------|
| `feat:` | 新功能 |
| `fix:` | Bug修复 |
| `docs:` | 文档更新 |
| `style:` | 代码格式（不影响功能） |
| `refactor:` | 代码重构 |
| `test:` | 测试相关 |
| `chore:` | 构建/工具相关 |

### 示例

```
feat: 添加番茄工作法支持

- 实现25分钟工作计时
- 添加休息提醒功能
- 更新文档

Closes #123
```

## 🎯 代码规范

### Python 代码风格

- 使用 **Black** 格式化代码
- 使用 **Ruff** 进行代码检查
- 使用 **MyPy** 进行类型检查
- 最大行长度：100字符

### 文档字符串

使用 Google 风格的文档字符串：

```python
def function_name(param1: str, param2: int) -> bool:
    """简短描述。
    
    详细描述（可选）。
    
    Args:
        param1: 参数1说明
        param2: 参数2说明
        
    Returns:
        返回值说明
        
    Raises:
        ValueError: 异常说明
    """
    pass
```

## 🧪 测试要求

- 新功能必须包含测试用例
- 测试覆盖率应保持在 80% 以上
- 使用 pytest 编写测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_tracker.py

# 生成覆盖率报告
pytest --cov=timeflow --cov-report=html
```

## 📚 文档要求

- 更新 README.md（如需要）
- 添加/更新 API 文档
- 更新 CHANGELOG.md

## 🎨 TUI 开发指南

如果使用 Textual 开发 TUI：

1. 遵循 Textual 组件设计模式
2. 保持界面简洁美观
3. 支持键盘导航
4. 添加适当的帮助提示

## 💬 沟通方式

- GitHub Issues - 功能讨论、Bug报告
- Pull Request - 代码审查、技术讨论

## ⚖️ 行为准则

- 尊重他人，保持友善
- 接受建设性批评
- 关注社区最佳利益

## 🙏 感谢

再次感谢您的贡献！
