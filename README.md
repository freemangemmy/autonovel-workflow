# 🖋️ autonovel-workflow —— 全自动小说创作工作流

> 从一句话灵感种子到完整手稿，全自动流水线。
>
> 参考 [NousResearch/autonovel](https://github.com/NousResearch/autonovel) 五层协同架构，完全基于 Hermes Agent 自身能力实现，无需任何外部 Python 脚本或 API Key。

---

## 📋 目录

- [简介](#-简介)
- [核心架构](#-核心架构)
- [安装指南](#-安装指南)
- [快速上手](#-快速上手)
- [四阶段流水线详解](#-四阶段流水线详解)
- [文件结构](#-文件结构)
- [常见陷阱](#-常见陷阱)
- [FAQ](#-faq)

---

## 📖 简介

`autonovel-workflow` 是一个为 Hermes Agent 设计的小说创作技能。它定义了一套完整、可重复的自动化创作流程，从一句话灵感种子出发，经过：

1. **地基构建** —— 世界观、角色、大纲、叙事声音、硬设数据库
2. **初稿撰写** —— 逐章写作，每章质量门控
3. **修改循环** —— 对抗式编辑 + 读者评审 + 深度审阅
4. **导出成品** —— 合并手稿 + 统计报告

最终产出一部结构完整、质量可控的小说手稿。

### 适用场景

- 你有一个灵感种子（一句话 premise），想扩展成完整小说
- 你有一个故事构思，但不知道如何系统地展开
- 你想要自动化的世界构建 + 角色设计 + 大纲生成流程
- 你写了一版初稿但不知道如何修改，需要对抗式编辑和读者评审
- 你想快速验证一个故事创意的可行性

---

## 🏗️ 核心架构

### 五层协同设计

```
Layer 5:  voice.md          —— 怎么写（叙事声音、文风调性）
Layer 4:  world.md          —— 什么存在（世界观设定、物理/社会规则）
Layer 3:  characters.md     —— 谁行动（角色档案、动机弧光、关系网）
Layer 2:  outline.md        —— 发生什么（章节大纲、情节 beats）
Layer 1:  chapters/*.md     —— 实际文本（逐章小说正文）
Cross:    canon.md           —— 什么是真的（硬设数据库、不可违背的事实）
```

### 变动双向传播原则

- **向下影响：** 上层变动（如修改世界观）→ 下层自动调整（如重写相关章节的对话）
- **向上反馈：** 下层写作过程中发现的设定矛盾 → 更新上层 canon.md 和 world.md

### 评分门控

每个阶段完成时进行质量评分，只有达标才能进入下一阶段，防止有缺陷的根基影响后续所有工作。

---

## 🔧 安装指南

### 前置条件

| 条件 | 说明 |
|------|------|
| Hermes Agent | 已安装并配置好模型/提供商 |
| 工具集 | 确保 `file` 工具集已启用（`hermes tools enable file`） |
| Context 窗口 | 建议 ≥ 32K tokens（长篇小说建议 ≥ 128K） |
| 可选工具 | `delegate_task`（用于读者小组评审并行分发） |

### 安装方法

#### 方法一：从 zip 压缩包安装（推荐）

如果你已拿到 `autonovel-workflow.zip`：

```bash
# 1. 解压到 Hermes 技能目录
unzip -o autonovel-workflow.zip -d ~/.hermes/skills/

# 2. 验证安装
hermes skills list | grep autonovel
```

#### 方法二：直接复制文件

```bash
# 创建目录
mkdir -p ~/.hermes/skills/creative/autonovel-workflow/
mkdir -p ~/.hermes/skills/creative/autonovel-workflow/references/
mkdir -p ~/.hermes/skills/creative/autonovel-workflow/templates/

# 复制文件（将以下文件放入对应目录）
# SKILL.md           → creative/autonovel-workflow/
# anti-slop.md       → creative/autonovel-workflow/references/
# anti-patterns.md   → creative/autonovel-workflow/references/
# world.md           → creative/autonovel-workflow/templates/
# characters.md      → creative/autonovel-workflow/templates/
# outline.md         → creative/autonovel-workflow/templates/
# canon.md           → creative/autonovel-workflow/templates/
```

#### 方法三：远程 URL 安装

如果 SKILL.md 托管在可访问的 URL 上：

```bash
hermes skills install https://你的网址/SKILL.md
```

> ⚠️ 此方式只安装主文件，不会自动拉取 `references/` 和 `templates/` 目录。建议配合方法一使用。

### 安装后验证

```bash
# 刷新技能列表（在 Hermes 对话中输入）
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

在 Hermes 对话中：

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

## 📝 四阶段流水线详解

### Phase 1：地基构建（Foundation）

**目标：** 从种子概念出发，构建完整的五层设定体系。

| Step | 产出文件 | 内容 |
|------|---------|------|
| 1.1 | — | 用户提供灵感种子 |
| 1.2 | `foundation/world.md` | 世界观总览、物理法则、社会结构、地理生态、历史脉络 |
| 1.3 | `foundation/characters.md` | 角色欲望/恐惧/弧光/关系网络（至少主角+反派+2-5配角） |
| 1.4 | `foundation/outline.md` | 三幕/八序列章节大纲，每章含核心事件 + 悬念 |
| 1.5 | `foundation/voice.md` | 叙事人称、语言调色盘、节奏标记、禁忌清单 |
| 1.6 | `foundation/canon.md` | 不可违背的事实、设定一致性规则、时间线锚点 |
| 1.7 | `foundation/scores.md` | 评分门控（≥ 7.5 通过，否则退回修改，最多 3 轮） |

**评分维度：** 世界观一致性(20%)、角色深度(25%)、大纲可行性(20%)、声音独特性(15%)、灵感潜力(20%)

### Phase 2：初稿（First Draft）

**目标：** 逐章撰写初稿，每章质量门控。

- 每章独立文件 `chapters/ch_01.md`、`chapters/ch_02.md`……
- 每章自评 ≥ 6.0 才保留，否则重写（最多 3 次）
- 每 3 章一次一致性检查（更新 canon.md）
- 每完成 25% 输出阶段性报告

### Phase 3：修改循环（Revision）

**分为两个子阶段：**

#### Phase 3a：自动化修改

| 步骤 | 内容 | 产出 |
|------|------|------|
| 对抗式编辑 | AI 味检测 + 结构套路 + 冗余 + 过度解释 + 情节漏洞 | `revision/editorial-notes.md` |
| 读者小组评审 | 4 个 agent 并行扮演：文学评论家、普通读者、类型爱好者、编辑 | `revision/reader-reviews.md` |
| 生成修改简报 | 按优先级整理修改项 | `revision/revision-brief.md` |
| 逐条重写 | 按简报修改章节文件 | 更新章节 |

#### Phase 3b：深度审阅循环

- 合并完整手稿 → 双人格（文学评论家 + 写作教授）深度审阅
- 逐条修复 → 重新合并 → 再次审阅
- 当「无明显缺陷」条目 ≥ 90% 时退出循环

### Phase 4：导出（Export）

- 合并最终手稿 → `manuscript.md`
- 输出统计报告 → `manuscript-stats.md`
- 可选：导出 epub、生成封面文案、角色关系图谱

---

## 📂 完整文件结构

```
~/novels/<小说名称>/
├── foundation/
│   ├── world.md              # 世界设定
│   ├── characters.md         # 角色档案
│   ├── outline.md            # 章节大纲
│   ├── voice.md              # 叙事声音
│   ├── canon.md              # 硬设数据库
│   └── scores.md             # 地基评分记录
├── chapters/
│   ├── ch_01.md              # 第1章
│   ├── ch_02.md              # 第2章
│   ├── ...
│   └── ch_NN.md              # 第N章
├── revision/
│   ├── editorial-notes.md    # 对抗式编辑记录
│   ├── reader-reviews.md     # 读者评审记录
│   ├── revision-brief.md     # 修改简报
│   ├── deep-review.md        # 深度审阅记录
│   └── fix-log.md            # 修复日志
├── manuscript.md             # 最终合并手稿
├── manuscript-stats.md       # 手稿统计报告
└── state.json                # 写作进度状态
```

---

## ⚠️ 常见陷阱

| # | 陷阱 | 后果 | 解决 |
|---|------|------|------|
| 1 | 地基不够就开写 | 写到一半发现设定矛盾/角色平庸 | 严格执行评分门控 ≥ 7.5 |
| 2 | 评分走过场 | 低质章节累积到后期修复成本高 | 自评时诚实地问「读到这章会觉得被坑了吗？」 |
| 3 | 过度修改 | 作品失去生气，或永远完不成 | 设定退出条件：无明显缺陷 ≥ 90% |
| 4 | 忽视向上反馈 | 设定矛盾越积越多 | 每3章强制执行一致性检查 |
| 5 | 声音漂移 | 第一章和最后一章像两个人写的 | 写每章前重读 voice.md |
| 6 | 章节太长或太短 | 节奏失控 | 目标字数范围 1500-3000 字/章 |
| 7 | 角色行为不一致 | 角色失真，读者失去代入感 | 写前重读对应角色档案 |

---

## ❓ FAQ

**Q：我需要准备 API Key 吗？**
A：不需要。本技能完全基于 Hermes Agent 自身的文件操作、子任务分发和文本生成能力，无需任何额外的 API Key。

**Q：最多能写多长的小说？**
A：取决于 Hermes Agent 的 context window 大小。建议 32K+ tokens 用于中篇（10-15章），128K+ 用于长篇（20章以上）。

**Q：可以中途手动修改吗？**
A：可以！所有文件都是标准 markdown，你可以随时手动编辑任何文件。修改后继续运行工作流即可。

**Q：写了一半想换大纲怎么办？**
A：修改 `foundation/outline.md`，然后重新启动 Phase 2。注意 canon.md 中的设定需要同步更新。

**Q：可以导出为 epub 格式吗？**
A：Phase 4 提供可选扩展，需要系统安装 `pandoc` 或 `calibre` 命令行工具。

**Q：AI 味很重怎么办？**
A：本技能自带了 `references/anti-slop.md`（词汇/句式/结构级 AI 味检测清单）和 `references/anti-patterns.md`（叙事结构反模式检测），在 Phase 3a 的对抗式编辑中会使用它们。你也可以单独加载 `humanizer` 技能作为补充。

**Q：怎么配合其他技能用？**
A：建议搭配 `writing-plans` 技能进行写作前的详细规划，用 `humanizer` 技能增强文本的自然感。

---

## 📄 文件信息

| 项目 | 说明 |
|------|------|
| 版本 | 1.0.0 |
| 作者 | Hermes Agent |
| 协议 | MIT |
| 分类 | creative（创意写作） |
| 标签 | novel, writing, fiction, worldbuilding, character-design, outline, revision, editing |

---

*由 autonovel-workflow 自动生成*
