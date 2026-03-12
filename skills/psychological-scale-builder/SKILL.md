---
name: psychological-scale-builder
description: 标准化心理测评量表构建工具，支持将离散的量表文本内容（题目、评分规则、结果解释等）自动转换为统一规范的JSON结构，内置临床心理学量表标准规范。使用触发场景：用户要制作/转换心理测评量表、标准化量表数据结构、为心理测评Agent提供量表数据源、生成符合规范的量表JSON文件、说"帮我做个心理量表"、"把这个量表转成JSON"时，必须使用这个技能。
---

# 心理量表构建工具

## 概述
本工具用于快速将离散的心理测评量表文本内容转换为统一规范的JSON格式，严格遵循临床心理学量表设计标准，自动校验量表结构完整性，确保生成的量表可直接用于Agent对话式测评场景。

## 核心功能
1. **自动结构化转换**：将纯文本格式的量表内容自动识别并转换为标准JSON结构
2. **结构校验**：自动检查量表必填字段是否完整，不符合规范时给出修正建议
3. **内置模板**：提供情绪、人格、睡眠、职业倦怠等常见量表的模板参考
4. **批量生成**：支持一次性转换多个量表，统一输出规范格式

## 标准量表JSON结构
```json
{
  "scaleId": "string", // 量表唯一标识
  "scaleName": "string", // 量表名称
  "scaleIntro": "string", // 量表介绍、适用场景、完成时长说明
  "questionCount": "number", // 题目总数
  "questions": [
    {
      "questionId": "string", // 题目ID
      "questionNo": "number", // 题目序号
      "questionStem": "string", // 题干内容
      "options": [ // 选项列表
        {
          "optionId": "string",
          "optionText": "string", // 选项内容
          "score": "number" // 选项分值
        }
      ]
    }
  ],
  "scoringRule": {
    "scoringType": "sum|reverse|dimension", // 评分类型：总分/反向计分/多维度计分
    "totalScoreRange": [number, number], // 总分范围
    "reverseQuestions": ["string"], // 需要反向计分的题目ID列表（可选）
    "dimensions": [ // 多维度计分的维度定义（可选）
      {
        "dimensionId": "string",
        "dimensionName": "string",
        "dimensionDesc": "string",
        "questionIds": ["string"], // 该维度包含的题目ID
        "scoreRange": [number, number] // 维度分数范围
      }
    ]
  },
  "resultInterpretation": [
    {
      "scoreRange": [number, number], // 分数区间
      "level": "string", // 风险等级：正常/轻度/中度/重度
      "resultDesc": "string", // 结果说明
      "resultMeaning": "string", // 结果含义解释
      "suggestions": ["string"] // 给用户的建议列表
    }
  ]
}
```

## 使用流程
1. 输入原始量表文本内容，包含：量表介绍、所有题目、选项、评分规则、结果解释
2. 工具自动识别各部分内容，按照标准结构生成JSON
3. 自动校验结构完整性，提示缺失字段
4. 输出最终标准化量表JSON文件，可直接导入心理测评系统使用

## 资源说明
### scripts/
- `scale-converter.py`：量表转换脚本，支持将文本格式量表转换为标准JSON
- `scale-validator.py`：量表结构校验脚本，检查生成的JSON是否符合规范

### references/
- `scale-standard.md`：临床心理量表设计规范文档
- `common-scales.md`：常见量表模板参考（焦虑、抑郁、睡眠、职业倦怠等）

### assets/
- `scale-template.json`：标准量表JSON模板文件
- `example-sas.json`：焦虑自评量表（SAS）示例JSON
- `example-sds.json`：抑郁自评量表（SDS）示例JSON
