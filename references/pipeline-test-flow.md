# plan→compose→draft 管线验收测试流程

> 记录日期：2026-07-07
> 对应技能版本：v1.14.0
> 测试项目：末日降临_末世游戏 @ `/vol1/1000/data/ai文案/novels/末日降临_末世游戏/`

## 测试目标

验证新输入治理控制面管线（plan→compose→draft）在真实项目上的完整可执行性：
1. Plan 正确读取 foundation 并生成 intent.md
2. Compose 正确读取 intent + foundation 并输出三件套
3. Draft 只读 compose 产物，不碰 foundation
4. 字数治理检查正确执行
5. 语音/风格规则自动生效

## 测试步骤

### Step 0：项目准备
```bash
mkdir -p {foundation,chapters,runtime,revision,prompt,materials}
```

### Step 1：Plan（规划师意图声明）
- 输入：foundation/*.md + outline.md + state.json
- 输出：runtime/ch_NN/intent.md
- 检查点：
  - □ 包含「本章目标」「must keep」「must avoid」「可能冲突」
  - □ must-avoid 引用 canon.md 中的硬设规则
  - □ 字数目标与 outline 一致

### Step 2：Compose（编排师上下文编译）
- 输入：runtime/ch_NN/intent.md + foundation/*.md
- 输出三件套：context.md + rule-stack.yaml + trace.json
- 检查点：
  - □ context.md 包含「本章意图概要」区块（来自 intent.md）
  - □ context.md 不重复 foundation 全量内容
  - □ rule-stack.yaml 有 10+ 条规则，优先级 1-5 覆盖
  - □ trace.json 记录每个 source 文件的 extracted 内容
  - □ 写手只读 compose 产物即可完成写作

### Step 3：Draft（写手撰写）
- 输入：只读 context.md + intent.md（不读 foundation）
- 输出：chapters/ch_NN.md
- 字数治理检查：

| 偏差 | 处理 |
|:-----|:-----|
| < 50% target | 🔴 暂不保存，补写到 ≥ 60% |
| 50-70% | 🟡 short，保存，Phase 3 扩张 |
| 70-130% | 🟢 合格 |
| > 130% | 🟡 overshoot，Phase 3 压缩 |

### Step 4：验证脚本

```python
import re

path = 'chapters/ch_NN.md'
with open(path) as f:
    c = f.read()

zh = len(re.findall(r'[\u4e00-\u9fff\uf900-\ufaff]', c))

# 禁用词扫描
forbidden = ['突然','好像','忍不住','猛地','然而','但是','却','仿佛','宛如','与此同时']
hits = {w: c.count(w) for w in forbidden if c.count(w) > 0}

# 情绪词扫描
emotions = ['愤怒','悲伤','恐惧','害怕']
em_hits = {w: c.count(w) for w in emotions if c.count(w) > 0}

# 旧版遗骸扫描
legacy = ['极速光纹','注射式','深渊科技']
legacy_hits = {w: c.count(w) for w in legacy if c.count(w) > 0}

# 「看着」统计
kanzhe = c.count('看着')

print(f"字数: {zh} | {'🟢' if 0.7*TARGET <= zh <= 1.3*TARGET else '⚠️'}")
print(f"禁用词: {hits if hits else '✅ 零'}")
print(f"情绪词: {em_hits if em_hits else '✅ 零'}")
print(f"旧版遗骸: {legacy_hits if legacy_hits else '✅ 零'}")
print(f"「看着」: {kanzhe}处 {'✅' if kanzhe <= 5 else '⚠️'}")
```

## 会话特定信息

- 测试项目路径：`/vol1/1000/data/ai文案/novels/末日降临_末世游戏/`
- 文件属主：生成后需 `chown -R gemmt:Users <path>`
- 目标模型：deepseek-v4-flash（当前会话模型）
- 已知 issue：patch 替换「突然」时需要前后各1行上下文防止误替换相邻对话
