from project.lexicon.lexicon_A import (
    REQUEST_WORDS,
    ACTION_WORDS,
    CONTRAST_WORDS,
    TIME_WORDS,
    PERSPECTIVE_WORDS,
    DEICTIC_WORDS
)

def contains_any(text, word_list):
    return any(word in text for word in word_list)


def detect_A(text):

    # A-1 実行報告型ズレ
    if (
        contains_any(text, REQUEST_WORDS)
        and contains_any(text, ACTION_WORDS)
        and contains_any(text, CONTRAST_WORDS)
    ):
        return "A-1"

    # A-2 暗黙期待型
    if (
        contains_any(text, REQUEST_WORDS)
        and contains_any(text, ACTION_WORDS)
    ):
        return "A-2"

    # A-3 参照ズレ
    if contains_any(text, DEICTIC_WORDS):
        return "A-3"

    # A-4 時間・視点ズレ
    if (
        contains_any(text, TIME_WORDS)
        or contains_any(text, PERSPECTIVE_WORDS)
    ):
        return "A-4"

    return None