# InkOS v1.6.x 融合评估与路线图

> 评估日期：2026-07-07
> 评估范围：InkOS v1.5.0 → v1.6.0 → v1.6.1 → v1.6.2
> 当前完成：Phase 1（输入治理控制面）✅ + Phase 2（可编辑提示词包）✅ + Phase 3（材料归档检索）✅ + 短篇模式 ✅
> 对应技能版本：v1.15.0
> 参考：`https://github.com/Narcooo/inkos/releases`

---

## 一、已对齐功能（融合完成）

| InkOS 组件 | autonovel 位置 | 融合版本 |
|:-----------|:--------------|:--------:|
| 审计员 Auditor (37维) | Step 3a.1 | v1.3 |
| 写手 Writer + 风格指纹 | Step 1.5 + `scripts/style-fingerprint.py` | v1.4 |
| 字数治理 | Step 2.2 + Step 3b.2b | v1.4 |
| 雷达 Radar | Step 1.0 | v1.5 |
| 编排师 Composer | Step 2.1b | v1.6 |
| 观察者 Observer (7→9类) | Step 2.2b | v1.7→v1.10 |
| 伏笔追踪 Pending Hooks | canon.md V21 | v1.3 |
| 输入治理控制面 | Step 2.1b plan→compose→draft | v1.12 |
| 可编辑提示词包 | Step 2.1c prompt/ 目录 + 三层加载 | v1.13 |
| 材料归档与证据检索 | Step 2.1d materials/ + Compose联动 | v1.14 |
| **短篇模式 Short Run** | **短篇模式章节（S0→S4）** | **v1.15** |

---

## 二、已评估但暂缓融合

| 项 | InkOS 版 | 暂缓原因 |
|:--|:---------|:---------|
| Reflector JSON delta 模式 | v1.5.0+ | Hermes Agent 工具层无法处理 Zod schema 校验 + immutable apply |
| 互动影游 | v1.6.0 | 偏离小说创作核心，适合独立模块 |
| 守护进程 + 通知推送 | v1.5.0+ | Hermes cronjob 已有等效能力 |
| 同人创作系统 | v1.5.0+ | niche 需求，暂无用户场景驱动 |
| 多模型路由 | v1.5.0+ | 可通过 Hermes system profile 间接实现 |

---

## 三、实战教训（本版本评估积累）

### 用户纠正：短篇属于小说创作范畴
- **表现：** 首次评估时把短篇模式列为 🟢（非核心），用户纠正为「短篇生成也属于写小说范畴」
- **教训：** 独立短篇和长篇连载都是小说创作工作流的一部分。短篇的发布场景（简介卖点 + 封面提示词）是增值产出，不应被完整长篇管线的高 overhead 阻塞。
- **修复：** v1.15.0 新增短篇模式章节，轻量版管线 5-10 分钟跑完全流程。

### GitHub 内容提取受阻的处理
- **表现：** web_extract 和 curl 请求均失败。browser 页面过长被截断。
- **解决：** browser_navigate 加载慢但最终成功 → browser_console (document.querySelector('article.markdown-body')?.innerText) 提取完整 README。Releases 页面同理。
- **参见：** version-history.md 实战教训「GitHub 内容提取受阻」

---

## 四、InkOS 更新监控方法论

当需要评估 InkOS 新版本时：

1. **获取版本数据** — 访问 `https://github.com/Narcooo/inkos/releases` 获取 release notes
2. **横向对比** — 对照本文件的「已对齐」「待融合」「暂缓」三表
3. **搜索关联** — 用 `web_search` + "inkos <feature>" 搜索社区讨论和文档
4. **优先级判定** — 按「核心写作价值 > 易融合性 > 用户场景」排序
5. **评估输出** — 格式：分析报告 → 对比表 → 融合方案（按优先级排）→ 工作量预估
