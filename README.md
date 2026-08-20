<p align="center">
  <img src="https://img.shields.io/badge/autonovel--workflow-v1.15.0-blue?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/Hermes_Agent-Skill-FF6B35?style=for-the-badge" alt="Hermes Agent Skill">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/dynamic/json?style=for-the-badge&label=stars&query=stargazers_count&url=https%3A%2F%2Fapi.github.com%2Frepos%2Fgemmt%2Fautonovel-workflow&color=yellow" alt="Stars">
</p>

<h1 align="center">autonovel-workflow<br><sub>全自动小说创作工作流 — Autonomous Novel Writing Pipeline</sub></h1>

<p align="center">
  <strong>从一句话灵感种子到完整手稿，全自动流水线。</strong><br>
  <em>From a single spark of inspiration to a complete manuscript — fully automated.</em>
</p>

<p align="center">
  <a href="readme_cn.md">中文</a> · <a href="readme_en.md">English</a>
</p>

---

<p align="center">
  🚀 <strong>v1.15.0 最新亮点</strong> — Input Governance 控制面 · Editable Prompt Packs · Material Archive · Short Run 短篇模式
</p>

---

### 快速导航 / Quick Links

| 语言 | 文档 | 内容 |
|:----|:-----|:-----|
| 🇨🇳 中文 | [readme_cn.md](readme_cn.md) | 完整中文说明（核心架构、四阶段流水线、短篇模式、InkOS 融合矩阵、安装指南） |
| 🇬🇧 English | [readme_en.md](readme_en.md) | Full English documentation (architecture, 4-phase pipeline, Short Story Mode, integration matrix, installation) |
| 📄 SKILL.md | [SKILL.md](SKILL.md) | 主技能定义 / Main skill definition |
| 📋 版本历史 | [references/version-history.md](references/version-history.md) | 完整版本演进记录 |

---

### 核心特性 / Core Features

| | 特性 | 说明 / Description |
|:--|:-----|:-------------------|
| 🏗️ | **五层协同架构** | voice → world → characters → outline → chapters 层层耦合，变动双向传播 |
| 🎯 | **评分门控** | Phase 1 地基评分 ≥ 7.5 才允许进入写作，防止烂尾 |
| 🧠 | **Input Governance** (v1.12) | plan→compose 双层控制面，写手只读精简上下文，不读全量 foundation |
| 📝 | **Editable Prompt Packs** (v1.13) | agent 提示词外置可编辑，删除即回退 |
| 📁 | **Material Archive** (v1.14) | 外部资料归档检索，Compose 联动引用 |
| ⚡ | **Short Run 短篇模式** (v1.15) | 轻量独立管线，5-10 分钟快速产出 |
| 🔄 | **并行写作** | delegate_task 批量委托，50+ 章长篇已验证 |
| 🎭 | **37 维度审计** | 对抗式编辑 + 读者小组评审 + 深度审阅循环 |
| 🧹 | **AI 味清除** | anti-slop 检测 + 风格指纹 + 字数治理 |

---

### 四阶段流水线 / 4-Phase Pipeline

```
Phase 1: 地基构建 Foundation  ──→  Phase 2: 初稿撰写 First Draft  ──→  Phase 3: 修改循环 Revision  ──→  Phase 4: 导出 Export
(评分门控 ≥ 7.5)               (字数治理 + 批量委托)                (37维审计 + 深度审阅)                (手稿 + 统计)
```

---

### 文件导航 / File Navigation

```
autonovel-workflow/
├── SKILL.md                              # 主技能定义
├── README.md                             # 本文件 / This file (landing page)
├── readme_cn.md                          # 中文说明文档
├── readme_en.md                          # English documentation
├── references/                           # 参考文档 / References
│   ├── version-history.md                # 版本历史
│   ├── adversarial-review-framework.md   # 37 维度审计框架
│   ├── adversarial-review-case-study.md  # 实战案例
│   ├── batch-delegation-benchmark.md     # 批量委托基准
│   ├── style-cleanup-protocol.md         # 文风清理
│   ├── inkos-fusion-pattern.md           # InkOS 融合指南
│   ├── inkos-v1.6-fusion-roadmap.md      # 融合路线图
│   ├── anti-patterns.md                  # 反模式检测
│   ├── anti-slop.md                      # AI 味检测
│   ├── radar-report-template.md          # 雷达报告模板
│   ├── word-governance.md                # 字数治理
│   ├── chapter-editing-revision-criteria.md
│   ├── chapter-restructuring.md
│   ├── chapter-revision-checklist.md
│   ├── editor-review-patterns.md
│   ├── pipeline-test-flow.md
│   ├── shengtai-table.md
│   ├── single-chapter-revision-patterns.md
│   ├── usage-guide.md
│   └── web-fiction-golden-opening.md
├── templates/                            # 模板 / Templates
│   ├── world.md / characters.md / outline.md
│   ├── voice.md / canon.md
│   └── chapter-intent.md / context-pack.md
└── scripts/                              # 脚本 / Scripts
    ├── style-fingerprint.py
    ├── check-anti-slop.sh
    └── verify-single-chapter.py
```

---

### 许可 / License

MIT
