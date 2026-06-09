"""
CrewAI 层级模式 Demo
场景：多个 Agent 协作写一个井字棋小游戏
"""

from crewai import Agent, Task, Crew, Process, LLM
import os

# ============================================
# 配置 API — 用 OpenAI 兼容格式
# ============================================
# ⚠️ 使用前请配置你的 API Key
# 方式一：环境变量
#   export OPENAI_API_KEY="sk-xxx"
#   export OPENAI_BASE_URL="https://api.deepseek.com"
# 方式二：直接修改下面两行
API_KEY = os.environ.get("OPENAI_API_KEY", "your-api-key-here")
API_BASE = os.environ.get("OPENAI_BASE_URL", "https://api.deepseek.com")

os.environ["OPENAI_API_KEY"] = API_KEY
os.environ["OPENAI_BASE_URL"] = API_BASE
os.environ["PYTHONIOENCODING"] = "utf-8"

# 通用的 LLM 配置
common_llm = LLM(
    model="openai/deepseek-chat",
    api_key=API_KEY,
    base_url=API_BASE
)

# ============================================
# 1️⃣ 定义 Agent（角色）
# ============================================

# Manager 角色 — 负责拆任务、分配、汇总
# 注：Hierarchical 模式下 Manager Agent 会自动生成
# 我们只需要定义 Worker Agent

技术分析 = Agent(
    role="技术分析师",
    goal="深入分析技术方案的优缺点",
    backstory="你有10年架构经验，擅长发现技术方案中的问题和风险",
    llm=common_llm,
    verbose=True,
)

代码审查 = Agent(
    role="代码审查员",
    goal="审查代码质量，找出bug和安全隐患",
    backstory="你是资深代码审查专家，对代码质量问题零容忍",
    llm=common_llm,
    verbose=True,
)

架构设计 = Agent(
    role="架构设计师",
    goal="设计优雅、可扩展的系统架构",
    backstory="你擅长系统架构设计，注重可维护性和扩展性",
    llm=common_llm,
    verbose=True,
)

# ============================================
# 2️⃣ 定义 Task（任务）
# ============================================

task1 = Task(
    description="""分析以下Bug报告并制定修复方案：
1. BUG-001：Board.save_state() 引用了不存在的 self._current_player 属性
2. BUG-002：DisplayManager.show_game_info() 中 end="" 使用错误
3. BUG-003：悔棋逻辑 _undo_move 直接访问私有成员 _history
4. ISSUE-001：AI对AI模式未正确实现
5. 其他代码质量问题

请列出每个Bug的修复步骤和方案。""",
    expected_output="包含每个Bug的根因分析和具体修复步骤的修复方案",
    agent=技术分析,
)

task2 = Task(
    description="""根据修复方案，重写井字棋游戏的完整代码。
要求：
1. 修复所有已知Bug（参考修复方案）
2. 输出完整的、可直接运行的单个Python文件（不要分包）
3. 支持双人对战模式
4. 终端界面，命令行交互
5. 代码必须能直接 python xxx.py 运行""",
    expected_output="一个完整的、可直接运行的Python井字棋游戏代码文件",
    agent=架构设计,
)

task3 = Task(
    description="审查修复后的井字棋代码，确保所有Bug已修复且代码可以正常运行",
    expected_output="最终确认：所有Bug已修复，代码可直接运行",
    agent=代码审查,
)

# ============================================
# 3️⃣ 组队开干
# ============================================

团队 = Crew(
    agents=[技术分析, 代码审查, 架构设计],
    tasks=[task1, task2, task3],
    process=Process.sequential,  # ← 顺序执行：分析→编码→审查
    verbose=True,
)

# ============================================
# 4️⃣ 执行
# ============================================
if __name__ == "__main__":
    result = 团队.kickoff(inputs={
        "goal": "修复井字棋代码中的Bug并输出可直接运行的完整Python脚本"
    })
    print("\n" + "="*60)
    print("最终结果：")
    print(result)
