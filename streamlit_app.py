import streamlit as st
from project.rules.rules_A import detect_A

st.subheader("A：日常の行き違い解析")

text = st.text_area("文章を入力")

if st.button("解析"):
    result = detect_A(text)

    if result:

        st.markdown("## 🅰 判定結果")

        st.markdown(f"**軸**：{result['axis']}")
        st.markdown(f"**タグ**：{', '.join(result['tags'])}")
        st.markdown(f"**状態**：{result['state']}")
        st.markdown(f"**トリガー**：{', '.join(result['triggers'])}")

        st.divider()

        # レイヤー表示（エビデンス風）
        st.markdown("### 構造レイヤー")

        st.markdown(f"""
        A（期待ズレ）
        └─ {result['axis']}
            └─ {', '.join(result['tags'])}
                └─ {result['state']}
        """)

    else:
        st.info("A構造は検出されませんでした。")

        import streamlit as st
from project.rules.rules_B import detect_B

st.subheader("B：評価構造解析")

text = st.text_area("文章を入力（B解析）", key="b_input")

if st.button("Bを解析"):
    result = detect_B(text)

    if result:

        st.markdown("## 🅱 判定結果")

        st.markdown(f"**source**：{result['source']}")
        st.markdown(f"**strength**：{result['strength']}")
        st.markdown(f"**評価語**：{', '.join(result['eval_words'])}")

        if result["attitude_triggers"]:
            st.markdown(f"**態度トリガー**：{', '.join(result['attitude_triggers'])}")

        st.markdown(f"**confidence**：{result['confidence']}")

        st.divider()

        # レイヤー可視化
        st.markdown("### 構造レイヤー")

        st.markdown(f"""
        B（評価）
        └─ source: {result['source']}
            └─ strength: {result['strength']}
                └─ eval: {', '.join(result['eval_words'])}
        """)

    else:
        st.info("B構造は検出されませんでした。")