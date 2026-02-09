import streamlit as st

# =========================
# 設定
# =========================

DELEGATION_WORDS = ["任せ", "決めて", "どちらでも", "お好きに"]
EMOTION_WORDS = ["別に", "まあ", "全然", "大丈夫"]
IMPLICIT_WORDS = ["そう", "らしい", "みたい"]

# =========================
# stage 推論
# =========================

def stage1_basic_context(text):
    return "発話内容は通常の叙述文として成立している"

def stage2_clarification_need(text):
    if any(w in text for w in EMOTION_WORDS):
        return "感情的含みを示す語彙が含まれているため、聞き返し余地あり"
    return "明示的な聞き返しは不要"

def stage3_causality(text):
    if "から" in text or "ので" in text:
        return "因果関係を示す接続が含まれている"
    return "明示的な因果関係は検出されない"

def stage4_modifier(text):
    if any(w in text for w in IMPLICIT_WORDS):
        return "推測・含意を示す修飾表現が含まれている"
    return "修飾構造は単純"

def stage5_case_relation(text):
    if any(w in text for w in DELEGATION_WORDS):
        return "判断主体が相手に委ねられている"
    return "判断主体は話者側にある"

# =========================
# 文脈タイプ分類
# =========================

def classify_context(text):
    b_score = 0
    c_score = 0
    reasons = []

    if any(w in text for w in EMOTION_WORDS):
        b_score += 1
        reasons.append("感情・含みを示す語彙が検出された")

    if any(w in text for w in IMPLICIT_WORDS):
        b_score += 1
        reasons.append("推測・含意表現が検出された")

    if any(w in text for w in DELEGATION_WORDS):
        c_score += 2
        reasons.append("判断委譲を示す語彙が検出された")

    if c_score >= 2:
        return "C：判断委ね型", reasons

    if b_score >= 2:
        return "B：感情・含み型", reasons

    return "A：日常的すれ違い型", reasons

# =========================
# UI
# =========================

st.title("文脈推論デモ（説明可能AI）")

st.markdown("""
このデモでは、入力された日本語文を  
段階的な文脈推論（stage1〜5）に基づいて解析し、  
文脈タイプ（A・B・C）への**推論可能性**を評価します。

※ 統計モデル・LLMは使用していません。
""")

user_input = st.text_input("発話文を入力してください")

if user_input:
    st.subheader("推論ステージ")

    s1 = stage1_basic_context(user_input)
    s2 = stage2_clarification_need(user_input)
    s3 = stage3_causality(user_input)
    s4 = stage4_modifier(user_input)
    s5 = stage5_case_relation(user_input)

    st.write("stage1：", s1)
    st.write("stage2：", s2)
    st.write("stage3：", s3)
    st.write("stage4：", s4)
    st.write("stage5：", s5)

    context_type, reasons = classify_context(user_input)

    st.markdown("---")
    st.subheader("分類結果")

    st.write(f"**文脈タイプ：{context_type}**")

    if reasons:
        st.markdown("**推論根拠（語彙ベース）**")
        for r in reasons:
            st.write("・", r)

    st.caption(
        "※ 本結果は入力文単体に基づく推論可能性を示すものです。"
        "前後の文脈や関係性が与えられた場合、"
        "他の文脈タイプとして解釈される可能性があります。"
    )