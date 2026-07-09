#!/usr/bin/env python3
"""
verify-single-chapter.py — 单章后期验证脚本

在 Step 2.2 字数治理检查 + 门控判断之间运行。
按 intent.md 和 voice.md 中的规则检查一章的合规性。

用法:
  python3 verify-single-chapter.py <chapter_path> [--target N] [--forbidden WORD1 WORD2 ...]

输出 4 项检查结果 + 综合判定。
"""

import re
import sys
import json
import os

ZH_RE = re.compile(r'[\u4e00-\u9fff\uf900-\ufaff]')

# 默认禁用词（从 voice.md 常见规则提取）
DEFAULT_FORBIDDEN = ['忽然', '好像', '忍不住', '突然', '猛地', '然而', '但是', '却']

# 默认情绪词
EMOTION_WORDS = ['愤怒', '悲伤', '恐惧', '害怕']

# 默认 AI 味句式
AI_PATTERNS = ['不禁', '仿佛', '似乎', '或许', '默默', '微微', '轻轻']

# 默认旧版遗骸词（各项目不同，请在 --old-refs 覆盖）
DEFAULT_OLD_REFS = []


def count_zh(text: str) -> int:
    return len(ZH_RE.findall(text))


def check_forbidden(text: str, words: list) -> dict:
    return {w: text.count(w) for w in words if w in text}


def check_kanzhe(text: str) -> tuple:
    """返回 (总计, 分布)"""
    variants = {'看着': 0, '盯着': 0, '扫了': 0, '打量': 0, '注视': 0, '望向': 0}
    for v in variants:
        variants[v] = text.count(v)
    total = sum(variants.values())
    return total, variants


def check_emotions(text: str, words: list) -> dict:
    return {w: text.count(w) for w in words if w in text}


def check_old_refs(text: str, refs: list) -> dict:
    return {w: text.count(w) for w in refs if w in text}


def check_bolds(text: str) -> list:
    return [b for b in re.findall(r'\*\*[^*]+\*\*', text) if b != '**POV**']


def check_ai_phrases(text: str, patterns: list) -> dict:
    return {p: text.count(p) for p in patterns if p in text}


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Verify a single chapter against writing rules')
    parser.add_argument('chapter', help='Path to chapter file (e.g. chapters/ch_01.md)')
    parser.add_argument('--target', type=int, default=None, help='Target word count for governance check')
    parser.add_argument('--min-pct', type=int, default=50, help='Minimum acceptable % of target (default: 50)')
    parser.add_argument('--max-pct', type=int, default=130, help='Maximum acceptable % of target (default: 130)')
    parser.add_argument('--forbidden', nargs='*', default=DEFAULT_FORBIDDEN, help='Forbidden words to scan for')
    parser.add_argument('--old-refs', nargs='*', default=DEFAULT_OLD_REFS, help='Old-version reference words to detect')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    path = args.chapter
    if not os.path.exists(path):
        print(f"❌ File not found: {path}")
        sys.exit(1)

    with open(path) as f:
        content = f.read()

    # === Checks ===
    zh = count_zh(content)
    forbidden_hits = check_forbidden(content, args.forbidden)
    emotions = check_emotions(content, EMOTION_WORDS)
    ai_phrases = check_ai_phrases(content, AI_PATTERNS)
    kanzhe_total, kanzhe_dist = check_kanzhe(content)
    bolds = check_bolds(content)
    old_refs = check_old_refs(content, args.old_refs)

    # === Word governance ===
    governance_status = None
    if args.target:
        gov_pct = (zh / args.target) * 100
        if gov_pct < args.min_pct:
            governance_status = '🔴 severe_short'
        elif gov_pct < 70:
            governance_status = '🟡 short'
        elif gov_pct <= args.max_pct:
            governance_status = '🟢 ok'
        elif gov_pct <= 200:
            governance_status = '🟡 overshoot'
        else:
            governance_status = '🔴 severe_overshoot'
    else:
        gov_pct = None

    # === Results ===
    if args.json:
        result = {
            'chapter': path,
            'zh_chars': zh,
            'target': args.target,
            'gov_pct': round(gov_pct, 1) if gov_pct else None,
            'governance': governance_status,
            'forbidden': forbidden_hits,
            'emotions': emotions,
            'ai_phrases': ai_phrases,
            'kanzhe': {'total': kanzhe_total, 'distribution': kanzhe_dist},
            'bolds': len(bolds),
            'old_refs': old_refs,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0 if governance_status in ('🟢 ok', '🟡 short', '🟡 overshoot') else 1)

    # === Human-readable output ===
    print(f"{'='*50}")
    print(f"  验证报告：{path}")
    print(f"{'='*50}")

    # 1. Word count
    print(f"\n📏 字数治理")
    print(f"  中文字数: {zh}", end='')
    if args.target:
        print(f"  (目标 {args.target}, {gov_pct:.0f}%)", end='')
        print(f"  → {governance_status}")
    else:
        print()

    # 2. Forbidden words
    fw_pass = len(forbidden_hits) == 0
    print(f"\n🔍 禁用词扫描")
    print(f"  状态: {'✅ 零命中' if fw_pass else f'⚠️ {forbidden_hits}'}")

    # 3. Emotions
    em_pass = len(emotions) == 0
    print(f"\n💢 情绪词扫描")
    print(f"  状态: {'✅ 零使用' if em_pass else f'⚠️ {emotions}'}")

    # 4. AI phrases
    ai_pass = len(ai_phrases) == 0
    print(f"\n🤖 AI 味句式")
    print(f"  状态: {'✅ 零命中' if ai_pass else f'⚠️ {ai_phrases}'}")

    # 5. 看着
    kz_pass = kanzhe_total <= 5
    print(f"\n👁️  「看着」频率")
    print(f"  总计: {kanzhe_total}处  {'✅ ≤5' if kz_pass else '⚠️ >5'}")
    print(f"  分布: {kanzhe_dist}")

    # 6. Bold marks
    bd_pass = len(bolds) <= 1
    print(f"\n🖊️  加粗标记")
    print(f"  数量: {len(bolds)}处  {'✅ ≤1' if bd_pass else '⚠️ >1'}")
    if bolds:
        for b in bolds:
            print(f"    - {b}")

    # 7. Old version relics
    if args.old_refs:
        or_pass = len(old_refs) == 0
        print(f"\n📜 旧版遗骸")
        print(f"  状态: {'✅ 零残留' if or_pass else f'⚠️ {old_refs}'}")
    else:
        or_pass = True

    # === Summary ===
    all_pass = all([fw_pass, em_pass, ai_pass, kz_pass, bd_pass, or_pass])
    print(f"\n{'='*50}")
    print(f"  综合判定: {'✅ ALL PASS' if all_pass else '⚠️ 需修复（见上方 ⚠️ 项）'}")
    print(f"{'='*50}")
    sys.exit(0 if all_pass else 1)


if __name__ == '__main__':
    main()
