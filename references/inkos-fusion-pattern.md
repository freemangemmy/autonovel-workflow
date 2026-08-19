# InkOS 融合模式指南

> 记录如何将 InkOS（或类似外部创作 Agent 系统）的特性融合进 autonovel-workflow。
> 适用于后续的持续迭代（如 多模型路由、局部章节重写 等）。

---

## 融合步骤

### Step 1 — 查找特征

从 InkOS 上游 README（https://github.com/Narcooo/inkos）获取特征描述。

**坑：** 不要用第三方平台（如 ClawHub SKILL.md）的缓存数据——它们可能落后数个版本。
**实战教训（2026-06-14）：** ClawHub 显示 33 维度，上游 README 实际是 37 维度。

### Step 2 — 设计 Hermes 原生等价物

| InkOS 特性 | Hermes 等价物 |
|:-----------|:--------------|
| 独立的 Agent 角色 | `delegate_task` + 心智切换约束 |
| 专用 CLI 命令 | `terminal` + `write_file` 组合 |
| SQLite 记忆库 | `state.json` + foundation/*.md |
| 多模型路由 | 配置文件的 `model` 字段（将来支持） |
| 编辑提示词包 | `prompt/` 目录 + 三层叠加载 |
| 材料归档检索 | `materials/` 目录 + `index.json` |

### Step 3 — 修改 SKILL.md

- 插入新 Step（如 Step 1.0、Step 2.1b、Step 3b.2b）
- 更新流程编号（后续步骤重编号）
- **插入位置原则：** 放在最接近执行时机的阶段。Phase 开头加 Step 0（如雷达）、Phase 中间加 Step b（如编排师、字数治理）

### Step 4 — 创建参考文件

| 文件类型 | 路径 | 用途 |
|:---------|:-----|:-----|
| 参考文档 | `references/<feature>.md` | 详细说明、表格、案例 |
| 模板 | `templates/<name>.md` | 供复制的起始文件 |
| 脚本 | `scripts/<name>.py` | 可重用的自动化工具 |

### Step 5 — 更新项目实例

- 更新 `state.json` 增加新字段
- 更新 `manuscript-stats.md` 增加新指标
- 如果适用，对项目实例做首次初始化

### Step 6 — 版本号 + 描述

- 大功能（新增 Agent 角色/Phase）：x.**0** → x+1.**0**
- 小功能（深化已有能力）：x.**y** → x.**y+1**
- 更新 `description` 字段以反映新增融合

### Step 7 — 验证

- `skill_view` 检查 SKILL.md 完整性
- 检查 reference templates 是否正确
- 检查 state.json schema 是否一致

---

## 已完成融合

| Agent / 组件 | 融合方式 | 位置 | 版本 |
|:-------------|:---------|:-----|:----|
| **审计员 (Auditor)** 🔴 | 37 维度审计框架 + 伏笔追踪 | Step 3a.1 + `references/adversarial-review-framework.md` + canon.md | v1.3.0 |
| **写手 (Writer)** 🖊️ | 文风量化(voice.md) + 字数治理 | Step 1.5 + Step 2.2 + `references/word-governance.md` | v1.4.0 |
| **雷达 (Radar)** 📡 | 市场调研扫描 | Step 1.0 + `references/radar-report-template.md` | v1.5.0 |
| **编排师 (Composer)** 📦 | 上下文编译 + 规则栈 | Step 2.1b + `templates/context-pack.md` | v1.6.0 |
| **观察者 (Observer)** 🔍 | 9 类事实提取 + 伏笔自动检测 | Step 2.2b + `templates/character-registry.md` | v1.7.0 → v1.10 |
| **输入治理 (Input Governance)** 🧠 | plan→compose 双层控制面 | Step 2.1b + `templates/chapter-intent.md` + rule-stack.yaml + trace.json | **v1.12.0** |
| **可编辑提示词包** 📝 | 外置 agent 提示词 + 三层叠加载 | Step 2.1c + `prompt/` 目录 | **v1.13.0** |
| **材料归档检索 (Material Archive)** 📁 | 外部资料沉淀 + Compose 联动 + evidence trace | Step 2.1d + `materials/` + `index.json` | **v1.14.0** |
| **短篇模式 (Short Run)** ⚡ | 轻量独立管线 + 导出三件套 | Short Story Mode S1-S4 | **v1.15.0** |

### 融合要点

**Input Governance (v1.12)：**
- 规划师 (Planner)：读 foundation + 上章 + 状态，生成本章意图声明（intent.md）
- 编排师 (Composer)：读 intent + foundation + 状态，编译上下文包 + 规则栈 + 轨迹
- 写手只读 compose 产物，不读全量 foundation
- intent.md 可人工编辑，删除即可回退到旧流程

**可编辑提示词包 (v1.13)：**
- `prompt/` 目录下存放 writer/planner/composer/auditor/reviser 五个文件
- 三层叠加载：`prompt/<agent>.md` > 项目 `.inkos/prompts/` > 内置默认值
- 编辑原则：只微调语气/侧重/约束，不覆盖核心逻辑

**材料归档 (v1.14)：**
- `materials/` 目录按主题分组，每条材料含元信息块 + 证据标记
- `materials/index.json` 自动维护索引
- Compose 编译时自动检索与本章 POV/场景/标签相关的材料

---

## 待融合

| 特性 | 优先级 | 预估工时 | 方案参考 |
|:-----|:------|:---------|:---------|
| **局部章节重写** | 高 | 30 分钟 | 重写半章 + 级联更新后续 truth 文件 |
| **多模型路由** | 中 | 15 分钟 | state.json 加 model_routing 字段，不同 agent 走不同模型 |
| **自定义 agent 插件** | 低 | 待评估 | 参考 InkOS Skill 系统设计 |
| **平台格式导出** | 低 | 20 分钟 | 起点/番茄等平台格式适配 |
