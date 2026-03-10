#!/usr/bin/env python3
"""
心理量表转换脚本：将文本格式的量表内容转换为标准JSON结构
用法：python3 scale-converter.py <input.txt> <output.json>
"""
import json
import re
import sys
from pathlib import Path

def parse_scale_text(text):
    """解析文本格式的量表内容"""
    scale = {
        "scaleId": "",
        "scaleName": "",
        "scaleIntro": "",
        "questionCount": 0,
        "questions": [],
        "scoringRule": {},
        "resultInterpretation": []
    }
    
    # 提取量表ID和名称
    name_match = re.search(r"量表名称：(.+)", text)
    if name_match:
        scale["scaleName"] = name_match.group(1).strip()
        scale["scaleId"] = re.sub(r"[^a-z0-9]+", "-", scale["scaleName"].lower())
    
    # 提取量表介绍
    intro_match = re.search(r"量表介绍：(.+?)(?=\n\d+\.|评分规则|结果解释)", text, re.DOTALL)
    if intro_match:
        scale["scaleIntro"] = intro_match.group(1).strip()
    
    # 提取题目
    questions = []
    question_pattern = re.compile(r"(\d+)\. (.+?)(?=\nA\.|\nB\.|\nC\.|\nD\.|\n\d+\.|评分规则|结果解释)", re.DOTALL)
    option_pattern = re.compile(r"([A-D])\. (.+?)(?=\([0-5]分\)|\n[A-D]\.|\n|$)")
    score_pattern = re.compile(r"\(([0-5])分\)")
    
    for q_match in question_pattern.finditer(text):
        q_no = int(q_match.group(1))
        q_stem = q_match.group(2).strip()
        options_text = text[q_match.end():]
        
        options = []
        for opt_match in option_pattern.finditer(options_text):
            opt_id = opt_match.group(1)
            opt_text = opt_match.group(2).strip()
            score_match = score_pattern.search(options_text[opt_match.end():opt_match.end()+10])
            score = int(score_match.group(1)) if score_match else 0
            
            options.append({
                "optionId": opt_id,
                "optionText": opt_text,
                "score": score
            })
        
        questions.append({
            "questionId": f"q{q_no}",
            "questionNo": q_no,
            "questionStem": q_stem,
            "options": options
        })
    
    scale["questions"] = questions
    scale["questionCount"] = len(questions)
    
    # 提取评分规则
    scoring_match = re.search(r"评分规则：(.+?)(?=结果解释|$)", text, re.DOTALL)
    if scoring_match:
        scoring_text = scoring_match.group(1).strip()
        scoring_rule = {
            "scoringType": "sum",
            "totalScoreRange": [0, len(questions)*4],
            "reverseQuestions": [],
            "dimensions": []
        }
        
        # 检测反向计分
        reverse_match = re.search(r"反向计分题目：(.+)", scoring_text)
        if reverse_match:
            reverse_q = re.findall(r"\d+", reverse_match.group(1))
            scoring_rule["reverseQuestions"] = [f"q{q}" for q in reverse_q]
        
        # 检测多维度
        dimension_pattern = re.compile(r"维度(.+?)：(.+?)包含题目：([\d、, ]+)", re.DOTALL)
        for dim_match in dimension_pattern.finditer(scoring_text):
            dim_name = dim_match.group(1).strip()
            dim_desc = dim_match.group(2).strip()
            dim_qs = re.findall(r"\d+", dim_match.group(3))
            scoring_rule["dimensions"].append({
                "dimensionId": re.sub(r"[^a-z0-9]+", "-", dim_name.lower()),
                "dimensionName": dim_name,
                "dimensionDesc": dim_desc,
                "questionIds": [f"q{q}" for q in dim_qs],
                "scoreRange": [0, len(dim_qs)*4]
            })
        
        if len(scoring_rule["dimensions"]) > 0:
            scoring_rule["scoringType"] = "dimension"
        
        scale["scoringRule"] = scoring_rule
    
    # 提取结果解释
    result_match = re.search(r"结果解释：(.+)", text, re.DOTALL)
    if result_match:
        result_text = result_match.group(1).strip()
        result_pattern = re.compile(r"([0-9\-]+)分：(.+?)(?=\n[0-9\-]+分：|$)", re.DOTALL)
        
        for res_match in result_pattern.finditer(result_text):
            score_range_str = res_match.group(1).strip()
            content = res_match.group(2).strip()
            
            # 解析分数区间
            if "-" in score_range_str:
                min_s, max_s = map(int, score_range_str.split("-"))
            else:
                min_s = int(score_range_str)
                max_s = scale["scoringRule"]["totalScoreRange"][1]
            
            # 提取等级、描述、含义、建议
            level = "正常"
            if "轻度" in content:
                level = "轻度"
            elif "中度" in content:
                level = "中度"
            elif "重度" in content:
                level = "重度"
            
            desc = re.search(r"(.+?)。", content).group(1) if re.search(r"(.+?)。", content) else content
            meaning = re.search(r"含义：(.+?)。", content).group(1) if re.search(r"含义：(.+?)。", content) else ""
            suggestions = re.findall(r"建议：(.+?)(?。|；|$)", content)
            
            scale["resultInterpretation"].append({
                "scoreRange": [min_s, max_s],
                "level": level,
                "resultDesc": desc,
                "resultMeaning": meaning,
                "suggestions": [s.strip() for s in suggestions if s.strip()]
            })
    
    return scale

def main():
    if len(sys.argv) != 3:
        print("用法：python3 scale-converter.py <输入文本文件> <输出JSON文件>")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    
    if not input_path.exists():
        print(f"错误：输入文件 {input_path} 不存在")
        sys.exit(1)
    
    # 读取输入文本
    text = input_path.read_text(encoding="utf-8")
    
    # 解析量表
    scale = parse_scale_text(text)
    
    # 写入JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(scale, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 量表转换完成，已保存到 {output_path}")
    print(f"📊 量表名称：{scale['scaleName']}")
    print(f"📝 题目数量：{scale['questionCount']}")

if __name__ == "__main__":
    main()
