# 🧠 PsychoClaw
OpenClaw 专业心理健康测评工具套件

## ⚡ 一键安装
直接在 OpenClaw 中执行以下命令即可安装整套 PsychoClaw 技能：
```bash
# 安装完整套件（两个技能）
openclaw skill install https://github.com/Anctro/psychoclaw.git
```

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
- **对话式测评**：自然语言逐题询问，无需手动填写冗长问卷，最多10轮对话完成测评，测评过程隐藏分值避免用户心理负担
- **自动评分报告**：测评完成后自动计算得分，生成专业评估报告和个性化改善建议
- **记录管理**：自动保存所有测评记录到 `mentalhealth.md`，支持历史查询和统计分析
- **安全合规**：内置心理咨询伦理规范和危机干预流程，高风险情况自动提示就医

### 3. 🧠 智能心理状态评估 (`psychological-intelligent-assessment`)
- **无需答题**：无需用户做量表题，自动基于多源数据分析
- **多源数据融合**：自动读取历史测评记录、用户profile、会话历史综合分析
- **多维度评估**：覆盖抑郁、焦虑、睡眠、压力四个核心维度
- **结论分级**：明确区分「明确判断」、「合理推测」、「数据不足」三种结论可信度
- **个性化建议**：基于用户实际情况给出可落地的改善建议
- **风险预警**：自动检测高风险信号，提示用户寻求专业帮助

### 4. 📋 问卷星快速导入工具 (`questionnaire-star-importer`)
- **双格式支持**：同时生成问卷星「文本快速导入」和「Excel快速导入」两种格式，无需手动调整
- **多输入支持**：支持纯文本、Markdown、心理量表JSON等多种输入格式
- **题型自动识别**：自动识别单选、多选、量表、填空等常见题型，支持自定义题型映射
- **心理量表适配**：支持直接将PsychoClaw的心理量表JSON一键转换为问卷星格式
- **格式自动校验**：自动检查是否符合问卷星导入规范，不符合时给出修正建议
- **批量处理**：支持一次性转换多个问卷/量表，批量生成导入文件

## 📁 目录结构
```
psychoclaw/
├── psychological-scale-builder/        # 量表构建工具
│   ├── SKILL.md                        # 技能说明文档
│   ├── scripts/
│   │   ├── scale-converter.py          # 文本转JSON转换脚本
│   │   └── scale-validator.py          # 量表结构校验脚本
│   ├── references/
│   │   ├── scale-standard.md           # 临床心理量表设计规范
│   │   └── common-scales.md            # 常见量表模板参考
│   └── assets/
│       └── scale-template.json         # 标准量表JSON模板
├── psychological-assessment/           # 对话式测评服务
│   ├── SKILL.md                        # 技能说明文档
│   ├── scripts/
│   │   ├── assessment-flow.py          # 测评流程控制脚本
│   │   └── record-manager.py           # 测评记录管理脚本
│   ├── references/
│   │   ├── ethical-guidelines.md       # 心理咨询伦理规范
│   │   └── crisis-intervention.md      # 危机干预指南
│   └── assets/
│       ├── phq9.json                   # PHQ-9抑郁量表
│       ├── gad7.json                   # GAD-7焦虑量表
│       ├── pss10.json                  # PSS-10压力量表
│       └── psqi.json                   # PSQI睡眠量表
├── psychological-intelligent-assessment/ # 智能心理状态评估
│   ├── SKILL.md                        # 技能说明文档
│   ├── scripts/
│   │   └── intelligent-analyzer.py     # 智能分析脚本
│   └── references/
│       └── analysis-framework.md       # 心理学分析框架（专家版）
├── questionnaire-star-importer/        # 问卷星快速导入工具
│   ├── SKILL.md                        # 技能说明文档
│   ├── scripts/
│   │   ├── txt-converter.py            # 转换为问卷星文本导入格式
│   │   ├── excel-converter.py          # 转换为问卷星Excel导入格式
│   │   └── scale-converter.py          # 心理量表JSON转问卷星格式专用脚本
│   ├── references/
│   │   ├── format-spec.md              # 问卷星导入格式官方规范
│   │   └── question-type-mapping.md    # 题型映射规则说明
│   └── assets/
│       └── text-template.txt           # 文本导入格式模板
└── README.md                           # 项目说明文档
```

## 🚀 快速开始
### 安装
直接在 OpenClaw 中执行一键安装命令即可安装整套技能：
```bash
openclaw skill install https://github.com/Anctro/psychoclaw.git
```
安装完成后可通过 `openclaw skill list` 查看已安装的三个技能。

---
### 使用方法
所有技能均支持直接通过 OpenClaw 命令调用，无需关注底层实现：

#### 1. 🛠️ 心理量表构建工具
**功能**：将纯文本量表转换为标准JSON格式
**使用场景**：制作新的心理测评量表、标准化现有量表
```bash
# 转换文本量表为标准JSON
openclaw skill run psychological-scale-builder convert <input.txt> <output.json>

# 校验量表结构是否符合规范
openclaw skill run psychological-scale-builder validate <scale.json>
```

#### 2. 📊 对话式心理健康测评
**功能**：通过自然对话完成心理测评，无需手动填写问卷
**使用场景**：用户需要进行抑郁/焦虑/压力/睡眠测评
```bash
# 启动对话式测评
openclaw skill run psychological-assessment

# 查看历史测评记录
openclaw skill run psychological-assessment records

# 查看测评统计信息
openclaw skill run psychological-assessment stat
```
也可以直接在对话中触发：用户说「我要做心理测评」、「测一下我的压力」等即可自动启动。

#### 3. 🧠 智能心理状态评估
**功能**：无需答题，基于用户历史数据自动分析心理状态
**使用场景**：用户说「评估一下我现在的心理状态」、「分析我的心理情况」
```bash
# 生成智能评估报告
openclaw skill run psychological-intelligent-assessment
```
无需用户输入任何内容，系统会自动读取历史测评记录、用户特征、会话历史进行综合分析，直接输出评估报告。

## ⚠️ 重要声明
1. 本工具仅用于心理健康自我筛查，**绝对不能替代专业的临床医学诊断**
2. 如果测评结果显示存在中重度症状，或您感到极其痛苦、影响日常生活，请务必寻求专业心理咨询师或精神科医生的帮助
3. 本工具严格遵循心理咨询伦理规范，所有测评数据仅保存在本地，不会对外泄露
4. 如用户出现自杀/自伤/伤人等高危倾向，本工具会自动提示立即寻求专业医疗帮助

## 📄 许可证
MIT License

## 🤝 贡献
欢迎提交 Issue 和 Pull Request 来完善这个项目~
