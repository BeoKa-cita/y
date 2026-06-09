"""
CrewAI 飞书集成版
用法：python crewai_feishu.py "你的需求"
示例：python crewai_feishu.py "写一个贪吃蛇游戏"
"""

from crewai import Agent, Task, Crew, Process, LLM
import os
import sys

# ============================================
# 配置 API
# ============================================
# ⚠️ 安全：API Key 必须通过环境变量提供，禁止硬编码
API_KEY = os.environ.get("OPENAI_API_KEY")
API_BASE = os.environ.get("OPENAI_BASE_URL", "https://api.deepseek.com")

if not API_KEY or API_KEY == "your-api-key-here":
    print("❌ 请设置环境变量 OPENAI_API_KEY")
    print("   在终端执行: export OPENAI_API_KEY='sk-xxx'")
    print("   或创建 .env 文件（参考 .env.example）")
    sys.exit(1)

os.environ["OPENAI_API_KEY"] = API_KEY
os.environ["OPENAI_BASE_URL"] = API_BASE
os.environ["PYTHONIOENCODING"] = "utf-8"

common_llm = LLM(
    model="openai/deepseek-chat",
    api_key=API_KEY,
    base_url=API_BASE
)

# ============================================
# 定义 Agent
# ============================================
技术分析 = Agent(
    role="技术分析师",
    goal="深入分析需求，制定技术方案",
    backstory="你有10年架构经验，擅长把模糊需求变成清晰的技术方案",
    llm=common_llm,
)

架构设计 = Agent(
    role="架构设计师",
    goal="输出完整可运行的代码",
    backstory="你擅长写完整的可运行代码，注重代码质量和可维护性",
    llm=common_llm,
)

代码审查 = Agent(
    role="代码审查员",
    goal="确保代码正确、无Bug、可直接运行",
    backstory="你是资深审查专家，发现过无数生产环境Bug",
    llm=common_llm,
)

# ============================================
# 定义 Task（任务按顺序执行）
# ============================================
task1 = Task(
    description="""分析以下需求，给出技术方案和设计思路：
目标：{goal}
要求：给出清晰的技术选型和实现方案""",
    expected_output="包含技术选型、模块划分、实现步骤的设计方案",
    agent=技术分析,
)

task2 = Task(
    description="""根据技术方案，编写完整代码。
目标：{goal}
要求：
1. 输出单个完整的Python文件，可直接运行
2. 添加必要的输入处理（如果有交互）
3. 代码要健壮，做好异常处理""",
    expected_output="可直接运行的Python代码文件",
    agent=架构设计,
)

task3 = Task(
    description="审查上述代码，确保可以正常运行，没有语法错误和逻辑Bug",
    expected_output="最终确认：代码可运行，并附上完整的最终代码",
    agent=代码审查,
)

# ============================================
# 组队执行
# ============================================
团队 = Crew(
    agents=[技术分析, 架构设计, 代码审查],  # 与 tasks 执行顺序一致
    tasks=[task1, task2, task3],
    process=Process.sequential,
    verbose=False,
)


def main():
    """主函数：根据用户需求调用 CrewAI 团队执行"""
    goal = sys.argv[1] if len(sys.argv) > 1 else "写一个井字棋游戏"
    result = 团队.kickoff(inputs={"goal": goal})
    print("\n" + "="*60)
    print("📦 最终结果：")
    print(result)


if __name__ == "__main__":
    main()
