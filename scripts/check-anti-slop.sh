#!/usr/bin/env bash
# check-anti-slop.sh — Run all anti-slop grep checks on a chapter file
#
# Usage: bash scripts/check-anti-slop.sh chapters/ch_NN.md
#
# Scans for the vocabulary-level and phrase-level patterns documented in
# references/anti-slop.md: AI-preferential words, tell-words, forbidden
# phrases, and show-don't-tell violations.
#
# Output: one section per check, with line numbers for matches.
# Exit code: 0 = clean (no hits), 1 = at least one hit found.

FILE="$1"
if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
  echo "Usage: $0 <chapter-file>"
  echo "Example: $0 chapters/ch_03.md"
  exit 2
fi

HITS=0
section() {
  echo ""
  echo "=== $1 ==="
}

check() {
  local label="$1"
  local pattern="$2"
  local result
  result="$(grep -n "$pattern" "$FILE")"
  if [ -n "$result" ]; then
    echo "$label — MATCHES:"
    echo "$result"
    HITS=$((HITS + 1))
  else
    echo "$label — clean"
  fi
}

echo "========================================"
echo "  ANTI-SLOP CHECK: $(basename "$FILE")"
echo "========================================"

# Yellow-warning words (Section 1.1)
section "1.1 黄色警告词"
check "不禁让人思考/感叹" "不禁让人(思考|感叹)"
check "以…的方式" "以[^，。]{1,20}的方式"
check "似乎/仿佛/好像/或许" "似乎|仿佛|好像|或许"
check "一般/一样/似的（非必要）" "(如释重负|死|坠入|跌入).*一般[^人]"
check "就这样（过渡词）" "[，。]就这样"

# Red-zone forbidden phrases (Section 1.2)
section "1.2 红色禁区词"
check "在这个充满变数的时代" "在这个充满变数的时代"
check "不禁让人(深思|反思)" "不禁让人(深思|反思)"
check "命运(似乎|仿佛)在开玩笑" "命运(似乎|仿佛)在开"
check "也许这就是人生吧" "也许这就是人生"
check "时间仿佛在这一刻静止" "时间仿佛在这一刻静止"
check "空气中弥漫" "空气中弥漫"

# Show-Don't-Tell (Section 2.1)
section "2.1 Show-Don't-Tell — Tell 词"
check "感到" "感到"
check "觉得" "(不)?觉得"
check "看起来" "看起来[^不]"
check "似乎显得" "似乎显得"
check "充满了" "充满了"
check "弥漫着" "弥漫着"
check "发现自己是" "发现自己是"

# Sentence structure (Section 2.2)
section "2.2 句式 — 连续陈述句密度（参考）"
STMT_COUNT=$(grep -cP '^[^「」\\n]*是[^「」]*。' "$FILE" 2>/dev/null || echo 0)
echo "以「是」作谓语的陈述句数: $STMT_COUNT"

# 对话标签 (Section 2.3)
section "2.3 对话标签 — 多样化"
SAID_COUNT=$(grep -c '[。，：]''"[^"」]{1,50}"' "$FILE" 2>/dev/null || echo 0)
echo "引用式对话句数（参考）: $SAID_COUNT"

# Transition crutch words
section "1.3 过渡拐杖词"
check "突然" "突然"
check "忽然" "忽然"
check "骤然" "骤然"
check "就在这时" "就在这时"
check "就在这时" "就在这时"

# End
echo ""
echo "========================================"
if [ $HITS -eq 0 ]; then
  echo "  ✅ CLEAN — No anti-slop patterns detected."
else
  echo "  ⚠️  $HITS section(s) with hits. Review and fix before Phase 4."
fi
echo "========================================"
exit $HITS
