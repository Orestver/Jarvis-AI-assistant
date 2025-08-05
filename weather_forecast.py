import aiohttp
import asyncio
from urllib.parse import quote
from dotenv import load_dotenv
import os
from elevenlabsspeach import speak
load_dotenv()
WEATHER_API = os.getenv("WEATHER_API_KEY")


class WeatherForecast:
    def transliterate_city_name(self, city_name):
        translit_map = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g',
            'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z',
            'и': 'y', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k',
            'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
            'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
            'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
            'ь': '', 'ю': 'iu', 'я': 'ia', '’': '', "'": ''
        }
        return ''.join(translit_map.get(c, c) for c in city_name.lower())

    async def get_weather(self, city):
        if not city:
            print("⚠️ Введіть назву міста.")
            return

        try:
            city_latin = self.transliterate_city_name(city)
            city_encoded = quote(city_latin)
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city_encoded}&appid={WEATHER_API}&units=metric&lang=en"

            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    if response.status != 200:
                        print(f"❌ Не вдалося отримати дані (статус: {response.status})")
                        return

                    data = await response.json()

            if data.get("cod") != 200:
                print(f"❌ Місто «{city}» не знайдено (код: {data.get('cod')})")
                return

            temp = data["main"]["temp"]
            weather = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            message = (
                f" Temperature: {temp}°C\n"
                f" Description: {weather.capitalize()}\n"
                f" Humidity: {humidity}%\n"
                f" Wind speed: {wind_speed} meters per second"
            )
            print(message)
            speak(f"The weather in {city} is {temp} degrees Celsius")
            return message

        except aiohttp.ClientError as e:
            print(f"❌ Проблема з'єднання: {str(e)}")
        except asyncio.TimeoutError:
            print("❌ Запит перевищив час очікування.")
        except Exception as e:
            print(f"⚠️ Помилка: {str(e)}")



