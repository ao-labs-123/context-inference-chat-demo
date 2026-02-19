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

        import streamlit as st
from project.rules.rules_C import detect_C

st.subheader("C：判断委ね構造解析")

text_c = st.text_area("文章を入力（C解析）", key="c_input")

if st.button("Cを解析"):
    result = detect_C(text_c)

    if result:

        st.markdown("## 🅲 判定結果")

        st.markdown(f"**subtype**：{result['subtype']}")
        st.markdown(f"**delegation_direction**：{result['delegation_direction']}")
        st.markdown(f"**trigger_words**：{', '.join(result['trigger_words'])}")
        st.markdown(f"**confidence**：{result['confidence']}")

        st.divider()

        # 🔎 構造レイヤー表示
        st.markdown("### 構造レイヤー")

        st.markdown(f"""
        C（判断委ね）
        └─ subtype: {result['subtype']}
            └─ delegation: {result['delegation_direction']}
                └─ trigger: {', '.join(result['trigger_words'])}
        """)

        # 🔵 サブタイプ説明表示（エビデンス補助）
        st.divider()
        st.markdown("### subtype解説")

        explanations = {
            "position": "主導権を相手に委ねる構造",
            "implicit": "社会的規範・暗黙基準への依存",
            "responsibility": "条件付きで行動責任を相手に移動",
            "consideration": "配慮・丁寧条件による判断委譲"
        }

        st.info(explanations.get(result["subtype"], ""))

    else:
        st.info("C構造は検出されませんでした。")