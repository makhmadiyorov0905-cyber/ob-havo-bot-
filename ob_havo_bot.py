import os
import requests
from datetime import datetime

TOKEN = os.environ["BOT_TOKEN"]
API_KEY = os.environ["WEATHER_API_KEY"]
CHAT_ID = os.environ["CHAT_ID"]
CITY = "Tashkent"

WEATHER_EMOJI = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Rain": "🌧",
    "Drizzle": "🌦",
    "Thunderstorm": "⛈",
    "Snow": "❄️",
    "Mist": "🌫",
}


def get_weather():
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={CITY}&appid={API_KEY}&units=metric&lang=uz"
    )
    response = requests.get(url, timeout=10)
    data = response.json()

    temp = round(data["main"]["temp"])
    feels_like = round(data["main"]["feels_like"])
    description = data["weather"][0]["description"]
    main = data["weather"][0]["main"]
    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"]
    emoji = WEATHER_EMOJI.get(main, "🌤")

    today = datetime.now().strftime("%d.%m.%Y")

    text = (
        f"{emoji} *{CITY} uchun ob-havo* — {today}\n\n"
        f"🌡 Harorat: {temp}°C (his qilinishi: {feels_like}°C)\n"
        f"📝 Holat: {description}\n"
        f"💧 Namlik: {humidity}%\n"
        f"💨 Shamol: {wind} m/s\n\n"
        f"Xayrli tong! Kuningiz yaxshi o'tsin 🌅"
    )
    return text


def send_message():
    text = get_weather()
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    r = requests.post(url, data=payload, timeout=10)
    if r.status_code == 200:
        print("Xabar muvaffaqiyatli yuborildi.")
    else:
        print(f"Xatolik: {r.text}")
        raise SystemExit(1)


if __name__ == "__main__":
    send_message()
