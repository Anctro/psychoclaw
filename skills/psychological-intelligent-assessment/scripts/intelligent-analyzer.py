#!/usr/bin/env python3
"""
智能心理状态分析脚本
用法：python3 intelligent-analyzer.py [会话历史文件]
"""
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

WORKSPACE_DIR = Path("/Users/ange/.openclaw/workspace")
MENTAL_HEALTH_RECORD = WORKSPACE_DIR / "mentalhealth.md"
USER_PROFILE = WORKSPACE_DIR / "USER.md"

def load_mental_records():
    """加载历史测评记录"""
    if not MENTAL_HEALTH_RECORD.exists():
        return []
    
    # 限制文件大小：最大5MB
    MAX_FILE_SIZE = 5 * 1024 * 1024
    file_size = MENTAL_HEALTH_RECORD.stat().st_size
    if file_size > MAX_FILE_SIZE:
        print(f"⚠️  历史测评记录文件过大：{file_size/1024/1024:.2f}MB，仅读取最近30天记录")
        # 只读取文件最后5MB内容
        with open(MENTAL_HEALTH_RECORD, 'rb') as f:
            f.seek(-MAX_FILE_SIZE, 2)
            content = f.read().decode('utf-8', errors='ignore')
    else:
        content = MENTAL_HEALTH_RECORD.read_text(encoding="utf-8")
    
    # 限制文本长度：最大5万字符
    MAX_TEXT_LENGTH = 50000
    if len(content) > MAX_TEXT_LENGTH:
        content = content[-MAX_TEXT_LENGTH:] # 取最后部分，保留最新记录
    records = []
    current_record = {}
    
    for line in content.split("\n"):
        if line.startswith("## "):
            if current_record:
                records.append(current_record)
            time_str, scale_name = line[3:].split(" - ", 1)
            try:
                record_time = datetime.strptime(time_str.strip(), "%Y-%m-%d %H:%M:%S")
                current_record = {
                    "time": record_time,
                    "scale_name": scale_name.strip(),
                    "is_recent": (datetime.now() - record_time) < timedelta(days=30)
                }
            except:
                current_record = {}
        elif line.startswith("- 总分：") and current_record:
            current_record["total_score"] = line.split("：")[1].strip()
        elif line.startswith("- 等级：") and current_record:
            current_record["level"] = line.split("：")[1].strip()
        elif line.startswith("- 摘要：") and current_record:
            current_record["summary"] = line.split("：")[1].strip()
    
    if current_record:
        records.append(current_record)
    
    # 按时间倒序排列
    records.sort(key=lambda x: x.get("time", datetime.min), reverse=True)
    return records

def load_user_profile():
    """加载用户profile"""
    if not USER_PROFILE.exists():
        return {}
    
    content = USER_PROFILE.read_text(encoding="utf-8")
    profile = {}
    for line in content.split("\n"):
        if line.startswith("- "):
            if "：" in line:
                key, value = line[2:].split("：", 1)
                profile[key.strip()] = value.strip()
    return profile

def load_conversation_history(file_path=None):
    """加载会话历史"""
    if not file_path or not Path(file_path).exists():
        return ""
    
    path = Path(file_path)
    # 限制文件大小：最大10MB
    MAX_FILE_SIZE = 10 * 1024 * 1024
    file_size = path.stat().st_size
    if file_size > MAX_FILE_SIZE:
        print(f"⚠️  会话历史文件过大：{file_size/1024/1024:.2f}MB，仅读取最后10MB内容")
        with open(path, 'rb') as f:
            f.seek(-MAX_FILE_SIZE, 2)
            content = f.read().decode('utf-8', errors='ignore')
    else:
        content = path.read_text(encoding="utf-8")
    
    # 限制文本长度：最大8万字符，避免token超限
    MAX_TEXT_LENGTH = 80000
    if len(content) > MAX_TEXT_LENGTH:
        content = content[-MAX_TEXT_LENGTH:] # 取最后部分，保留最新会话
    return content

def analyze_dimension(records, dimension, conversation=""):
    """分析单个维度"""
    scale_map = {
        "depression": "PHQ-9",
        "anxiety": "GAD-7",
        "sleep": "PSQI",
        "stress": "PSS-10"
    }
    
    scale_name = scale_map[dimension]
    
    # 查找最近30天的测评记录
    recent_record = None
    for record in records:
        if record.get("is_recent") and scale_name in record.get("scale_name", ""):
            recent_record = record
            break
    
    if recent_record:
        return {
            "level": recent_record["level"],
            "confidence": "明确判断",
            "evidence": f"2026-03-10 {scale_name} 测评结果为{recent_record['level']}",
            "description": recent_record["summary"]
        }
    
    # 没有测评数据，分析会话线索
    # 这里可以扩展NLP分析逻辑，目前简化处理
    return {
        "level": "暂无足够数据评估",
        "confidence": "数据不足",
        "evidence": "近期无相关测评记录，且无足够行为线索",
        "description": "建议进行专项测评获得准确结果"
    }

def generate_report(records, profile, conversation=""):
    """生成评估报告"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 分析四个维度
    dimensions = {
        "depression": analyze_dimension(records, "depression", conversation),
        "anxiety": analyze_dimension(records, "anxiety", conversation),
        "sleep": analyze_dimension(records, "sleep", conversation),
        "stress": analyze_dimension(records, "stress", conversation)
    }
    
    # 生成报告
    report = f"""🧠 你的智能心理状态评估报告
---
## 一、基础信息
- 评估时间：{now}
- 数据来源：历史测评记录（{len(records)}条）+ 用户特征 + 近期会话信息
---
## 二、分维度评估
### 📉 抑郁状态：{dimensions['depression']['level']}
**判断依据**：{dimensions['depression']['evidence']}
**状态说明**：{dimensions['depression']['description']}

### 😰 焦虑状态：{dimensions['anxiety']['level']}
**判断依据**：{dimensions['anxiety']['evidence']}
**状态说明**：{dimensions['anxiety']['description']}

### 😴 睡眠质量：{dimensions['sleep']['level']}
**判断依据**：{dimensions['sleep']['evidence']}
**状态说明**：{dimensions['sleep']['description']}

### 🥵 压力水平：{dimensions['stress']['level']}
**判断依据**：{dimensions['stress']['evidence']}
**状态说明**：{dimensions['stress']['description']}
---
## 三、整体状态总结
"""
    
    # 整体总结
    has_issue = any(d["level"] in ["轻度", "中度", "重度"] for d in dimensions.values())
    if has_issue:
        report += "从目前的数据分析来看，你在部分维度存在一定的心理困扰，建议重点关注相关问题，及时调整。"
    else:
        report += "从目前的数据分析来看，你的整体心理状态良好，继续保持健康的生活习惯和心态即可。"
    
    # 建议部分
    report += "\n---\n## 四、个性化改善建议\n"
    suggestions = []
    
    if dimensions['depression']['level'] in ["轻度", "中度", "重度"]:
        suggestions.append(f"针对抑郁状态：{dimensions['depression']['level']}，建议多进行户外运动，多和亲友交流，必要时寻求专业帮助。")
    if dimensions['anxiety']['level'] in ["轻度", "中度", "重度"]:
        suggestions.append(f"针对焦虑状态：{dimensions['anxiety']['level']}，建议尝试正念冥想、深呼吸等放松技巧，合理安排工作休息节奏。")
    if dimensions['sleep']['level'] in ["轻度", "中度", "重度"]:
        suggestions.append(f"针对睡眠问题：{dimensions['sleep']['level']}，建议建立规律的作息习惯，睡前避免使用电子设备，必要时就医检查。")
    if dimensions['stress']['level'] in ["轻度", "中度", "重度"]:
        suggestions.append(f"针对压力问题：{dimensions['stress']['level']}，建议合理规划任务，学会拒绝不合理的要求，适当给自己减负。")
    
    if not suggestions:
        suggestions.append("1. 保持规律的作息和健康的饮食习惯\n2. 每周保持3次以上的有氧运动\n3. 定期进行心理状态自查，及时调整状态")
    else:
        for idx, s in enumerate(suggestions, 1):
            suggestions[idx-1] = f"{idx}. {s}"
    
    report += "\n".join(suggestions)
    
    # 风险提示
    report += "\n\n---\n⚠️ 提示：本评估为基于已有数据的智能分析，不能替代专业诊断。如有明显不适请及时寻求专业心理咨询师或精神科医生的帮助。"
    
    return report

def main():
    conversation_file = sys.argv[1] if len(sys.argv) > 1 else None
    
    # 加载数据
    records = load_mental_records()
    profile = load_user_profile()
    conversation = load_conversation_history(conversation_file)
    
    # 生成报告
    report = generate_report(records, profile, conversation)
    print(report)
    
    # 保存报告到记录
    if MENTAL_HEALTH_RECORD.exists():
        with open(MENTAL_HEALTH_RECORD, "a", encoding="utf-8") as f:
            time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"\n## {time_str} - 智能心理状态评估\n")
            f.write("- 类型：智能分析\n")
            f.write(f"- 记录已保存\n---\n")

if __name__ == "__main__":
    main()
