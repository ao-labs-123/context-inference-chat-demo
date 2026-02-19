# rules_B.py

from project.lexicon.lexicon_B_core import (
    EVALUATION_ADJ,
    EVALUATION_ADV,
    EVALUATIVE_NOUN,
)

from project.lexicon.lexicon_B_human import (
    PERSONALITY_ADJ,
    AMBIGUOUS_TRAITS,
    CHARACTER_NOUN,
)

from project.lexicon.lexicon_B_attitude import (
    CONTRAST_WORDS,
    LIMITATION_WORDS,
    INTERJECTION_WORDS,
    QUESTION_MARKERS,
    AGREEMENT_PRESSURE,
    HOLDING_PATTERNS,
)


def contains_with_hits(text, word_list):
    hits = [w for w in word_list if w in text]
    return hits


def detect_B(text):

    result = {
        "type": "B",
        "source": None,
        "strength": None,
        "eval_words": [],
        "attitude_triggers": [],
        "confidence": 0.0,
    }

    # ===== core評価検出 =====
    core_hits = []
    core_hits += contains_with_hits(text, EVALUATION_ADJ)
    core_hits += contains_with_hits(text, EVALUATION_ADV)
    core_hits += contains_with_hits(text, EVALUATIVE_NOUN)

    # ===== human評価検出 =====
    human_hits = []
    human_hits += contains_with_hits(text, PERSONALITY_ADJ)
    human_hits += contains_with_hits(text, AMBIGUOUS_TRAITS)
    human_hits += contains_with_hits(text, CHARACTER_NOUN)

    # ===== 態度トリガー検出 =====
    attitude_hits = []
    attitude_hits += contains_with_hits(text, CONTRAST_WORDS)
    attitude_hits += contains_with_hits(text, LIMITATION_WORDS)
    attitude_hits += contains_with_hits(text, INTERJECTION_WORDS)
    attitude_hits += contains_with_hits(text, QUESTION_MARKERS)
    attitude_hits += contains_with_hits(text, AGREEMENT_PRESSURE)
    attitude_hits += contains_with_hits(text, HOLDING_PATTERNS)

    # ===== source判定 =====
    if human_hits:
        result["source"] = "human"
        result["eval_words"] = human_hits
    elif core_hits:
        result["source"] = "core"
        result["eval_words"] = core_hits
    else:
        return None  # B構造なし

    # ===== 強度判定 =====
    if attitude_hits:
        result["strength"] = "strong"
        result["attitude_triggers"] = attitude_hits
    else:
        result["strength"] = "weak"

    # ===== confidence簡易算出 =====
    base_score = len(result["eval_words"]) * 0.3
    attitude_score = len(attitude_hits) * 0.2
    score = min(1.0, base_score + attitude_score)

    result["confidence"] = round(score, 2)

    return result