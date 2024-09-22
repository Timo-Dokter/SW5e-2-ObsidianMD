def get_prof_bonus_from_cr(cr):
    if cr < 5:
        return 2
    elif cr < 9:
        return 3
    elif cr < 13:
        return 4
    elif cr < 17:
        return 5
    elif cr < 21:
        return 6
    elif cr < 25:
        return 7
    elif cr < 29:
        return 8
    else:
        return 9
