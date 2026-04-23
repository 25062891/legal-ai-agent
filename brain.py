# brain.py
import json
from openai import OpenAI
from schemas import Clause, AuditDetail, LegalReference
from typing import List

# ==========================================
# 1. 填入你的钥匙
# ==========================================
DEEPSEEK_API_KEY = "sk-66cc56ee2ed740c68c504398b459d526" # 例如 "sk-1234abcd..."

client = OpenAI(
    api_key=DEEPSEEK_API_KEY, 
    base_url="https://api.deepseek.com"
)

# ==========================================
# 2. 编写 Prompt (你是 Prompt 工程师的核心工作)
# ==========================================
SYSTEM_PROMPT = """
你是一位精通马来西亚《1955年雇佣法》(Employment Act 1955) 的资深合规律师。
你的任务是对比【待审核合同条款】与我提供的【马来西亚法律条文】，评估其合规性。

【重要提醒】
1. 如果法律条文显示周工时上限是 45 小时，而合同写 48 小时，必须判定为 "HIGH" 风险。
2. 给出原因时，请务必引用具体的 Section 编号。
3. 风险等级选择：HIGH (违规), MEDIUM (模糊/建议优化), LOW (合规)。
"""

# ==========================================
# 3. 核心功能函数 (给成员 D 调用的接口)
# ==========================================
def analyze_contract(clause: Clause, references: List[LegalReference]) -> AuditDetail:
    # 拼接法律条文和合同内容
    laws_text = "\n".join([f"- {ref.section}: {ref.content}" for ref in references])
    user_content = f"【待审核合同条款】\n标题：{clause.title}\n内容：{clause.content}\n\n【相关的法律条文】\n{laws_text}"
    
    try:
        # 呼叫 DeepSeek 大脑
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content}
            ],
            response_format={"type": "json_object"}, # 强制它输出 JSON
            temperature=0.1
        )
        
        # 解析返回的数据
        result_dict = json.loads(response.choices[0].message.content)
        
        # 组装成成员 D 需要的 AuditDetail 格式
        return AuditDetail(
            clause_id=clause.clause_id,
            risk_level=result_dict.get("risk_level", "MEDIUM"),
            reason=result_dict.get("reason", "解析失败"),
            suggestion=result_dict.get("suggestion", "解析失败"),
            references=references
        )
        
    except Exception as e:
        print(f"出错啦: {e}")
        # 如果断网了，给个默认回复，防止程序崩溃
        return AuditDetail(
            clause_id=clause.clause_id,
            risk_level="MEDIUM",
            reason=f"AI 系统异常: {str(e)}",
            suggestion="需人工复核",
            references=references
        )

# ==========================================
# 4. 本地测试区 (你自己模拟 A 和 B 的数据来测试)
# ==========================================
if __name__ == "__main__":
    print("开始模拟测试...")
    
    # 模拟一条黑心合同
    test_clause = Clause(
        clause_id="clause_001", 
        title="工作时间与加班",
        content="雇员每周的正常工作时间为 55 小时，超出部分不计算加班费。"
    )
    
    # 模拟一条马来西亚雇佣法
    test_refs = [
        LegalReference(
            section="Employment Act 1955, Section 60A", 
            content="雇员一周的正常工作时间不得超过 45 小时。超过正常工作时间的劳动需支付加班费。"
        )
    ]
    
    print("🧠 正在呼叫 DeepSeek 进行审计...")
    
    # 运行你的核心逻辑
    result = analyze_contract(test_clause, test_refs)
    
    print("\n✅ 测试成功！输出了完美的数据：")
    print(f"风险等级: [{result.risk_level}]")
    print(f"违规原因: {result.reason}")
    print(f"修改建议: {result.suggestion}")
