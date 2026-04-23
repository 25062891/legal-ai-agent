import sys
import gradio as gr
import json
import datetime
import os
print("🔥 正在尝试关联 main.py...")
import main
print("✅ main.py 关联成功！")

# 1. 尝试导入 main，如果 main 有错，这里会报错

# ===== 核心分析函数 =====
def analyze(file):
    if file is None:
        return "❌ 请先上传 PDF 文件"

    try:
        # 调用 main.py 里的函数
        report = main.run_full_audit(file.name)

        # 格式化展示
        result = f"📄 文件：{report.filename}\n"
        result += f"📊 状态：{report.overall_status}\n\n"
        result += "⚠️ 审计详情：\n"

        for detail in report.details:
            result += f"--------------------------------\n"
            result += f"🚩 风险等级: {detail.risk_level}\n"
            result += f"📝 原因: {detail.reason}\n"
            result += f"💡 建议: {detail.suggestion}\n"
        return result

    except Exception as e:
        return f"❌ 运行中出错: {str(e)}"

# ===== 反馈逻辑 =====
def save_feedback(choice, result):
    data = {"time": str(datetime.datetime.now()), "feedback": choice, "result": result}
    with open("feedback.json", "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")
    return "✅ 已记录反馈"

# ===== UI 界面 =====
with gr.Blocks() as demo:
    gr.Markdown("## 🧠 智能合同审核系统")
    
    with gr.Row():
        file_input = gr.File(label="上传合同 (PDF)", file_types=[".pdf"])
        output_box = gr.Textbox(label="📊 审核结果", lines=15)

    analyze_btn = gr.Button("🔍 开始分析", variant="primary")
    analyze_btn.click(analyze, file_input, output_box)

    gr.Markdown("### 📊 人工反馈")
    with gr.Row():
        good_btn = gr.Button("👍 合理")
        bad_btn = gr.Button("👎 不合理")
        result_msg = gr.Textbox(label="反馈状态")

    good_btn.click(lambda r: save_feedback("good", r), output_box, result_msg)
    bad_btn.click(lambda r: save_feedback("bad", r), output_box, result_msg)

# 🚀 启动指令 (确保顶格写！)
if __name__ == "__main__":
    # 尝试用 9999 端口启动，如果不行会自动报错
    demo.launch(server_name="127.0.0.1", server_port=9999, share=True)