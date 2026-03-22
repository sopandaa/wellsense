from datetime import timedelta


def get_status_from_burnout(risk):
    if risk == "HIGH":
        return "RED"
    elif risk == "MODERATE":
        return "YELLOW"
    return "GREEN"