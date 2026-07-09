# autonovel-workflow 版本沿革与 InkOS 融合路径

> 本文件记录技能从初始创建至今的完整演进历史，包括版本变更、InkOS 组件融合时间点、以及开发中
> 积累的实战教训。

---

## 一、版本演进时间线

```
v1.0.0 ──→ 初始创建
              参考 NousResearch/autonovel 五层协同架构
              基础 Phase 1-4 流水线（Foundation→Draft→Revision→Export）
              评分门控（foundation_score ≥ 7.5）

v1.3.0 ──→ 🔴 InkOS Auditor 融合（第一轮融合）
              37 维度对抗式审计框架（V1-V37）
              伏笔追踪表（pending_hooks）：🟢/🟡/🔴/⚪ 四态
              输出五层分级：🔴硬伤 → 🟡角色 → 🟢结构 → 📌套路 → 🔍小问题

v1.4.0 ──→ 🖊️ InkOS Writer 融合
              voice.md 量化风格指纹（句长分布/段落密度/对话占比/高频字/禁忌词）
              字数治理体系（保守写原则 + 5 级偏差处理 + --words N 覆盖）
              scripts/style-fingerprint.py 文风量化脚本

v1.5.0 ──→ 📡 InkOS Radar 融合
              Step 1.0 雷达市场调研（web_search + 竞争分析）
              references/radar-report-template.md 报告模板

v1.6.0 ──→ 📦 InkOS Composer 融合
              Step 2.1b 上下文编译流程（纯文件读取，不依赖 LLM）
              templates/context-pack.md（~1000 字精简上下文包）
              canon_stale 缓存失效标记（foundation 变动时自动标记）

v1.7.0 ──→ 🔍 InkOS Observer 融合
              Step 2.2b 7 类事实提取（新角色/时间/地点/财物/系统/关系/伏笔）
              templates/character-registry.md 角色出场登记表
              伏笔自动检测：每写完一章即扫描新埋伏笔

v1.8.x ──→ 原创功能爆发期（InkOS 无等价物）
              角色自动改名提议（Step 1.3a）
              年代特征审查（references/period-name-review.md）
              剧情修改确认（Step 3b.0 clarify 三选项确认）
              连续执行模式（发现新问题不打断，统一汇报）

v1.9.x ──→ 批量委托策略落地
              delegate_task 并行写作（每片 ≤10 章）
              后处理验证脚本（禁用词/加粗/字数/句式）
              session resume 健康检查流程
              33→37 维度修正（见下方实战教训）
              并行审计策略（3 worker 分组审计 37 维度）
              实战案例参考（references/adversarial-review-case-study.md）
              批量委托基准数据（references/batch-delegation-benchmark.md）

v1.10.x ──→ 实战沉淀期
              字数治理修复流程（Step 3b.2b，深改前治理）
              章节重排参考（references/chapter-restructuring.md）
              声台形表角色驱动写作法（references/shengtai-table.md）
              单章快速修改参考（references/single-chapter-revision-patterns.md）
              Observer 从 7→9 类事实扩展（新增情感/物理状态）

v1.12.0 ──→ 🧠 InkOS Input Governance 融合（2026-07-07）
              评估覆盖 InkOS v1.5.0→v1.6.2 全版本
              输入治理控制面：plan→compose 三层管线
              intent.md：规划师意图声明（可编辑，compose 自动读新版）
              rule-stack.yaml：规则优先级链（1=章节级→5=通用级）
              trace.json：输入编译轨迹（每个信息的来源和选入理由）
              templates/chapter-intent.md 新模板
              templates/context-pack.md 更新（意图概要 + 声台形表）
              state.json 新增 input_governance 字段
              旧项目向后兼容：legacy mode 自动检测

v1.13.0 ──→ 📝 InkOS Editable Prompt Packs 融合
              Step 2.1c 可编辑提示词包：prompt/ 目录 + 三层叠加载
              5 个 agent 提示词文件定义（writer/planner/composer/auditor/reviser）
              编辑原则（不覆盖核心逻辑 + diff 可追踪 + 删除回退）

v1.14.0 ──→ 📁 InkOS Material Archive & Evidence Trace 融合
              Step 2.1d 材料归档检索：materials/ 目录 + index.json
              Compose 检索联动（context.md 新增「相关材料参考」区块）
              trace.json 材料引用记录
              对抗式编辑中引用证据标记（mat-XX-XX）
              mkdir -p materials 初始化

v1.15.0 ──→ ⚡ InkOS Short Run 融合（短篇模式）
              轻量版独立管线：不跑完整 4-Phase
              快速地基：仅 characters.md + outline.md（无 world/voice/canon/评分门控）
              S2 批量撰写：一次 delegate_task 写完所有章节（不逐章 Plan→Compose）
              S3 轻量审阅：5 维度检查（情节/角色/文笔/悬念/完成度）
              S4 导出三件套：manuscript.md + sales-package.md + cover-prompt.md
              全程预估 5-10 分钟（vs 长篇管线 30-60 分钟）
              目录结构：~/novels/shorts/<短篇名>/
```

---

## 二、InkOS 融合清单

| InkOS 组件 | autonovel 位置 | 实现方式 | 融合版本 |
|:----------|:--------------|:---------|:--------:|
| **审计员 Auditor** | Step 3a.1 + `references/adversarial-review-framework.md` | 3 个 delegate_task worker 并行，各负责一组维度 | v1.3 |
| **写手 Writer** | Step 1.5 voice.md + `scripts/style-fingerprint.py` | 句长/段落/对话/高频字/禁忌词 五项量化指纹 | v1.4 |
| **字数治理** | Step 2.2.4 + Step 3b.2b + `references/word-governance.md` | 保守写原则 + 5 级偏差（<50%/50-70%/70-130%/130-200%/>200%） | v1.4 |
| **雷达 Radar** | Step 1.0 + `references/radar-report-template.md` | web_search + 竞争分析报告模板 | v1.5 |
| **编排师 Composer** | Step 2.1b + `templates/context-pack.md` | 纯文件读取，输出 ~1000 字上下文包，含缓存失效标记 | v1.6 |
| **观察者 Observer** | Step 2.2b + `templates/character-registry.md` | 7→9 类事实提取扩展 | v1.7 → v1.10 |
| **伏笔追踪** | canon.md pending_hooks + V21 回收率检测 | 🟢已回收/🟡待回收/🔴逾期未收/⚪艺术留白 四态 | v1.3 |
| **输入治理 Input Governance** | Step 2.1b + `templates/chapter-intent.md` | plan→compose 双层管线：intent.md + rule-stack.yaml + trace.json | v1.12 |

---

## 三、原创功能（InkOS 无等价物）

以下功能是 autonovel-workflow 基于 Hermes Agent 自身能力独创，InkOS 不提供：

| 功能 | 说明 |
|:----|:-----|
| **角色自动改名提议** Step 1.3a | AI 自我检测角色名是否套路化/撞名/时代错位，clarify 三选项确认 |
| **年代特征审查** | `references/period-name-review.md` 年代命名特征表，七零/八零/九零专项 |
| **剧情修改确认** Step 3b.0 | 改前展示计划清单 + clarify 三选项（全部/选择性/暂不） |
| **连续执行模式** | 修复中发现新问题不打断，记入 fix-log 新增发现区，修完统一汇报 |
| **批量委托策略** Step 2.2a | delegate_task 并行分发，每片 ≤10 章，含超时误判处理 |
| **后处理验证脚本** | 禁用词/加粗/字数/句式 四重验证，execute_code 自动化 |
| **Session Resume 健康检查** | 自动扫描文件系统 vs state.json，修复同步偏差 |
| **评分门控 foundation_score** | 5 维度加权（世界观20%/角色25%/大纲20%/声音15%/灵感20%），≥7.5 通过 |
| **读者小组评审** Step 3a.2 | 4 人格并行（文学评论家/普通读者/类型爱好者/编辑） |
| **双向传播原则** | 上层变→下层自动调；下层发现矛盾→更新上层 canon.md |

---

## 四、InkOS 方式 vs autonovel 方式对比

| InkOS | autonovel | 差异要点 |
|:------|:----------|:---------|
| `inkos style analyze` CLI 命令 | `scripts/style-fingerprint.py` | 不依赖外部 CLI，纯 Python |
| SQLite 记忆库 | `state.json` + foundation/*.md 文件系统 | 更透明，可手动编辑 |
| 独立 Agent 进程 | `delegate_task` 心智切换子任务 | 同进程内，无外部依赖 |
| 多模型路由 | `config.yaml` model 字段 | 更轻量，暂未做自动 fallback |

---

## 五、已知问题与实战教训

### 🐛 33→37 维度不匹配（2026-06-14）
- **表现：** SKILL.md 和 references 引用 InkOS 审计框架为「33 维度」
- **真相：** ClawHub 第三方 SKILL.md 缓存了旧版数据（33 维），InkOS 上游 README 已是 37 维
- **后果：** 用户纠正（内存中记录：「User caught 33→37 dimension error」）
- **修复：** SKILL.md 参考区增加实战教训警示，全量替换为 37 维度引用
- **教训：** 引用上游项目时，优先检查上游 README，而不是第三方平台缓存的 SKILL.md

### 🐛 delegate_task 超时误判（多次验证）
- **表现：** 分发 10+ 章写作时，子任务返回 `status: "timeout"`
- **真相：** 600s 限制在汇报阶段触发，**文件已安全写入磁盘**
- **修复方式：** 超时后用 `ls chapters/ch_*.md` 确认文件存在，不要重试
- **预防：** 每批 ≤10 章
- **记录位置：** SKILL.md 陷阱 9

### 🐛 state.json 与实际文件系统不同步
- **表现：** `word_governance.per_chapter` 中 `actual` 仍为 null
- **原因：** 多轮修改后忘记更新 state.json
- **修复：** session resume 时自动遍历统计，以文件系统为准
- **记录位置：** SKILL.md 陷阱 8

### 🐛 read_file 行号前缀写入损坏文件
- **表现：** 文件每行变成 `15|15|#### 第5章`（双重行号）
- **原因：** `execute_code` 的 `read_file` 返回带行号前缀的显示文本，直接传给 `write_file`
- **修复：** `sed -i 's/^[[:space:]]*[0-9]*|//' file.md` 剥离前缀
- **预防：** 勿将 read_file 显示输出直接传给 write_file
- **记录位置：** analyzebook SKILL.md（章节大纲维护 场景四）

### 🐛 GitHub 内容提取受阻（2026-07-07）
- **表现：** web_extract（ddgs）失败 + proxy 请求被阻止 + browser_navigate 超时
- **真相：** 网络代理/防火墙限制，纯 HTTP 和 API 请求不可达 GitHub
- **修复方式：** 先用 `web_search` 获取预览线索（star 数、描述），再用 `browser_navigate` 直接打开 GitHub 页面，然后用 `browser_console` + `document.querySelector('article.markdown-body')?.innerText` 提取完整 README 文本。在 releases 页面用同样方法获取更新日志。
- **教训：** 当 web_extract 和 curl 都不工作，browser_navigate + browser_console 是最后的可靠路径。先用 search 收集基本数据，再进浏览器获取全文。

---

## 六、目录结构

```
~/.hermes/skills/creative/autonovel-workflow/
├── SKILL.md                        # 主技能文档（v1.15.0）
├── references/
│   ├── version-history.md          ← 本文件
│   ├── adversarial-review-framework.md   # 37维度审计框架
│   ├── adversarial-review-case-study.md  # 42章年代文实战案例
│   ├── anti-patterns.md                  # 结构套路检测
│   ├── anti-slop.md                      # 文风反注水指南
│   ├── batch-delegation-benchmark.md     # 54章批量委托基准数据
│   ├── inkos-fusion-pattern.md           # InkOS 融合模式指南
│   ├── inkos-v1.6-fusion-roadmap.md      # v1.6.x 融合路线图（2026-07-07）
│   ├── radar-report-template.md          # 雷达报告模板
│   ├── style-cleanup-protocol.md         # 文风清理协议
│   └── word-governance.md                # 字数治理详细说明
├── templates/
│   ├── canon.md
│   ├── characters.md
│   ├── character-registry.md
│   ├── chapter-intent.md            # 规划师意图声明（v1.12 新增）
│   ├── context-pack.md
│   ├── outline.md
│   ├── voice.md
│   └── world.md
└── scripts/
    └── style-fingerprint.py
```
