import streamlit as st

# =====================
# 基本設定
# =====================
st.set_page_config(page_title="文脈推定チャットデモ", layout="centered")
st.title("文脈推定チャット・デモ")
st.caption("統計モデル・LLMを用いない段階的文脈推定の簡易実証")

st.markdown("""
このデモでは、入力された日本語文を**stage1〜5の段階的文脈推定**に通し、  
文脈タイプ（A・B・C）を分類します。
""")

# =====================
# セッション管理
# =====================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =====================
# 語彙定義
# =====================
IMPLICIT_WORDS = ["そう", "みたい", "らしい", "得意", "好きそう", "真面目"]
SOFTENING_WORDS = ["まぁ", "別に", "一応", "特に"]
EMOTION_WORDS = ["大変", "疲れ", "困る", "嫌"]
DELEGATION_WORDS = ["任せ", "どちらでも", "お好きに", "決めて"]

# =====================
# stage定義
# =====================
def stage1_basic_context(text):
    return {
        "stage": "stage1",
        "label": "基本発話タイプ",
        "note": "評価・判断文の可能性"
    }

def stage2_ambiguity(text):
    ambiguous = any(w in text for w in SOFTENING_WORDS)
    return {
        "stage": "stage2",
        "label": "曖昧性検出",
        "note": "曖昧表現あり" if ambiguous else "曖昧表現なし"
    }

def stage3_emotion_cause(text):
    detected = [w for w in EMOTION_WORDS if w in text]
    return {
        "stage": "stage3",
        "label": "感情・背景推定",
        "note": f"感情語検出: {', '.join(detected)}" if detected else "感情語なし"
    }

def stage4_modality(text):
    detected = [w for w in IMPLICIT_WORDS if w in text]
    return {
        "stage": "stage4",
        "label": "含意・修飾検出",
        "note": f"含み語彙検出: {', '.join(detected)}" if detected else "含意なし"
    }

def stage5_case_relation(text):
    delegated = any(w in text for w in DELEGATION_WORDS)
    return {
        "stage": "stage5",
        "label": "格・責任関係",
        "note": "判断主体が相手に委ねられている" if delegated else "判断主体は明示的"
    }

# =====================
# 文脈タイプ分類
# =====================
def classify_context(stages):
    stage2_note = stages[1]["note"]
    stage3_note = stages[2]["note"]
    stage4_note = stages[3]["note"]
    stage5_note = stages[4]["note"]

    b_score = 0
    c_score = 0

    if "曖昧表現あり" in stage2_note:
        b_score += 1
    if "感情語検出" in stage3_note:
        b_score += 1
    if "含み語彙検出" in stage4_note:
        b_score += 1
    if "委ねられている" in stage5_note:
        c_score += 2

    if c_score >= 2:
        return "C：判断委ね型"
    if b_score >= 2:
        return "B：感情・含み型"
    return "A：日常のすれ違い型"

# =====================
# 最終要約
# =====================
def summarize(context_type):
    if context_type.startswith("A"):
        return "前提や期待の共有不足による軽度な文脈ズレが想定されます。"
    if context_type.startswith("B"):
        return "感情や評価が直接表現されず、含意として示唆されています。"
    if context_type.startswith("C"):
        return "判断や責任の所在が相手側に委ねられています。"
    return "明確な文脈ズレは検出されませんでした。"

# =====================
# チャット表示
# =====================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("文を入力してください")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    stages = [
        stage1_basic_context(user_input),
        stage2_ambiguity(user_input),
        stage3_emotion_cause(user_input),
        stage4_modality(user_input),
        stage5_case_relation(user_input),
    ]

    context_type = classify_context(stages)
    summary = summarize(context_type)

    with st.chat_message("assistant"):
        st.markdown("### 推論ステージ")
        for s in stages:
            st.markdown(f"- **{s['stage']}**：{s['label']}（{s['note']}）")

        st.markdown("---")
        st.markdown(f"### 文脈タイプ：{context_type}")
        st.markdown(summary)

    st.session_state.messages.append({
        "role": "assistant",
        "content": f"**文脈タイプ：{context_type}**\n\n{summary}"
    })