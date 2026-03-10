# 🧠 PsychoClaw
OpenClaw 专业心理健康测评工具套件

## 项目介绍
PsychoClaw 是专为 OpenClaw 打造的心理健康测评 Skill 套件，包含**量表构建工具**和**对话式测评服务**两大核心功能，内置4个国际公认的标准化心理量表，支持快速生成符合临床规范的量表数据源，以及开箱即用的对话式心理健康筛查服务。

## ✨ 核心功能
### 1. 🛠️ 心理量表构建工具 (`psychological-scale-builder`)
- **自动结构化转换**：将纯文本格式的量表内容自动识别并转换为统一规范的JSON结构
- **结构校验**：自动检查量表必填字段完整性，不符合规范时给出修正建议
- **内置规范**：遵循临床心理学量表设计标准，提供常见量表模板参考
- **批量处理**：支持一次性转换多个量表，统一输出规范格式

### 2. 📊 对话式心理健康测评服务 (`psychological-assessment`)
- **4个内置标准量表**：
  - PHQ-9 抑郁症筛查量表
  - GAD-7 广泛性焦虑障碍量表
  - PSS-10 压力知觉量表
  - PSQI 匹兹堡睡眠质量指数
- **智能交互流程**：通过2-3个引导问题自动推荐合适的测评量表，支持用户自主选择
- **对话式测评**：自然语言逐题询问，无需手动填写冗长问卷，最多10轮对话完成测评
- **自动评分报告**：测评完成后自动计算得分，生成专业评估报告和个性化改善建议
- **记录管理**：自动保存所有测评记录到 `mentalhealth.md`，支持历史查询和统计分析
- **安全合规**：内置心理咨询伦理规范和危机干预流程，高风险情况自动提示就医

## 📁 目录结构
```
psychoclaw/
├── psychological-scale-builder/    # 量表构建工具
│   ├── SKILL.md                    # 技能说明文档
│   ├── scripts/
│   │   ├── scale-converter.py      # 文本转JSON转换脚本
│   │   └── scale-validator.py      # 量表结构校验脚本
│   ├── references/
│   │   ├── scale-standard.md       # 临床心理量表设计规范
│   │   └── common-scales.md        # 常见量表模板参考
│   └── assets/
│       └── scale-template.json     # 标准量表JSON模板
├── psychological-assessment/       # 对话式测评服务
│   ├── SKILL.md                    # 技能说明文档
│   ├── scripts/
│   │   ├── assessment-flow.py      # 测评流程控制脚本
│   │   └── record-manager.py       # 测评记录管理脚本
│   ├── references/
│   │   ├── ethical-guidelines.md   # 心理咨询伦理规范
│   │   └── crisis-intervention.md  # 危机干预指南
│   └── assets/
│       ├── phq9.json               # PHQ-9抑郁量表
│       ├── gad7.json               # GAD-7焦虑量表
│       ├── pss10.json              # PSS-10压力量表
│       └── psqi.json               # PSQI睡眠量表
└── README.md                       # 项目说明文档
```

## 🚀 快速开始
### 环境要求
- Python 3.8+
- OpenClaw 运行环境

### 量表构建工具使用
1. 准备纯文本格式的量表内容
2. 转换为标准JSON：
```bash
python3 psychological-scale-builder/scripts/scale-converter.py input.txt output.json
```
3. 校验量表结构：
```bash
python3 psychological-scale-builder/scripts/scale-validator.py output.json
```

### 对话式测评服务使用
1. 启动测评流程：
```bash
python3 psychological-assessment/scripts/assessment-flow.py
```
2. 查看历史测评记录：
```bash
python3 psychological-assessment/scripts/record-manager.py list
```
3. 查看测评统计信息：
```bash
python3 psychological-assessment/scripts/record-manager.py stat
```

## ⚠️ 重要声明
1. 本工具仅用于心理健康自我筛查，**绝对不能替代专业的临床医学诊断**
2. 如果测评结果显示存在中重度症状，或您感到极其痛苦、影响日常生活，请务必寻求专业心理咨询师或精神科医生的帮助
3. 本工具严格遵循心理咨询伦理规范，所有测评数据仅保存在本地，不会对外泄露
4. 如用户出现自杀/自伤/伤人等高危倾向，本工具会自动提示立即寻求专业医疗帮助

## 📄 许可证
MIT License

## 🤝 贡献
欢迎提交 Issue 和 Pull Request 来完善这个项目~
