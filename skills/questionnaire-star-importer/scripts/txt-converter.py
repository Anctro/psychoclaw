#!/usr/bin/env python3
"""
问卷星文本导入格式转换脚本
用法：python3 txt-converter.py <输入文件> <输出文件>
"""
import re
import sys
from pathlib import Path

def parse_question(content):
    """解析单道题目"""
    lines = content.strip().split("\n")
    if not lines:
        return None
    
    # 第一行是题目
    first_line = lines[0].strip()
    # 去除题号
    q_match = re.match(r"(\d+)[.、\s]+(.+)", first_line)
    if q_match:
        q_no = q_match.group(1)
        q_content = q_match.group(2)
    else:
        q_no = ""
        q_content = first_line
    
    # 识别题型
    q_type = "单选题" # 默认单选
    type_match = re.search(r"【(多选题|量表题|填空题|多行填空题|排序题|评分题)(.*)】", q_content)
    if type_match:
        q_type = type_match.group(1)
        q_content = q_content.replace(type_match.group(0), "").strip()
        
        # 处理量表题/评分题的分值
        if q_type in ["量表题", "评分题"] and type_match.group(2):
            score_range = type_match.group(2).strip("|")
            q_content += f"【{q_type}|{score_range}】"
        else:
            q_content += f"【{q_type}】"
    else:
        # 检测是否是多选：选项超过4个/有"可多选"字样
        if "可多选" in q_content or "多选" in q_content:
            q_type = "多选题"
            q_content += "【多选题】"
    
    # 处理选项
    options = []
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        opt_match = re.match(r"([A-Za-z])[.、\s]+(.+)", line)
        if opt_match:
            opt_text = opt_match.group(2).strip()
            options.append(f"{opt_match.group(1)}. {opt_text}")
        elif re.match(r"\d+[.、\s]+", line): # 数字开头的选项
            opt_text = re.sub(r"\d+[.、\s]+", "", line).strip()
            options.append(opt_text)
    
    # 组装题目
    question = f"{q_no}. {q_content}\n"
    for opt in options:
        question += f"{opt}\n"
    
    return question

def convert_to_txt(input_path, output_path, title="问卷标题", description=""):
    """转换为问卷星文本导入格式"""
    content = Path(input_path).read_text(encoding="utf-8")
    
    # 分割题目（按数字题号分割）
    questions = re.split(r"\n\d+[.、]", content)
    if not questions[0].strip():
        questions = questions[1:]
    
    # 组装输出内容
    output = f"【{title}】\n"
    if description:
        output += f"{description}\n\n"
    
    for idx, q_content in enumerate(questions, 1):
        # 补上题号
        q_content = f"{idx}. {q_content.strip()}"
        parsed_q = parse_question(q_content)
        if parsed_q:
            output += parsed_q + "\n"
    
    # 写入输出文件
    Path(output_path).write_text(output, encoding="utf-8")
    print(f"✅ 文本导入格式已生成：{output_path}")
    print("💡 直接复制内容到问卷星「文本快速导入」框即可导入")
    return output

def main():
    if len(sys.argv) < 3:
        print("用法：python3 txt-converter.py <输入文件> <输出文件> [问卷标题] [问卷说明]")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    title = sys.argv[3] if len(sys.argv) > 3 else "问卷标题"
    description = sys.argv[4] if len(sys.argv) > 4 else ""
    
    if not Path(input_path).exists():
        print(f"❌ 输入文件不存在：{input_path}")
        sys.exit(1)
    
    convert_to_txt(input_path, output_path, title, description)

if __name__ == "__main__":
    main()
