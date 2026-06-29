#!/usr/bin/env python3
"""
style-fingerprint.py — InkOS-style quantitative style analysis for novels.

Extracts style fingerprint from chapter files:
  - Sentence length distribution (句长分布)
  - Paragraph density (段落密度)
  - Dialogue ratio (对话占比)
  - High-frequency characters (高频字)
  - Vocabulary red flags (违禁词检测)

Usage:
  python3 style-fingerprint.py --dir <chapters-dir>
  python3 style-fingerprint.py --dir ~/novels/my-novel/chapters/ --prefix ch_

Output: Markdown-formatted style report, ready to paste into foundation/voice.md

Reference: InkOS `inkos style analyze` — this script provides equivalent
quantitative data without requiring InkOS to be installed.
"""

import os, re, sys, argparse
from collections import Counter
from pathlib import Path

# ── Common AI-ism / forbidden vocabulary markers ──
AI_ISMS = [
    "然而", "但是", "却", "仿佛", "似乎", "好像", "不禁",
    "不由得", "忍不住", "突然", "忽然", "猛地", "骤然",
    "注视", "凝视", "默默", "缓缓", "轻轻", "微微",
    "某种", "某种程度", "某种意义",
]

def safe_div(a, b):
    return a / b if b else 0

def extract_sentences(text):
    """Split Chinese text into sentences."""
    raw = re.split(r'[。！？…\n]+', text)
    return [s.strip() for s in raw if len(s.strip()) > 5]

def count_chinese_chars(text):
    return len(re.sub(r'[\sA-Za-z0-9，。！？、；：""''「」（）《》—…·\-\n]', '', text))

def extract_dialogues(text):
    """Extract 「」 dialogues."""
    return re.findall(r'「[^」]*」', text)

def analyze_chapter(filepath):
    with open(filepath, encoding='utf-8') as f:
        text = f.read()

    stats = {}

    # Paragraphs
    stats['paragraphs'] = len(re.findall(r'\n\n+', text)) + 1

    # Characters (Chinese only)
    stats['chars'] = count_chinese_chars(text)
    stats['total_chars'] = len(text)

    # Sentences
    sents = extract_sentences(text)
    stats['sentences'] = len(sents)
    sent_lengths = [count_chinese_chars(s) for s in sents]
    if sent_lengths:
        stats['avg_sent_len'] = round(sum(sent_lengths) / len(sent_lengths), 1)
        sorted_lens = sorted(sent_lengths)
        n = len(sorted_lens)
        stats['median_sent_len'] = round(
            sorted_lens[n//2] if n % 2
            else (sorted_lens[n//2 - 1] + sorted_lens[n//2]) / 2,
            1
        )
    else:
        stats['avg_sent_len'] = 0
        stats['median_sent_len'] = 0

    # Dialogues
    dials = extract_dialogues(text)
    stats['dialogues'] = len(dials)
    dial_chars = sum(count_chinese_chars(d) for d in dials)
    stats['dial_pct'] = round(safe_div(dial_chars, stats['chars']) * 100, 1)
    dial_lengths = [count_chinese_chars(d) for d in dials]
    stats['avg_dial_len'] = round(safe_div(sum(dial_lengths), len(dial_lengths)), 1) if dial_lengths else 0

    # AI-ism frequency
    stats['ai_isms'] = {}
    for word in AI_ISMS:
        count = text.count(word)
        if count > 0:
            stats['ai_isms'][word] = count

    # Word frequency (single char)
    chars_only = re.sub(r'[\sA-Za-z0-9，。！？、；：""''「」（）《》—…·\-\n]', '', text)
    stats['char_freq'] = Counter(chars_only).most_common(30)

    return stats, sent_lengths

def main():
    parser = argparse.ArgumentParser(description='Extract InkOS-style style fingerprint from novel chapters')
    parser.add_argument('--dir', required=True, help='Directory containing chapter files')
    parser.add_argument('--prefix', default='ch_', help='Chapter filename prefix (default: ch_)')
    args = parser.parse_args()

    chap_dir = Path(args.dir)
    if not chap_dir.is_dir():
        print(f"Error: {chap_dir} is not a directory")
        sys.exit(1)

    files = sorted(chap_dir.glob(f"{args.prefix}*.md"))
    if not files:
        files = sorted(chap_dir.glob(f"{args.prefix}*.txt"))
    if not files:
        print(f"Error: no files matching '{args.prefix}*.md' or '{args.prefix}*.txt' in {chap_dir}")
        sys.exit(1)

    print(f"Analyzing {len(files)} chapter files from {chap_dir}\n")

    all_chapter_stats = []
    all_sent_lengths = []

    for fp in files:
        stats, sent_lens = analyze_chapter(str(fp))
        all_chapter_stats.append(stats)
        all_sent_lengths.extend(sent_lens)
        print(f"  {fp.name:30s} {stats['chars']:6d}字  {stats['sentences']:4d}句  "
              f"均{stats['avg_sent_len']:5.1f}字  中位{stats['median_sent_len']:4.1f}  对话{stats['dial_pct']:5.1f}%")

    # ── Aggregated report ──
    total_chars = sum(s['chars'] for s in all_chapter_stats)
    total_sents = sum(s['sentences'] for s in all_chapter_stats)
    total_dial_chars = sum(s['dial_pct'] * s['chars'] / 100 for s in all_chapter_stats)

    avg_sent = round(sum(s['avg_sent_len'] * s['sentences'] for s in all_chapter_stats) / total_sents, 1) if total_sents else 0
    avg_dial_pct = round(safe_div(total_dial_chars, total_chars) * 100 / len(all_chapter_stats), 1)

    # Sentence length distribution bins
    bins = {"1-5字": 0, "6-15字": 0, "16-30字": 0, "31-50字": 0, "51-80字": 0, "80+字": 0}
    for sl in all_sent_lengths:
        if sl <= 5: bins["1-5字"] += 1
        elif sl <= 15: bins["6-15字"] += 1
        elif sl <= 30: bins["16-30字"] += 1
        elif sl <= 50: bins["31-50字"] += 1
        elif sl <= 80: bins["51-80字"] += 1
        else: bins["80+字"] += 1

    total_binned = sum(bins.values())
    bin_pcts = {k: f"{v/total_binned*100:.1f}%" if total_binned else "N/A" for k, v in bins.items()}

    # Top char frequencies (aggregated)
    all_chars_text = ""
    for s in all_chapter_stats:
        for char, count in s['char_freq']:
            all_chars_text += char * count
    top30 = Counter(all_chars_text).most_common(30)

    # AI-ism aggregate
    all_ai_isms = Counter()
    for s in all_chapter_stats:
        for word, count in s['ai_isms'].items():
            all_ai_isms[word] += count

    # ── Output ──
    print(f"\n{'='*60}")
    print(f"风格指纹分析报告")
    print(f"{'='*60}")

    print(f"\n## 1.1 句长分布")
    print(f"\n| 指标 | 数值 |")
    print(f"|:----|:-----|")
    print(f"| **样本章节数** | {len(all_chapter_stats)} |")
    print(f"| **总字数** | {total_chars} |")
    print(f"| **总句子数** | {total_sents} |")
    print(f"| **平均句长** | **{avg_sent} 字** |")
    print(f"| 中位句长 | 见各章统计 |")
    print(f"\n| 区间 | 句数 | 占比 |")
    print(f"|:----|:----:|:----:|")
    for k in ["6-15字", "16-30字", "31-50字", "51-80字", "80+字", "1-5字"]:
        if k in bins:
            print(f"| {k} | {bins[k]} | {bin_pcts[k]} |")

    print(f"\n## 1.2 段落密度")
    paras_total = sum(s['paragraphs'] for s in all_chapter_stats)
    print(f"| 指标 | 数值 |")
    print(f"|:----|:-----|")
    print(f"| 平均每章段落数 | {round(safe_div(paras_total, len(all_chapter_stats)), 1)} |")
    print(f"| 平均每段字数 | {round(safe_div(total_chars, paras_total))} |")

    print(f"\n## 1.3 对话占比")
    avg_dial = round(sum(s['dialogues'] for s in all_chapter_stats) / len(all_chapter_stats), 1)
    print(f"| 指标 | 数值 |")
    print(f"|:----|:-----|")
    print(f"| 平均每章对话条数 | {avg_dial} |")
    print(f"| 对话占总字数（估算） | {avg_dial_pct}% |")
    avg_dial_len = round(sum(s['avg_dial_len'] for s in all_chapter_stats if s['dialogues'] > 0) / max(1, sum(1 for s in all_chapter_stats if s['dialogues'] > 0)), 1)
    print(f"| 平均对话长度 | {avg_dial_len} 字 |")

    print(f"\n## 1.4 高频字指纹（TOP30）")
    print(f"\n`{'、'.join(f'「{c}」' for c, _ in top30[:10])}`")
    print(f"\n全部 TOP30:")
    for i, (char, count) in enumerate(top30[:30], 1):
        print(f"  {i:2d}. `{char}` × {count}")

    if all_ai_isms:
        print(f"\n## ⚠️ AI-ism 检测（违禁词频次）")
        print(f"\n| 违禁词 | 出现次数 |")
        print(f"|:-------|:--------:|")
        for word, count in all_ai_isms.most_common():
            print(f"| `{word}` | {count} |")
        print(f"\n> 将这些词加入 voice.md 的「禁忌清单」进行严格控制。")

    print(f"\n{'='*60}")
    print(f"提示: 将上方数据填入 foundation/voice.md 的「量化风格指纹」部分。")
    print(f"如不确定目标值，保持脚本输出的实际值即可。")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
