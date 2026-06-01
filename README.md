# 🕐 TimeFlow

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/psf/black)

**🚀 终端智能时间追踪与效率分析工具**

[简体中文](#简体中文) | [繁體中文](#繁體中文) | [English](#english)

</div>

---

## 简体中文

### 🎉 项目介绍

**TimeFlow** 是一款专为开发者打造的终端时间追踪工具，帮助您：

- 📊 **精准追踪** - 自动记录项目工作时间，无需手动切换
- 🎯 **智能分析** - 生成详细的生产力报告和趋势分析
- 🖥️ **终端优先** - 完全基于命令行，无需离开开发环境
- 🔒 **隐私保护** - 所有数据本地存储，不上传云端
- 🎨 **美观界面** - 支持TUI交互界面，体验流畅

**灵感来源**：受到 `hours`、`utt`、`terminal-wakatime` 等优秀项目的启发，TimeFlow 致力于打造一个更智能、更易用的时间追踪解决方案。

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🚀 **一键追踪** | 简单命令即可开始/停止时间追踪 |
| 🧠 **智能项目检测** | 自动识别Git项目和配置文件 |
| 📈 **多维度报告** | 日/周/月报告，支持JSON/CSV导出 |
| 🎨 **TUI界面** | 美观的终端交互界面 |
| 🔍 **时间回溯** | 查看历史记录，了解时间分配 |
| 🏷️ **标签管理** | 支持项目、任务、标签多维度分类 |
| ⚡ **高性能** | 基于SQLite本地存储，极速响应 |

### 🚀 快速开始

#### 环境要求

- Python 3.9+
- pip 或 uv

#### 安装

```bash
# 使用 pip 安装
pip install timeflow-cli

# 或使用 uv 安装
uv pip install timeflow-cli
```

#### 基础用法

```bash
# 开始追踪（自动检测项目）
timeflow start

# 开始追踪指定项目
timeflow start MyProject --task "开发新功能"

# 查看当前状态
timeflow status

# 停止追踪
timeflow stop --note "完成API接口"

# 查看今日报告
timeflow report --period today

# 启动TUI界面
timeflow tui
```

### 📖 详细使用指南

#### 命令列表

| 命令 | 说明 | 示例 |
|------|------|------|
| `start` | 开始追踪 | `timeflow start ProjectName` |
| `stop` | 停止追踪 | `timeflow stop --note "备注"` |
| `status` | 查看状态 | `timeflow status` |
| `projects` | 项目列表 | `timeflow projects --detailed` |
| `report` | 生成报告 | `timeflow report --period week` |
| `log` | 查看日志 | `timeflow log --limit 20` |
| `tui` | TUI界面 | `timeflow tui` |
| `config` | 配置管理 | `timeflow config --list` |

#### 报告周期

- `today` - 今日报告
- `yesterday` - 昨日报告
- `week` - 本周报告
- `month` - 本月报告
- `year` - 年度报告

#### 输出格式

- `table` - 表格格式（默认）
- `json` - JSON格式
- `csv` - CSV格式

### 💡 设计思路

TimeFlow 的设计理念是**"不打扰"** - 让时间追踪成为开发流程的自然组成部分，而不是额外的负担。

**核心设计原则**：
1. **零配置启动** - 开箱即用，智能检测项目
2. **终端原生** - 完全基于CLI，符合开发者习惯
3. **数据自主** - 本地存储，用户完全掌控数据
4. **模块化架构** - 核心功能与UI分离，易于扩展

### 📦 打包与部署

#### 开发环境搭建

```bash
# 克隆仓库
git clone https://github.com/gitstq/TimeFlow.git
cd TimeFlow

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -e ".[dev]"

# 运行测试
pytest
```

#### 构建发布

```bash
# 构建包
python -m build

# 上传到PyPI
python -m twine upload dist/*
```

### 🤝 贡献指南

欢迎提交 Issue 和 PR！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 📄 开源协议

本项目基于 [MIT](LICENSE) 协议开源。

---

## 繁體中文

### 🎉 專案介紹

**TimeFlow** 是一款專為開發者打造的終端時間追蹤工具，幫助您：

- 📊 **精準追蹤** - 自動記錄專案工作時間，無需手動切換
- 🎯 **智慧分析** - 生成詳細的生產力報告和趨勢分析
- 🖥️ **終端優先** - 完全基於命令列，無需離開開發環境
- 🔒 **隱私保護** - 所有資料本地儲存，不上傳雲端
- 🎨 **美觀介面** - 支援TUI互動介面，體驗流暢

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🚀 **一鍵追蹤** | 簡單命令即可開始/停止時間追蹤 |
| 🧠 **智慧專案檢測** | 自動識別Git專案和設定檔 |
| 📈 **多維度報告** | 日/週/月報告，支援JSON/CSV匯出 |
| 🎨 **TUI介面** | 美觀的終端互動介面 |
| 🔍 **時間回溯** | 檢視歷史記錄，瞭解時間分配 |
| 🏷️ **標籤管理** | 支援專案、任務、標籤多維度分類 |

### 🚀 快速開始

#### 安裝

```bash
pip install timeflow-cli
```

#### 基礎用法

```bash
# 開始追蹤
timeflow start

# 停止追蹤
timeflow stop

# 檢視報告
timeflow report

# 啟動TUI介面
timeflow tui
```

---

## English

### 🎉 Introduction

**TimeFlow** is a terminal-based time tracking tool designed for developers:

- 📊 **Accurate Tracking** - Automatically record project work time
- 🎯 **Smart Analytics** - Generate detailed productivity reports
- 🖥️ **Terminal-First** - Command-line based, no context switching
- 🔒 **Privacy-First** - All data stored locally, no cloud upload
- 🎨 **Beautiful UI** - Modern TUI interface

### ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🚀 **One-Click Tracking** | Simple commands to start/stop tracking |
| 🧠 **Smart Project Detection** | Auto-detect Git projects and config files |
| 📈 **Multi-dimensional Reports** | Daily/weekly/monthly reports with JSON/CSV export |
| 🎨 **TUI Interface** | Beautiful terminal UI |
| 🔍 **Time Travel** | View history and understand time allocation |
| 🏷️ **Tag Management** | Multi-dimensional categorization |

### 🚀 Quick Start

#### Installation

```bash
pip install timeflow-cli
```

#### Basic Usage

```bash
# Start tracking
timeflow start

# Stop tracking
timeflow stop

# View report
timeflow report

# Launch TUI
timeflow tui
```

### 📄 License

This project is licensed under the [MIT](LICENSE) License.

---

<div align="center">

**Made with ❤️ for Developers**

[GitHub](https://github.com/gitstq/TimeFlow) | [Issues](https://github.com/gitstq/TimeFlow/issues) | [Releases](https://github.com/gitstq/TimeFlow/releases)

</div>
