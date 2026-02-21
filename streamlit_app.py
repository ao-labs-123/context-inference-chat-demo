import streamlit as st

from project.rules.rules_A import detect_A
from project.rules.rules_B import detect_B
from project.rules.rules_C import detect_C

st.title("構造解析エンジン A / B / C")

text = st.text_area("文章を入力してください")

if st.button("解析する"):

    result_A = detect_A(text)
    result_B = detect_B(text)
    result_C = detect_C(text)

    detected = []

    if result_A:
        detected.append(("A", result_A["confidence"], result_A))
    if result_B:
        detected.append(("B", result_B["confidence"], result_B))
    if result_C:
        detected.append(("C", result_C["confidence"], result_C))

    if not detected:
        st.info("構造は検出されませんでした。")
        st.stop()

    st.markdown("## 🔎 検出結果")

    for label, conf, res in detected:
        st.markdown(f"### {label}")
        st.markdown(f"**confidence**：{conf}")

        if label == "A":
            st.markdown(f"subtype：{res.get('subtype')}")
            st.markdown(f"trigger：{', '.join(res.get('trigger_words', []))}")

        elif label == "B":
            st.markdown(f"source：{res.get('source')}")
            st.markdown(f"strength：{res.get('strength')}")
            st.markdown(f"eval_words：{', '.join(res.get('eval_words', []))}")

        elif label == "C":
            st.markdown(f"subtype：{res.get('subtype')}")
            st.markdown(f"delegation：{res.get('delegation_direction')}")
            st.markdown(f"trigger：{', '.join(res.get('trigger_words', []))}")

        st.divider()

    # ===== Dominant Type 判定 =====
    dominant = max(detected, key=lambda x: x[1])

    st.markdown("## 🧠 Dominant Structure")
    st.success(f"{dominant[0]} が優勢（confidence: {dominant[1]}）")

    # ===== レイヤー統合表示 =====
    st.markdown("## 🏗 構造レイヤー")

    for label, conf, res in detected:

        if label == "A":
            st.markdown(f"""
            A（行き違い）
            └─ subtype: {res.get('subtype')}
                └─ trigger: {', '.join(res.get('trigger_words', []))}
            """)

        if label == "B":
            st.markdown(f"""
            B（評価）
            └─ source: {res.get('source')}
                └─ strength: {res.get('strength')}
                    └─ eval: {', '.join(res.get('eval_words', []))}
            """)

        if label == "C":
            st.markdown(f"""
            C（判断委ね）
            └─ subtype: {res.get('subtype')}
                └─ delegation: {res.get('delegation_direction')}
                    └─ trigger: {', '.join(res.get('trigger_words', []))}
            """)