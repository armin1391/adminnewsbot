# ==========================
# Category Engine v1.7
# ==========================

from config import CATEGORY_RULES


def calculate_score(text, keywords):

    score = 0

    for word in keywords:

        if word in text:
            score += 1

    return score



def detect_category_advanced(title, source=""):

    text = title.lower()

    scores = {}


    for category, rules in CATEGORY_RULES.items():

        score = 0


        # کلمات مثبت
        for word in rules.get("keywords", []):

            if word in text:
                score += 2


        # کلمات منفی
        for word in rules.get("negative", []):

            if word in text:
                score -= 3


        # اولویت منبع
        for site in rules.get("sources", []):

            if site in source:
                score += 10


        scores[category] = score



    if not scores:
        return "همه"


    best_category = max(
        scores,
        key=scores.get
    )


    if scores[best_category] <= 0:
        return "همه"


    return best_category