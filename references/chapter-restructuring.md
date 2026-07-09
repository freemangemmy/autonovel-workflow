# 章节重排流程（Chapter Restructuring）

> 当需要在已有章节序列中插入、删除或重排章节时使用。
> 适用场景：新增第1章前置故事、拆分超长章节、合并短章、剧情顺序调整。

## 核心原则

章节重排涉及到 **文件命名、内部标题、大纲体系、state.json** 四个层面的同步变更，缺一不可。

## 常见触发场景

| 场景 | 典型操作 |
|:-----|:---------|
| 新增前置第1章（前传/起源） | 所有现存章节编号 +1 |
| 删除某一章 | 后续所有章节编号 -1 |
| 拆分超长章节（如8000字→4000+4000） | 插入新文件，后续编号 +1 |
| 两章合并 | 删除一章，后续编号 -1 |
| 章节顺序对调 | 仅涉及两个文件 |

## 通用执行流程（以「新增第1章」为例）

### 步骤1：文件重命名

```bash
cd ~/novels/<项目名>/chapters/

# 从后往前复制，防止覆盖
cp ch_04.md ch_05.md
cp ch_04.txt ch_05.txt
cp ch_03.md ch_04.md
cp ch_03.txt ch_04.txt
cp ch_02.md ch_03.md
cp ch_02.txt ch_03.txt
cp ch_01.md ch_02.md
cp ch_01.txt ch_02.txt

# （可选）ch_01.md 现在存着旧内容，将被新内容覆盖
```

### 步骤2：更新内部标题

每个 .md 文件的第一行是章节标题，需要逐一更新：

```bash
# 用 sed 批量修复
sed -i 's/^# 第.*章/# 第二章 不速之客/' ch_02.md
sed -i 's/^# 第.*章/# 第三章 活阎王/' ch_03.md
# ...类推
```

> ⚠️ **sed 陷阱：** `^# 第.*章` 是贪婪匹配，如果在一条含有 `第X章` 的行上运行，可能匹配到比预期更多的内容。建议用 Python 或 `execute_code` 直接替换第一行更可靠：

```python
import os
pairings = [("ch_02.md", "第二章 不速之客"), ("ch_03.md", "第三章 活阎王"), ...]
base = "~/novels/<项目名>/chapters"
for fname, title in pairings:
    path = os.path.join(base, fname)
    with open(path) as f:
        lines = f.readlines()
    lines[0] = f"# {title}\n"
    with open(path, 'w') as f:
        f.writelines(lines)
```

同步更新同名 .txt 文件。

### 步骤3：更新 state.json

```json
{
  "total_chapters": N,           // 增加或减少
  "completed_chapters": [...],   // 调整编号列表
  "current_chapter": N,          // 调整
  "word_governance": {
    "per_chapter": {
      "ch_01": {"target": 7000, "actual": null, "ok": null},
      "ch_02": {"target": 5000, "actual": 5058, "ok": true},  // 原ch_01数据
      // ...类推
    }
  }
}
```

> ⚠️ 注意 `per_chapter` 的 key 和 `completed_chapters` 的数字都要同步更新。容易漏掉！

### 步骤4：更新大纲体系

三个文件需要同步：

1. **foundation/outline.md** — 更新章节概览和分章大纲的编号
2. **大纲_书名.txt** — 同样更新章节编号和描述
3. **小纲_第X章_标题.txt** — 每个小纲文件需要：
   - 文件名改为新的编号
   - 文件内的章节编号描述（如「第1章」→「第2章」）

```bash
# 小纲文件重命名
mv "小纲_第1章_旧标题.txt" "小纲_第2章_旧标题.txt"

# 更新文件内引用
sed -i 's/第1章/第2章/g' "小纲_第2章_旧标题.txt"
```

### 步骤5：更新 foundation 中的章节引用

- **outline.md** — 更新 `- 第1章「标题」` 行
- **world.md** — 检查时间线和事件列表中是否有章节引用
- **canon.md** — 检查「当前章节已建立的事实」表中是否有章节号引用

### 步骤6：综合验证

```python
import os, re, json

base = "~/novels/<项目名>"

# 1. 验证所有章节文件标题
chapters_dir = f"{base}/chapters"
for f in sorted(os.listdir(chapters_dir)):
    if f.endswith('.md'):
        with open(f"{chapters_dir}/{f}") as fp:
            first_line = fp.readline().strip()
        print(f"{f}: {first_line}")

# 2. 验证 state.json 章节数与实际文件数一致
with open(f"{base}/state.json") as fp:
    state = json.load(fp)
ch_count = len([f for f in os.listdir(chapters_dir) if f.endswith('.md')
                and re.match(r'^ch_\d{2}\.md$', f)])
print(f"state.json total_chapters: {state['total_chapters']}, 实际文件数: {ch_count}")
assert state['total_chapters'] == ch_count, "章节数不匹配！"

# 3. grep 检查是否还有旧编号残留
# (如果是从ch_01→ch_02的重排，检查旧大纲文件引用)
```

## 注意事项 / 常见坑

| 坑 | 现象 | 解决 |
|:---|:-----|:-----|
| 文件复制顺序反了 | 先复制 ch_01→ch_02 导致 ch_01 被覆盖丢失 | **从后往前**复制（ch_N→ch_N+1） |
| sed 标题替换产生重复 | `# 第二章 不速之客 不速之客` | 用 Python 直接替换 lines[0] |
| 小纲文件名忘了改 | 旧编号仍在用，新写时找不到 | 重命名后 grep 验证 |
| ch_02.txt 没同步 | txt 和 md 内容不一致 | 每次修改 md 后 cp 到 txt |
| state.json per_chapter 的 key 没更新 | 字数治理引用错误的键 | 逐一检查所有 ch_NN 编号 |
| canon.md 的「当前章节已建立的事实」表 | 事实和章节号映射错误 | 手动核对或忽略（该表是描述性而非功能性） |

## 替代方案：不重排文件编号

如果只是**内部故事时间线**调整（如章节顺序对调），但不想改变文件名，可以在 outline.md 中标注 `ch_01 对应第2章` 的映射关系。但这种方案的缺点是文件名与内容脱节，长期维护容易混淆。

**建议：** 只要不超过 3 个文件，就重排编号。超过 3 个文件时再考虑映射方案。
