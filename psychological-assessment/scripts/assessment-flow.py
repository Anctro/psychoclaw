#!/usr/bin/env python3
"""
心理健康测评流程控制脚本
用法：python3 assessment-flow.py
"""
import json
import sys
from pathlib import Path
from datetime import datetime

ASSETS_DIR = Path(__file__).parent.parent / "assets"
SCALES = {
    "phq9": "抑郁状态测评（PHQ-9）",
    "gad7": "焦虑状态测评（GAD-7）",
    "pss10": "压力水平评估（PSS-10）",
    "psqi": "睡眠质量评估（PSQI")
}

def load_scale(scale_key):
    """加载量表JSON"""
    scale_path = ASSETS_DIR / f"{scale_key}.json"
    with open(scale_path, "r", encoding="utf-8") as f:
        return json.load(f)

def calculate_score(scale, answers):
    """计算得分"""
    total_score = 0
    for q_id, answer in answers.items():
        # 找到对应题目
        question = next(q for q in scale["questions"] if q["questionId"] == q_id)
        # 找到对应选项的分值
        score = next(opt["score"] for opt in question["options"] if opt["optionId"] == answer)
        # 反向计分处理
        if q_id in scale["scoringRule"]["reverseQuestions"]:
            max_score = max(opt["score"] for opt in question["options"])
            score = max_score - score
        total_score += score
    return total_score

def get_result(scale, total_score):
    """获取结果解释"""
    for result in scale["resultInterpretation"]:
        min_s, max_s = result["scoreRange"]
        if min_s <= total_score <= max_s:
            return result
    return None

def generate_report(scale, total_score, result):
    """生成测评报告"""
    report = f"""# 心理健康测评报告
## 基本信息
- 测评时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- 量表名称：{scale["scaleName"]}
- 总分：{total_score} / {scale["scoringRule"]["totalScoreRange"][1]}
- 风险等级：{result["level"]}

## 结果说明
{result["resultDesc"]}

{result["resultMeaning"]}

## 改善建议
"""
    for idx, suggestion in enumerate(result["suggestions"], 1):
        report += f"{idx}. {suggestion}\n"
    
    report += "\n⚠️ 重要提示：本测评结果仅用于自我筛查，不能替代专业医学诊断。如果症状持续影响日常生活，请及时寻求专业心理咨询师或精神科医生的帮助。"
    return report

def save_record(user_id, scale, total_score, result):
    """保存测评记录到mentalhealth.md"""
    record_path = Path("/Users/ange/.openclaw/workspace/mentalhealth.md")
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    record = f"""
## {time_str} - {scale["scaleName"]}
- 总分：{total_score} / {scale["scoringRule"]["totalScoreRange"][1]}
- 等级：{result["level"]}
- 摘要：{result["resultDesc"]}
- 建议：{result["suggestions"][0]}
---
"""
    if not record_path.exists():
        header = "# 心理健康测评记录\n\n"
        record_path.write_text(header + record, encoding="utf-8")
    else:
        with open(record_path, "a", encoding="utf-8") as f:
            f.write(record)

def main():
    print("="*50)
    print("🧠 心理健康测评小助手")
    print("="*50)
    print("你好呀~ 我可以帮你做四个方面的心理健康筛查：")
    print("1. 📉 抑郁状态测评（PHQ-9）")
    print("2. 😰 焦虑状态测评（GAD-7）")
    print("3. 🥵 压力水平评估（PSS-10）")
    print("4. 😴 睡眠质量评估（PSQI）")
    print("\n请问你想做哪个测评呢？请输入对应序号：")
    
    # 选择量表
    while True:
        choice = input("> ").strip()
        if choice == "1":
            scale_key = "phq9"
            break
        elif choice == "2":
            scale_key = "gad7"
            break
        elif choice == "3":
            scale_key = "pss10"
            break
        elif choice == "4":
            scale_key = "psqi"
            break
        else:
            print("请输入正确的序号（1-4）哦~")
    
    # 加载量表
    scale = load_scale(scale_key)
    print(f"\n✅ 已选择：{scale['scaleName']}")
    print(f"📝 {scale['scaleIntro']}")
    print("\n接下来我会问你几个问题，你根据实际情况选择对应选项就好啦~")
    print("="*50)
    
    # 答题
    answers = {}
    for question in scale["questions"]:
        print(f"\n{question['questionNo']}. {question['questionStem']}")
        for opt in question["options"]:
            print(f"  {opt['optionId']}. {opt['optionText']} ({opt['score']}分)")
        
        while True:
            ans = input("> ").strip().upper()
            valid_opts = [opt["optionId"] for opt in question["options"]]
            if ans in valid_opts:
                answers[question["questionId"]] = ans
                break
            else:
                print(f"请输入正确的选项（{'/'.join(valid_opts)}）哦~")
    
    # 计算结果
    print("\n" + "="*50)
    print("🔍 正在分析结果，请稍等...")
    total_score = calculate_score(scale, answers)
    result = get_result(scale, total_score)
    
    # 生成报告
    report = generate_report(scale, total_score, result)
    print("\n" + "="*50)
    print("📊 你的测评报告")
    print("="*50)
    print(report)
    
    # 保存记录
    save_record("default", scale, total_score, result)
    print("\n✅ 测评记录已保存到 mentalhealth.md")
    
    # 后续建议
    print("\n💡 如果需要做其他测评，或者有什么想聊聊的都可以告诉我哦~")
    if result["level"] in ["中度", "中重度", "重度"]:
        print("\n⚠️  温馨提示：你的测评结果显示存在一定程度的症状，如果已经影响到日常生活，建议及时寻求专业帮助哦。")

if __name__ == "__main__":
    main()
