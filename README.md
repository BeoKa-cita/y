# CrewAI 多 Agent 协作 Demo

一个基于 [CrewAI](https://github.com/joaomdmoura/crewAI) 的多 Agent 协作项目，演示多个 AI 角色分工合作完成代码任务。

## 快速开始

```bash
# 1. 安装依赖
pip install crewai litellm

# 2. 配置 API Key（DeepSeek / OpenAI 兼容接口）
export OPENAI_API_KEY="sk-xxx"
export OPENAI_BASE_URL="https://api.deepseek.com"

# 3. 运行
python crewai_demo.py
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `crewai_demo.py` | CrewAI 层级模式 Demo，多个 Agent 协作写代码 |
| `crewai_feishu.py` | 飞书集成版，支持命令行传参指定需求 |
| `tic_tac_toe.py` | 井字棋双人对战游戏（CrewAI 生成） |
| `tests/test_tic_tac_toe.py` | 单元测试（18 项） |
| `.env.example` | 环境变量配置模板 |

## 多 Agent 协作流程

```
你提需求
    → 技术分析师 分析可行性
    → 架构设计师 写完整代码
    → 代码审查员 审查质量、找 Bug
    → 输出可运行代码
```

## 配置方式

通过环境变量配置 API：

```bash
export OPENAI_API_KEY="sk-xxx"
export OPENAI_BASE_URL="https://api.deepseek.com"
```

或参考 `.env.example` 创建 `.env` 文件。
