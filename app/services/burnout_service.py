def calculate_burnout(records):

    if not records:
        return None

    fatigue_avg = sum(r.fatigue_score for r in records) / len(records)
    stress_avg = sum(r.stress_level for r in records) / len(records)
    sleep_avg = sum(r.sleep_hours for r in records) / len(records)
    productivity_avg = sum(r.productivity_score for r in records) / len(records)

    fatigue_norm = fatigue_avg / 10
    stress_norm = stress_avg / 10
    sleep_norm = sleep_avg / 8
    productivity_norm = productivity_avg / 10

    burnout_score = (
        fatigue_norm * 0.35 +
        stress_norm * 0.35 +
        (1 - sleep_norm) * 0.15 +
        (1 - productivity_norm) * 0.15
    ) * 100

    burnout_score = max(0, min(100, burnout_score))

    if burnout_score < 35:
        risk = "LOW"
    elif burnout_score < 65:
        risk = "MODERATE"
    else:
        risk = "HIGH"

    return round(burnout_score, 2), risk