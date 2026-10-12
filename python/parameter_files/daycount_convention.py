import datetime

def daycount(startDate, endDate, convention):
    startDate = datetime.datetime.strptime(startDate, "%d/%m/%Y")
    endDate = datetime.datetime.strptime(endDate, "%d/%m/%Y")
    if convention == "A360":
        return (endDate - startDate).days / 360
    elif convention == "A365":
        return (endDate - startDate).days / 365
    elif convention == "30360":
        return None
