import pyowm
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config

class TOWM:

	def __init__(self, owm_api_key):
		self.owm_api_key = owm_api_key
		self.config_dict = get_default_config()
		self.config_dict['language'] = 'ru'
		self.owm = OWM(owm_api_key, self.config_dict)
		self.mgr = self.owm.weather_manager()

	@staticmethod
	def get_weather_from_dict_to_str_ru(w_dict) -> str:
		answer = f"Город: {w_dict['location']['name']}, {w_dict['location']['country']}\n" \
		         f"Погода: {w_dict['weather']['detailed_status']}\n" \
		         f"Температура: {round((float(w_dict['weather']['temperature']['temp']) - 273.15), 2)} °C\n" \
		         f"Ощущается как: {round((float(w_dict['weather']['temperature']['feels_like']) - 273.15), 2)} °C\n" \
		         f"Влажность: {w_dict['weather']['humidity']}%\n" \
		         f"Ветер: {w_dict['weather']['wind']['speed']} m/s {TOWM.wind_deg_to_direction(float(w_dict['weather']['wind']['deg']))}\n" \
		         f"Давление: {round((w_dict['weather']['pressure']['press']) * 7.50062 * pow(10, -1), 2)} мм рт.ст.\n" \
		         f"Уровень облачности: {w_dict['weather']['clouds']}%\n" \
		         f"Видимость: {w_dict['weather']['visibility_distance']} м"
		return answer


	@staticmethod
	def wind_deg_to_direction(deg: float) -> str:
		direction = 'n/d'
		if deg > 348.75 and deg <= 11.25:
			direction = "N"
		elif deg > 11.25 and deg <= 33.75:
			direction = "NNE"
		elif deg > 33.75 and deg <= 56.25:
			direction = "NE"
		elif deg > 56.25 and deg <= 78.75:
			direction = "ENE"
		elif deg > 78.75 and deg <= 101.25:
			direction = "E"
		elif deg > 101.25 and deg <= 123.75:
			direction = "ESE"
		elif deg > 123.75 and deg <= 146.25:
			direction = "SE"
		elif deg > 146.25 and deg <= 168.75:
			direction = "SSE"
		elif deg > 168.75 and deg <= 191.25:
			direction = "S"
		elif deg > 191.25 and deg <= 213.75:
			direction = "SSW"
		elif deg > 213.75 and deg <= 236.25:
			direction = "SW"
		elif deg > 236.25 and deg <= 258.75:
			direction = "WSW"
		elif deg > 258.75 and deg <= 281.25:
			direction = "W"
		elif deg > 281.25 and deg <= 303.75:
			direction = "WNW"
		elif deg > 303.75 and deg <= 326.25:
			direction = "NW"
		elif deg > 326.25 and deg <= 348.75:
			direction = "NNW"
		else:
			direction = "none"
		return direction

	def get_weather(self, city: str) -> str:
		observation = self.mgr.weather_at_place(city)
		return TOWM.get_weather_from_dict_to_str_ru(observation.to_dict())

