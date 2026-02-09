import streamlit as st

# =========================
# 定義語彙（設計スコープ）
# =========================

DELEGATION_WORDS = ["任せ", "決めて", "どちらでも", "お好きに"]
EMOTION_WORDS = ["別に", "まあ", "全然", "大丈夫"]
IMPLICIT_WORDS = ["そう", "らしい", "みたい"]

ALL_KEYWORDS = DELEGATION_WORDS + EMOTION_WORDS + IMPLICIT_WORDS

# =========================
# stage 推論（抽象・簡潔）
# =========================

def stage1(text):
    return "発話は文として成立している"

def stage2(text):
    if any(w in text for w in EMOTION_WORDS):
        return "感情的含みを示す可能性あり"
    return "聞き返しを要する要素は少ない"

def stage3(text):
    if "から" in text or "ので" in text:
        return "因果関係が示唆されている"
    return "明示的な因果関係は検出されない"

def stage4(text):
    if any(w in text for w in IMPLICIT_WORDS):
        return "推測・含意を含む修飾がある"
    return "修飾構造は単純"

def stage5(text):
    if any(w in text for w in DELEGATION_WORDS):
        return "判断主体が相手に委ねられている"
    return "判断主体は話者側にある"

# =========================
# 分類ロジック
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

    return "A：日常的発話型", reasons

# =========================
# 定義範囲判定
# =========================

def is_out_of_scope(text):
    return not any(w in text for w in ALL_KEYWORDS)

# =========================
# UI
# =========================

st.title("文脈推論デモ（説明可能AI）")

st.markdown("""
本デモは、日本語対話における文脈解釈を  
**統計モデルやLLMを用いず**、  
段階的な論理推論によって扱う実証デモです。

分類結果は「正解」ではなく、  
**文脈タイプへの推論可能性**を示します。
""")

user_input = st.text_input("発話文を入力してください")

if user_input:
    st.subheader("推論ステージ（stage1〜5）")

    st.write("stage1：", stage1(user_input))
    st.write("stage2：", stage2(user_input))
    st.write("stage3：", stage3(user_input))
    st.write("stage4：", stage4(user_input))
    st.write("stage5：", stage5(user_input))

    context_type, reasons = classify_context(user_input)

    st.markdown("---")
    st.subheader("分類結果")

    st.write(f"**文脈タイプ：{context_type}**")

    if reasons:
        st.markdown("**推論根拠（語彙ベース）**")
        for r in reasons:
            st.write("・", r)

    # ===== 補足説明 =====
    if context_type.startswith("A"):
        if is_out_of_scope(user_input):
            st.markdown(
                "**補足**：本発話では、本デモで定義している"
                "文脈特徴語彙が検出されませんでした。"
                "そのため、推論対象となる文脈タイプは顕在化していません。"
            )
        else:
            st.markdown(
                "**補足**：文脈的特徴が弱いため、"
                "日常的な発話として解釈されています。"
            )

    st.caption(
        "※ 本結果は入力文単体に基づく推論可能性を示すものです。"
        "前後の文脈や関係性が与えられた場合、"
        "他の文脈タイプとして解釈される可能性があります。"
    )