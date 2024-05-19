from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/betting_results")
async def get_betting_results():
    url = "https://olimpbet.kz/betting"
    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
    else:
        return {"error": f"Ошибка при загрузке страницы: {response.status_code}"}

    soup = BeautifulSoup(html, "html.parser")

    results = []
    sports_of_interest = {
        '1': 'Футбол',
        '2': 'Хоккей',
        '3': 'Теннис',
        '5': 'Баскетбол',
        '9': 'Гандбол',
        '10': 'Волейбол',
        '11': 'Футзал',
        '35': 'Пляжный футбол',
        '40': 'Настольный теннис',
        '51': 'Бадминтон',
        '60': 'Пляжный волейбол',
        '67': 'Хоккей на траве',
        '113': 'Флорбол',
    }

    for row in soup.find_all("tr", {"class": ["forLiveFilter", "bg"]}):
        sport_id = row.get("data-sport")
        if sport_id in sports_of_interest:
            tab = row.find("a", class_="l-name-tab")
            score_tab = row.find("font", class_="txtmed l-name-tab")

            if tab:
                url = tab.get("href")
                home, away = tab.text.split(" - ")
            else:
                url = None
                home = away = None

            score = score_tab.text.strip() if score_tab else None
            sport_name = sports_of_interest.get(sport_id, None)

            home_score, away_score, periods = None, None, None

            if score:
                home_score_str, _, away_score_str = score.partition(":")
                try:
                    home_score = int(''.join(filter(str.isdigit, home_score_str)))
                except ValueError:
                    home_score = None
                try:
                    if away_score_str and away_score_str.split():
                        away_score = int(''.join(filter(str.isdigit, away_score_str.split()[0])))
                    else:
                        away_score = None
                except ValueError:
                    away_score = None

                if "(" in score and ")" in score:
                    periods = [item.strip() for item in score_tab.text.strip().split("(")[1].split(")")[0].split(',')]

            periods_dict = {}
            if periods is not None:
                for i, period in enumerate(periods, start=1):
                    if ':' in period:
                        p_home, p_away = period.split(':')
                        periods_dict[f"p{i}"] = period.strip()
                        periods_dict[f"p{i}h"] = p_home.strip()
                        periods_dict[f"p{i}a"] = p_away.strip()

            if sport_id is not None:
                result = {
                    "sport_id": sport_id.strip() if sport_id else None,
                    "sport_name": sport_name.strip() if sport_name else None,
                    "url": url,
                    "home": home.strip() if home else None,
                    "away": away.strip() if away else None,
                    "score": score,
                    "home_score": home_score,
                    "away_score": away_score,
                    "periods": periods
                }

                if periods is not None:
                    for i, period in enumerate(periods, start=1):
                        result[f"p{i}"] = period.strip()
                        result[f"p{i}h"] = periods_dict.get(f"p{i}h", None)
                        result[f"p{i}a"] = periods_dict.get(f"p{i}a", None)

                results.append(result)

    return results
