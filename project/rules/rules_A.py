# rules_A.py

from project.lexicon.lexicon_A import (
    REQUEST_WORDS,
    ACTION_WORDS,
    CONTRAST_WORDS,
    POSITIVE_WORDS,
    TIME_WORDS,
    PERSPECTIVE_WORDS,
    DEICTIC_WORDS,
)

def contains_with_triggers(text, word_list):
    hits = [w for w in word_list if w in text]
    return len(hits) > 0, hits


def detect_A(text):

    result = {
        "type": "A",
        "axis": None,
        "tags": [],
        "state": None,
        "triggers": []
    }

    # ===== request軸検出 =====
    has_request, req_hits = contains_with_triggers(text, REQUEST_WORDS)
    has_action, act_hits = contains_with_triggers(text, ACTION_WORDS)

    if has_request and has_action:
        result["axis"] = "request"
        result["triggers"] += req_hits + act_hits

        # タグ判定
        has_time, time_hits = contains_with_triggers(text, TIME_WORDS)
        has_persp, persp_hits = contains_with_triggers(text, PERSPECTIVE_WORDS)

        if has_time:
            result["tags"].append("time")
            result["triggers"] += time_hits

        if has_persp:
            result["tags"].append("perspective")
            result["triggers"] += persp_hits

        if not result["tags"]:
            result["tags"].append("implicit")

        # 解消判定
        has_contrast, contrast_hits = contains_with_triggers(text, CONTRAST_WORDS)
        has_positive, positive_hits = contains_with_triggers(text, POSITIVE_WORDS)

        result["triggers"] += contrast_hits + positive_hits

        if has_contrast and has_positive:
            result["state"] = "resolved"
        else:
            result["state"] = "unresolved"

        return result

    # ===== reference軸検出 =====
    has_deictic, deictic_hits = contains_with_triggers(text, DEICTIC_WORDS)

    if has_deictic:
        result["axis"] = "reference"
        result["tags"].append("deictic")
        result["state"] = "unresolved"
        result["triggers"] += deictic_hits
        return result

    return None