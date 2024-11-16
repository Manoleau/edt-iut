import datetime
from ics import Calendar, Event
import requests
base_url = f"https://adelb.univ-lyon1.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=:resources-id:&projectId=0&calType=ical&firstDate=:first-date:&lastDate=:last-date:"

def obtenir(resources_id:str, first_date:datetime.date, last_date:datetime.date):
    url = (base_url
           .replace(":resources-id:", resources_id)
           .replace(":first-date:", f"{first_date:%Y-%m-%d}")
           .replace(":last-date:", f"{last_date:%Y-%m-%d}"))
    try:
        req = requests.get(url)
        if req.status_code == 200:
            cal = Calendar(req.text)
            events = cal.events
            sorted_events = sorted(events, reverse=False)
            return {
                'events' : sorted_events,
                'ics' : url,
            }
        else:
            res = {
                'events': [],
                'ics': None,
                'erreur': f"Erreur {req.status_code} - Impossible de récupérer les données depuis le serveur.\nVeuillez réessayer plus tard.",
            }
    except Exception as e:
        print(e)
        res = {
            'events' : [],
            'ics' : None,
            'erreur': e
        }
    return res
