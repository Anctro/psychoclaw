#!/usr/bin/env python3
"""
心理量表校验脚本：检查生成的量表JSON是否符合规范
用法：python3 scale-validator.py <scale.json>
"""
import json
import sys
from pathlib import Path

REQUIRED_FIELDS = [
    "scaleId", "scaleName", "scaleIntro", "questionCount",
    "questions", "scoringRule", "resultInterpretation"
]

QUESTION_REQUIRED_FIELDS = ["questionId", "questionNo", "questionStem", "options"]
OPTION_REQUIRED_FIELDS = ["optionId", "optionText", "score"]
SCORING_RULE_REQUIRED_FIELDS = ["scoringType", "totalScoreRange"]
RESULT_REQUIRED_FIELDS = ["scoreRange", "level", "resultDesc", "resultMeaning", "suggestions"]

def validate_scale(scale):
    """校验量表是否符合规范"""
    errors = []
    warnings = []
    
    # 检查必填字段
    for field in REQUIRED_FIELDS:
        if field not in scale:
            errors.append(f"缺失必填字段：{field}")
    
    if errors:
        return errors, warnings
    
    # 检查题目数量是否一致
    if scale["questionCount"] != len(scale["questions"]):
        errors.append(f"题目数量不匹配：questionCount={scale['questionCount']}，实际题目数={len(scale['questions'])}")
    
    # 检查每个题目
    question_ids = set()
    for idx, question in enumerate(scale["questions"]):
        for field in QUESTION_REQUIRED_FIELDS:
            if field not in question:
                errors.append(f"题目{idx+1}缺失必填字段：{field}")
        
        if "questionId" in question:
            if question["questionId"] in question_ids:
                errors.append(f"题目ID重复：{question['questionId']}")
            question_ids.add(question["questionId"])
        
        # 检查选项
        if "options" in question:
            option_ids = set()
            for o_idx, option in enumerate(question["options"]):
                for field in OPTION_REQUIRED_FIELDS:
                    if field not in option:
                        errors.append(f"题目{idx+1}的选项{o_idx+1}缺失必填字段：{field}")
                
                if "optionId" in option:
                    if option["optionId"] in option_ids:
                        errors.append(f"题目{idx+1}的选项ID重复：{option['optionId']}")
                    option_ids.add(option["optionId"])
                
                if "score" in option and not isinstance(option["score"], (int, float)):
                    errors.append(f"题目{idx+1}的选项{o_idx+1}分值必须是数字：{option['score']}")
    
    # 检查评分规则
    scoring_rule = scale["scoringRule"]
    for field in SCORING_RULE_REQUIRED_FIELDS:
        if field not in scoring_rule:
            errors.append(f"评分规则缺失必填字段：{field}")
    
    if "scoringType" in scoring_rule:
        if scoring_rule["scoringType"] not in ["sum", "reverse", "dimension"]:
            errors.append(f"无效的评分类型：{scoring_rule['scoringType']}，可选值：sum/reverse/dimension")
    
    if "reverseQuestions" in scoring_rule:
        for q_id in scoring_rule["reverseQuestions"]:
            if q_id not in question_ids:
                warnings.append(f"反向计分题目ID不存在：{q_id}")
    
    if "dimensions" in scoring_rule and scoring_rule["dimensions"]:
        for dim_idx, dim in enumerate(scoring_rule["dimensions"]):
            for field in ["dimensionId", "dimensionName", "questionIds", "scoreRange"]:
                if field not in dim:
                    errors.append(f"维度{dim_idx+1}缺失必填字段：{field}")
            
            if "questionIds" in dim:
                for q_id in dim["questionIds"]:
                    if q_id not in question_ids:
                        warnings.append(f"维度{dim['dimensionName']}包含不存在的题目ID：{q_id}")
    
    # 检查结果解释
    if not scale["resultInterpretation"]:
        warnings.append("结果解释为空")
    else:
        for res_idx, result in enumerate(scale["resultInterpretation"]):
            for field in RESULT_REQUIRED_FIELDS:
                if field not in result:
                    errors.append(f"结果解释{res_idx+1}缺失必填字段：{field}")
            
            if "scoreRange" in result:
                if not isinstance(result["scoreRange"], list) or len(result["scoreRange"]) != 2:
                    errors.append(f"结果解释{res_idx+1}的分数区间必须是长度为2的数组")
    
    return errors, warnings

def main():
    if len(sys.argv) != 2:
        print("用法：python3 scale-validator.py <量表JSON文件>")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    
    if not input_path.exists():
        print(f"错误：文件 {input_path} 不存在")
        sys.exit(1)
    
    # 读取JSON
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            scale = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ JSON格式错误：{e}")
        sys.exit(1)
    
    # 校验
    errors, warnings = validate_scale(scale)
    
    # 输出结果
    if errors:
        print("❌ 校验失败，存在以下错误：")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("✅ 量表结构校验通过")
    
    if warnings:
        print("\n⚠️  存在以下警告：")
        for warn in warnings:
            print(f"  - {warn}")
    else:
        print("\n✅ 无警告信息")
    
    print(f"\n📊 量表信息：")
    print(f"  名称：{scale['scaleName']}")
    print(f"  题目数：{scale['questionCount']}")
    print(f"  评分类型：{scale['scoringRule']['scoringType']}")
    print(f"  结果解释数：{len(scale['resultInterpretation'])}")

if __name__ == "__main__":
    main()
