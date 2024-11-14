import datetime


def obtenir_jour_semaine_actuel():
    aujourdhui = datetime.date.today()
    lundi = aujourdhui - datetime.timedelta(days=aujourdhui.weekday())
    mardi = aujourdhui + datetime.timedelta(days=1 - aujourdhui.weekday() % 7)
    mercredi = aujourdhui + datetime.timedelta(days=2 - aujourdhui.weekday() % 7)
    jeudi = aujourdhui + datetime.timedelta(days=3 - aujourdhui.weekday() % 7)
    vendredi = aujourdhui + datetime.timedelta(days=4 - aujourdhui.weekday() % 7)
    if aujourdhui.weekday() == 5 or aujourdhui.weekday() == 6:
        lundi = lundi + datetime.timedelta(days=7)
        mardi = mardi + datetime.timedelta(days=7)
        mercredi = mercredi + datetime.timedelta(days=7)
        jeudi = jeudi + datetime.timedelta(days=7)
        vendredi = vendredi + datetime.timedelta(days=7)
    return [lundi, mardi, mercredi, jeudi, vendredi]