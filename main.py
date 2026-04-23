import os
import uuid
import shutil
# 导入协议规范
from schemas import FinalAuditReport, Clause, AuditDetail, LegalReference
# 导入成员 B 的 RAG 模块
try:
    import member_b
    print("✅ 成功关联法律数据库模块 (member_b)")
except ImportError:
    print("❌ 警告：未找到 member_b.py，请确保文件在同一目录下")

def run_full_audit(pdf_path: str):
    """
    【指挥中心】集成全流程逻辑
    """
    print(f"\n[🚀 系统启动] 正在审计文件: {os.path.basename(pdf_path)}")
    
    # ------------------------------------------
    # 步骤 1: 模拟提取条款 (后续可接入成员 A 的 OCR)
    # ------------------------------------------
    print("[Step 1] 正在提取合同条款...")
    clauses = [
        Clause(clause_id="C1", title="工时条款", content="The employee shall work 60 hours per week without overtime pay."),
        Clause(clause_id="C2", title="年假条款", content="The employee is entitled to 5 days of annual leave per year.")
    ]

    # ------------------------------------------
    # 步骤 2: 循环审计（集成成员 B 的 RAG 检索）
    # ------------------------------------------
    print("[Step 2] 正在检索法律依据并进行合规性分析...")
    all_details = []
    
    for c in clauses:
        print(f"  - 正在分析: {c.title}...")
        
        # --- 调用成员 B 的真实检索接口 ---
        try:
            raw_laws = member_b.get_relevant_laws(c.content)
            # 将检索到的字典列表转换为 LegalReference 对象列表
            real_laws = [
                LegalReference(section=l["section"], content=l["content"]) 
                for l in raw_laws
            ]
        except Exception as e:
            print(f"    ⚠️ 检索失败: {e}")
            real_laws = []

        # --- 模拟成员 C 的 AI 审计逻辑 ---
        # 实际演示时，这里的内容会根据 real_laws 的内容动态展示
        risk_lvl = "HIGH"
        reason = f"条款内容与 {real_laws[0].section if real_laws else '相关法规'} 冲突。"
        suggestion = "建议根据马来西亚雇佣法调整至法定标准。"

        # 针对具体条文的硬编码 Demo 逻辑（演示用）
        if "60 hours" in c.content:
            reason = f"违反了 {real_laws[0].section}: 每周工作时间不得超过 45 小时。"
            suggestion = "请将周工作时间修改为 45 小时以内，并依法支付加班费。"
        elif "5 days" in c.content:
            reason = f"违反了 {real_laws[0].section}: 法定最低年假为 8 天。"
            suggestion = "请将年假天数调整为至少 8 天。"

        detail = AuditDetail(
            clause_id=c.clause_id,
            risk_level=risk_lvl,
            reason=reason,
            suggestion=suggestion,
            references=real_laws
        )
        all_details.append(detail)

    # ------------------------------------------
    # 步骤 3: 封装最终报告
    # ------------------------------------------
    report = FinalAuditReport(
        report_id=str(uuid.uuid4()),
        filename=os.path.basename(pdf_path),
        overall_status="⚠️ 发现多个高风险合规项",
        details=all_details
    )
    
    return report

# ==========================================
# 本地测试运行区
# ==========================================
if __name__ == "__main__":
    # 1. 确保环境准备就绪
    os.makedirs("data/raw", exist_ok=True)
    test_pdf = "data/raw/contract_demo.pdf"
    if not os.path.exists(test_pdf):
        with open(test_pdf, "w") as f: f.write("dummy pdf content")
            
    # 2. 执行审计
    try:
        final_report = run_full_audit(test_pdf)
        print("\n" + "="*50)
        print("📊 审计报告生成成功 (JSON 格式):")
        print(final_report.model_dump_json(indent=2))
        print("="*50)
    except Exception as e:
        print(f"❌ 运行失败: {e}")