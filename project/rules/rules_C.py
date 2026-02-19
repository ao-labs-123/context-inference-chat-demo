# rules_C.py

from project.lexicon.lexicon_C import (
    POSITION_DEPENDENT,
    IMPLICIT_RULE,
    RESPONSIBILITY_IF,
    CONSIDERATION_DEPENDENT,
)


def contains_with_hits(text, word_list):
    return [w for w in word_list if w in text]


def detect_C(text):

    result = {
        "type": "C",
        "subtype": None,
        "trigger_words": [],
        "delegation_direction": None,
        "confidence": 0.0,
    }

    # ===== ① 立場依存型 =====
    position_hits = contains_with_hits(text, POSITION_DEPENDENT)

    # ===== ② 暗黙ルール型 =====
    implicit_hits = contains_with_hits(text, IMPLICIT_RULE)

    # ===== ③ 責任条件型 =====
    responsibility_hits = contains_with_hits(text, RESPONSIBILITY_IF)

    # 追加：相手主語 + なら
    if ("あなたが" in text or "相手が" in text or "君が" in text) and "なら" in text:
        responsibility_hits.append("相手主語＋なら")

    # ===== ④ 配慮依存型 =====
    consideration_hits = contains_with_hits(text, CONSIDERATION_DEPENDENT)

    # ===== subtype判定（優先順）=====
    # responsibility > consideration > position > implicit

    if responsibility_hits:
        result["subtype"] = "responsibility"
        result["trigger_words"] = responsibility_hits
        result["delegation_direction"] = "conditional"

    elif consideration_hits:
        result["subtype"] = "consideration"
        result["trigger_words"] = consideration_hits
        result["delegation_direction"] = "self→other (polite)"

    elif position_hits:
        result["subtype"] = "position"
        result["trigger_words"] = position_hits
        result["delegation_direction"] = "self→other"

    elif implicit_hits:
        result["subtype"] = "implicit"
        result["trigger_words"] = implicit_hits
        result["delegation_direction"] = "norm_based"

    else:
        return None  # C構造なし

    # ===== confidence算出 =====
    base = len(result["trigger_words"]) * 0.4
    score = min(1.0, base)

    result["confidence"] = round(score, 2)

    return result