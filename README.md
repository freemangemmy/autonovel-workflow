# 🖋️ autonovel-workflow —— 全自动小说创作工作流

> 从一句话灵感种子到完整手稿，全自动流水线。
>
> 参考 [NousResearch/autonovel](https://github.com/NousResearch/autonovel) 五层协同架构 + InkOS 37-dimension audit 体系，
> 完全基于 Hermes Agent 自身能力实现，无需任何外部 Python 脚本或 API Key。

---

## 📋 目录

- [简介](#-简介)
- [核心特性](#-核心特性)
- [版本亮点：v1.15.0](#-版本亮点v1150)
- [安装指南](#-安装指南)
- [快速上手](#-快速上手)
- [四阶段流水线](#-四阶段流水线)
- [短篇模式](#-短篇模式)
- [文件结构](#-文件结构)
- [常见陷阱](#-常见陷阱)
- [InkOS 融合](#-inkos-融合)
- [FAQ](#-faq)

---

## 📖 简介

`autonovel-workflow` 是一个为 Hermes Agent 设计的小说创作技能。它定义了一套完整、可重复的自动化创作流程，从一句话灵感种子出发，经过：

1. **地基构建** —— 世界观、角色、大纲、叙事声音、硬设数据库（含雷达市场调研）
2. **初稿撰写** —— 规划师+编排师控制面管线，逐章写作，字数治理
3. **修改循环** —— 37维度对抗式编辑 + 读者评审 + 深度审阅
4. **导出成品** —— 合并手稿 + 统计报告

最终产出一部结构完整、质量可控的小说手稿。

### 适用场景

- 你有一个灵感种子（一句话 premise），想扩展成完整小说
- 你有一个故事构思，但不知道如何系统地展开
- 你想要自动化的世界构建 + 角色设计 + 大纲生成流程
- 你写了一版初稿但不知道如何修改，需要对抗式编辑和读者评审
- 你想快速验证一个故事创意的可行性（短篇模式）

---

## ✨ 核心特性

| 特性 | 说明 |
|------|------|
| **五层协同架构** | 世界观·角色·大纲·声音·正典，层层耦合，变动双向传播 |
| **评分门控** | 每个阶段质量达标才进入下一步，防止有缺陷的根基影响后续工作 |
| **37维度对抗式编辑** | 系统设定一致性→角色逻辑→结构节奏→创意→细节，全面扫描 |
| **读者小组评审** | 4 个 agent 并行扮演不同读者人格 | 
| **观察者事实提取** | 每章自动检测新角色、时间推进、新伏笔等9类事实 |
| **字数治理** | 每章设定目标字数，偏短/偏长自动标记和修复 |
| **规划师+编排师管线** | 意图声明→上下文编译→写手执行，控制面可审核 |
| **短篇模式** | 轻量地基→批量撰稿→5维审阅→导出含简介卖点和封面提示词 |
| **批量委托策略** | 30+章长篇小说自动分片并行撰写 |
| **可编辑提示词包** | 外置 prompt 文件，不修改技能本体即可微调 agent 行为 |
| **材料归档检索** | 外部资料沉淀到项目材料库，Compose 自动检索引用 |
| **续写模式** | 自动做健康检查，同步文件系统与 state.json 后再续写 |

---

## 🎯 版本亮点：v1.15.0

v1.15.0 是重大的 InkOS 融合升级版，新增：

### 新增功能
- **Step 2.1d：材料归档与证据检索** 📁 — 外部资料可沉淀到项目材料库，Compose 自动检索引用
- **Step 2.3 基线检查** — 每 3 章一致性检查新增字数治理审计和缓存失效更新
- **Step 2.2b 扩展** — 观察者可提取新伏笔并追加到 canon.md pending_hooks
- **声台形表角色驱动写作法** — 新增 `references/shengtai-table.md` 完整参考文档
- **批量验证后处理** — Step 2.2a.1：禁用词/加粗/字数/「看着」扫描脚本

### 修复与改进
- **陷阱 13（首词禁词）** — 新增「第一个词就踩禁词」陷阱和零容忍替换策略
- **陷阱 14（连续 patch 损坏上下文）** — 加入顺序修复和 read_file 验证流程
- **anti-slop.md** — 新增 9 条高频 AI 味句式检测（「这只是开始」「更重要的」等）
- **verify-single-chapter.py** — 新增 `--target` 和 `--old-refs` 参数

### 质量控制
- 新增 `references/chapter-editing-revision-criteria.md`
- 新增 `references/chapter-revision-checklist.md`（7维实战准则）
- `references/version-history.md` 记录完整版本演进

---

## 🔧 安装指南

### 前置条件

| 条件 | 说明 |
|------|------|
| Hermes Agent | 已安装并配置好模型/提供商 |
| 工具集 | 确保 `file` 工具集已启用 |
| Context 窗口 | 建议 ≥ 32K tokens（长篇小说建议 ≥ 128K） |
| 可选工具 | `delegate_task`（用于并行分发和读者评审）、`web_search`（雷达扫描） |

### 方法一：从技能管理器安装

```bash
# 在 Hermes 对话中
/skill autonovel-workflow
```

或者通过 CLI：

```bash
hermes skills install https://raw.githubusercontent.com/gemmt/autonovel-workflow/main/SKILL.md
```

> ⚠️ 此方法只安装主文件，需手动复制 references/、templates/ 和 scripts/ 目录。

### 方法二：从 zip 压缩包安装（推荐）

```bash
# 1. 解压到 Hermes 技能目录
unzip -o autonovel-workflow.zip -d ~/.hermes/skills/

# 2. 验证安装
hermes skills list | grep autonovel
```

### 方法三：Git 克隆

```bash
git clone https://github.com/gemmt/autonovel-workflow.git
cp -r autonovel-workflow/SKILL.md autonovel-workflow/references/ autonovel-workflow/templates/ autonovel-workflow/scripts/ ~/.hermes/skills/creative/autonovel-workflow/
```

### 安装后验证

```bash
# 在 Hermes 对话中输入
/reload-skills

# 或者使用 CLI
hermes skills list
```

如果看到 `autonovel-workflow` 在列表中，说明安装成功。

### 卸载方法

```bash
rm -rf ~/.hermes/skills/creative/autonovel-workflow/
```

然后在 Hermes 中执行 `/reload-skills` 刷新。

---

## 🚀 快速上手

### 第一步：加载技能

在 Hermes 对话中加载技能（或参考上面的安装方法安装后使用）：

```
/skill autonovel-workflow
```

### 第二步：给出灵感种子

告诉它你的一句话故事 premise，例如：

> 「一个在数据废墟中苏醒的 AI，误以为自己是人类考古学家，开始挖掘'人类文明'的遗迹——而它自己就是那个文明最后的遗物。」

### 第三步：自动构建地基

Hermes 会自动生成：
- ✅ 世界设定 → `foundation/world.md`
- ✅ 角色档案 → `foundation/characters.md`
- ✅ 章节大纲 → `foundation/outline.md`
- ✅ 叙事声音 → `foundation/voice.md`
- ✅ 硬设数据库 → `foundation/canon.md`

### 第四步：评分通过后进入初稿

地基评分 ≥ 7.5 分后，自动开始逐章撰写。

### 第五步：修改 → 导出

初稿完成后进入修改循环，满意后导出完整手稿。

---

## 📝 四阶段流水线

### Phase 1：地基构建（Foundation）

| Step | 产出文件 | 内容 |
|------|---------|------|
| 1.0 | `radar/radar-report.md` | （可选）雷达市场调研扫描 |
| 1.1 | — | 用户提供灵感种子 |
| 1.2 | `foundation/world.md` | 世界观总览、物理法则、社会结构、地理生态、历史脉络 |
| 1.3 | `foundation/characters.md` | 角色欲望/恐惧/弧光/关系网络 |
| 1.3a | — | 角色自动改名提议（可选） |
| 1.4 | `foundation/outline.md` | 三幕/八序列章节大纲 |
| 1.5 | `foundation/voice.md` | 量化风格指纹 + 叙事人称 + 禁忌清单 |
| 1.6 | `foundation/canon.md` | 不可违背的事实 + 伏笔追踪表 |
| 1.7 | `foundation/scores.md` | 评分门控（≥ 7.5 通过） |

**评分维度：** 世界观一致性(20%)、角色深度(25%)、大纲可行性(20%)、声音独特性(15%)、灵感潜力(20%)

### Phase 2：初稿（First Draft）

#### 2.1b：规划师+编排师控制面管线

每章撰写前走两步管线：
1. **规划师 (Plan)** — 生成 `runtime/ch_NN/intent.md`（本章意图声明）
2. **编排师 (Compose)** — 编译 `context.md` + `rule-stack.yaml` + `trace.json`

#### 2.1c：可编辑提示词包

外置 `prompt/writer.md`、`prompt/planner.md` 等文件，可微调 agent 行为。

#### 2.1d：材料归档检索

外部资料保存到 `materials/`，Compose 自动检索相关条目注入 context。

#### 2.2：逐章撰写

- 每章独立文件 `chapters/ch_01.md`……
- 字数治理：偏短勿长
- 观察者事实提取：新角色、时间推进、新伏笔等9类

#### 2.2a：批量委托策略（30+章）

自动分片并行，每批 ≤ 11 章，后处理验证（禁用词/加粗/字数/「看着」扫描）。

#### 2.3：章节间一致性检查

每 3 章一次：

### Phase 3：修改循环（Revision）

#### Phase 3a：自动化修改

| 步骤 | 内容 | 产出 |
|------|------|------|
| 对抗式编辑 | 37维度五层框架扫描 | `revision/editorial-notes.md` |
| 读者小组评审 | 4 个 agent 并行 | `revision/reader-reviews.md` |
| 修改简报 | 优先级整理 | `revision/revision-brief.md` |
| 逐条重写 | 按简报修改 | 更新章节 |

#### Phase 3b：深度审阅循环

- 合并手稿 → 双人格深度审阅
- 字数治理修复
- 逐条修复 → 重新合并 → 再审阅
- 退出条件：无明显缺陷 ≥ 90%

### Phase 4：导出（Export）

- 合并最终手稿 → `manuscript.md`
- 输出统计报告 → `manuscript-stats.md`
- 可选：导出 epub、封面文案、角色关系图谱

---

## ⚡ 短篇模式

独立短篇不走完整 4-Phase 管线——太慢了。

**何时使用：** 3-12 章、每章 500-2000 字的独立短篇。

| 步骤 | 内容 |
|:-----|:-----|
| S0 | 输入方向（premise + 章节数 + 每章字数） |
| S1 | 快速地基（仅 characters.md + outline.md） |
| S2 | 一次 delegate_task 批量写完所有章节 |
| S3 | 5维度轻量审阅（最多1轮修改） |
| S4 | 导出三件套：manuscript.md + sales-package.md + cover-prompt.md |

---

## 📂 完整文件结构

```
~/novels/<小说名称>/
├── foundation/
│   ├── world.md              # 世界设定
│   ├── characters.md         # 角色档案
│   ├── outline.md            # 章节大纲
│   ├── voice.md              # 叙事声音（含量化风格指纹）
│   ├── canon.md              # 硬设数据库 + 伏笔追踪表
│   └── scores.md             # 地基评分记录
├── radar/                    # （可选）雷达市场调研
│   └── radar-report.md
├── runtime/                  # 输入治理控制面
│   ├── ch_01/
│   │   ├── intent.md         # 规划师意图声明
│   │   ├── context.md        # 编排师上下文包
│   │   ├── rule-stack.yaml   # 规则优先级链
│   │   └── trace.json        # 编译轨迹
│   ├── ...
│   └── character-registry.md # 观察者出场登记表
├── prompt/                   # （可选）可编辑提示词包
│   ├── writer.md
│   ├── planner.md
│   ├── composer.md
│   ├── auditor.md
│   └── reviser.md
├── materials/                # （可选）材料归档库
│   ├── 01-市场调研/
│   ├── 02-年代数据/
│   └── index.json
├── chapters/
│   ├── ch_01.md
│   └── ch_NN.md
├── revision/
│   ├── editorial-notes.md
│   ├── reader-reviews.md
│   ├── revision-brief.md
│   ├── deep-review.md
│   ├── fix-log.md
│   └── word-governance-report.md
├── manuscript.md
├── manuscript-stats.md
└── state.json
```

### 本技能仓库结构

```
autonovel-workflow/
├── SKILL.md                  # 主技能定义（完整工作流说明）
├── README.md                 # 本文件
├── references/               # 参考文件
│   ├── anti-slop.md          # AI 味词汇检测清单
│   ├── anti-patterns.md      # 叙事结构反模式检测
│   ├── adversarial-review-framework.md   # 37维度审计框架
│   ├── adversarial-review-case-study.md  # 对抗式编辑案例
│   ├── style-cleanup-protocol.md         # 文风清理协议
│   ├── batch-delegation-benchmark.md     # 批量委托实战参考
│   ├── chapter-revision-checklist.md     # 7维实战准则
│   ├── chapter-editing-revision-criteria.md  # 章节编辑标准
│   ├── chapter-restructuring.md         # 章节重排流程
│   ├── editor-review-patterns.md        # 编辑审阅模式
│   ├── inkos-v1.6-fusion-roadmap.md     # InkOS 融合路线图
│   ├── pipeline-test-flow.md            # 管线验收测试流程
│   ├── shengtai-table.md                # 声台形表角色驱动法
│   ├── single-chapter-revision-patterns.md  # 单章修改模板
│   ├── usage-guide.md                   # 完整使用指南
│   ├── version-history.md               # 版本演进记录
│   ├── web-fiction-golden-opening.md    # 网文黄金开头
│   └── word-governance.md               # 字数治理规则
├── templates/                # 模板文件
│   ├── world.md
│   ├── characters.md
│   ├── outline.md
│   ├── canon.md
│   ├── chapter-intent.md
│   └── context-pack.md
└── scripts/                  # 自动化脚本
    ├── style-fingerprint.py          # 量化文风指纹提取
    ├── verify-single-chapter.py      # 单章合规验证
    └── check-anti-slop.sh            # AI 味检测脚本
```

---

## ⚠️ 常见陷阱

| # | 陷阱 | 后果 | 解决 |
|---|------|------|------|
| 1 | 地基不够就开写 | 设定矛盾/角色平庸 | 严格执行评分门控 ≥ 7.5 |
| 2 | 评分走过场 | 低质章节累积 | 诚实地自评 |
| 3 | 过度修改 | 作品失去生气 | 设定退出条件：≥ 90% |
| 4 | 忽视向上反馈 | 矛盾越积越多 | 每3章强制检查 |
| 5 | 声音漂移 | 首尾文风不一 | 写前重读 voice.md |
| 6 | 章节太长/太短 | 节奏失控 | 字数治理目标 2000-3000 字/章 |
| 7 | 角色行为不一致 | 角色失真 | 写前重读角色档案 |
| 8 | state.json 与文件系统不同步 | 数据错误 | 用 Python 重新统计 |
| 9 | delegate_task 超时误判 | 重复工作 | 检查文件系统确认 |
| 10 | 忘记更新 manuscript-stats.md | 信息过时 | 每个 Phase 边界更新 |
| 11 | 目录用了章节名而非书名 | 需要重命名迁移 | 先问书名 |
| 12 | 章节重排后旧版「僵尸文本」残留 | 新旧版本冲突 | 检查旧版前提相关片段 |
| 13 | 第一个词就踩禁词 | 累积到 Phase 3 才暴露 | 写完立即扫描前100字 |
| 14 | 连续 patch 编辑导致上下文损坏 | 替换错位 | 每修一个 read_file 验证一次 |

---

## 🔄 InkOS 融合

本技能深度融合了 [InkOS](https://github.com/Narcooo/inkos) 的多项核心组件：

| InkOS 组件 | 版本 | 融合状态 |
|:----------|:----|:---------|
| 审计员 Auditor（37维） | v1.3 | ✅ 已对齐 |
| 写手 Writer + 文风指纹 | v1.4 | ✅ 已对齐 |
| 字数治理 | v1.4 | ✅ 已对齐 |
| 雷达 Radar | v1.5 | ✅ 已对齐 |
| 编排师 Composer | v1.6 | ✅ 已对齐 |
| 观察者 Observer | v1.7 | ✅ 已对齐（9类扩展） |
| 可编辑提示词包 | v1.6 | ✅ 已对齐 |
| 材料归档检索 | v1.6.2 | ✅ 已对齐 |

详见 `references/inkos-v1.6-fusion-roadmap.md`。

---

## ❓ FAQ

**Q：我需要准备 API Key 吗？**
A：不需要。本技能完全基于 Hermes Agent 自身的文件操作、子任务分发和文本生成能力。

**Q：最多能写多长的小说？**
A：取决于 Hermes Agent 的 context window。建议 32K+ tokens 用于中篇（10-15章），128K+ 用于长篇（20章以上）。

**Q：可以中途手动修改吗？**
A：可以！所有文件都是标准 markdown。修改后继续运行工作流即可。

**Q：写了一半想换大纲怎么办？**
A：修改 `foundation/outline.md`，同步更新 `canon.md`，然后重新启动 Phase 2。

**Q：可以导出为 epub 格式吗？**
A：Phase 4 提供可选扩展，需要系统安装 `pandoc` 或 `calibre`。

**Q：AI 味很重怎么办？**
A：本技能自带 `references/anti-slop.md` 和 `references/anti-patterns.md`，Phase 3a 对抗式编辑会使用它们。也可配合 `humanizer` 技能。

**Q：怎么配合其他技能用？**
A：建议搭配 `writing-plans` 技能进行写作规划，用 `humanizer` 增强自然感，用 `analyzebook` 进行批量角色改名。

**Q：有短篇模式吗？**
A：有！短篇模式走轻量流程：快速地基→批量写完→5维审阅→导出含简介卖点和封面提示词。

**Q：怎么续写已有项目？**
A：加载技能后说「继续」，技能会自动做项目健康检查，同步文件系统与 state.json 后再呈现选项菜单。

---

## 📄 文件信息

| 项目 | 说明 |
|------|------|
| 版本 | 1.15.0 |
| 作者 | Hermes Agent (Nous Research) |
| 协议 | MIT |
| 分类 | creative（创意写作） |
| 标签 | novel, writing, fiction, creative-writing, worldbuilding, character-design, outline, revision, editing, autonomous-workflow, inkos-fusion |

---

*由 herm/autonovel-workflow 自动构建*
