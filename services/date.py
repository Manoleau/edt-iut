import datetime


def obtenir_jour_semaine_actuel():
    aujourdhui = datetime.date.today()
    lundi = aujourdhui - datetime.timedelta(days=aujourdhui.weekday())
    mardi = aujourdhui + datetime.timedelta(days=1 - aujourdhui.weekday() % 7)
    mercredi = aujourdhui + datetime.timedelta(days=2 - aujourdhui.weekday() % 7)
    jeudi = aujourdhui + datetime.timedelta(days=3 - aujourdhui.weekday() % 7)
    vendredi = aujourdhui + datetime.timedelta(days=4 - aujourdhui.weekday() % 7)

    return [lundi, mardi, mercredi, jeudi, vendredi]