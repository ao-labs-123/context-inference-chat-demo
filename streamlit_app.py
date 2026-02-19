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