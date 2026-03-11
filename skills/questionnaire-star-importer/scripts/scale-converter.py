#!/usr/bin/env python3
"""
PsychoClaw心理量表JSON转问卷星导入格式脚本
用法：python3 scale-converter.py <量表JSON文件> <输出格式：txt/excel> [输出路径]
"""
import json
import sys
from pathlib import Path
from txt_converter import convert_to_txt
from excel_converter import convert_to_excel

def scale_to_question_text(scale_json):
    """将心理量表JSON转换为问卷文本格式"""
    text = ""
    
    # 问卷说明
    text += f"{scale_json['scaleIntro']}\n\n"
    
    # 题目
    for question in scale_json["questions"]:
        q_text = f"{question['questionNo']}. {question['questionStem']}\n"
        for opt in question["options"]:
            q_text += f"{opt['optionId']}. {opt['optionText']}\n"
        text += q_text + "\n"
    
    return text

def main():
    if len(sys.argv) < 3:
        print("用法：python3 scale-converter.py <量表JSON文件> <输出格式：txt/excel> [输出路径]")
        print("示例：python3 scale-converter.py phq9.json txt phq9_问卷星导入.txt")
        sys.exit(1)
    
    scale_path = sys.argv[1]
    output_format = sys.argv[2].lower()
    if output_format not in ["txt", "excel"]:
        print("❌ 输出格式只能是txt或excel")
        sys.exit(1)
    
    if not Path(scale_path).exists():
        print(f"❌ 量表文件不存在：{scale_path}")
        sys.exit(1)
    
    # 读取量表JSON
    with open(scale_path, "r", encoding="utf-8") as f:
        scale_json = json.load(f)
    
    # 转换为问卷文本
    question_text = scale_to_question_text(scale_json)
    temp_path = Path("temp_question.txt")
    temp_path.write_text(question_text, encoding="utf-8")
    
    # 生成输出路径
    if len(sys.argv) > 3:
        output_path = sys.argv[3]
    else:
        output_path = f"{scale_json['scaleId']}_问卷星导入.{output_format}"
    
    # 转换为对应格式
    if output_format == "txt":
        convert_to_txt(temp_path, output_path, scale_json["scaleName"], scale_json["scaleIntro"])
    else:
        convert_to_excel(temp_path, output_path, scale_json["scaleName"])
    
    # 删除临时文件
    temp_path.unlink()
    print(f"✅ 心理量表已成功转换为问卷星{output_format.upper()}导入格式")

if __name__ == "__main__":
    main()
