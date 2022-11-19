from os import getcwd
from pathlib import Path
from requests import get
from random import randint

class PixelEncounter:
	def __init__(self) -> None:
		self.first_api = "https://app.pixelencounter.com/api"
		self.second_api = "https://app.pixelencounter.com/api/v2"
		self.odata = " https://app.pixelencounter.com/odata"
		self.headers = {
			"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
		}

	def save_file(self, content: bytes, location: str = getcwd()) -> bool:
		with open(Path(location).joinpath(f"{randint(0, 86400)}.png"), "wb+",) as file:
			file.write(content)
			file.close()
		return True

	def get_monster(self, monster_id: int, size: int = 512) -> bool:
		response = get(
			f"{self.first_api}/basic/monsters/{monster_id}/png?size={size}",
			headers=self.headers).content
		return self.save_file(response)

	def get_random_monster(self, size: int = 512) -> bool:
		response = get(
			f"{self.first_api}/basic/monsters/random/png?size={size}",
			headers=self.headers).content
		return self.save_file(response)

	def get_monsters_list(self) -> bool:
		return get(f"{self.first_api}/basic/monsters", headers=self.headers).json()

	def get_monster_info(self, monster_id: int) -> dict:
		return get(
			f"{self.first_api}/basic/monsterdetails/{monster_id}",
			headers=self.headers).json()

	def get_monsters_list_info(
			self,
			rows: int = 10,
			order: str = "Id&desc",
			skip: int = 0,
			count: bool = True) -> dict:
		url = f"{self.odata}/basic/monsterdetails?top={rows}"
		if order:
			url += f"&orderby={order}"
		if skip:
			url += f"&skip={skip}"
		if count:
			url += f"&count={count}"
		return get(url, headers=self.headers).json()

	def get_monster_svg(
			self,
			size: int = 512,
			background_color: str = None,
			edge_brightness: int = 0,
			brightness_noise: int = 0,
			colored: bool = True,
			color_variations: int = 1,
			saturation: int = 1) -> bool:
		url = f"{self.second_api}/basic/svgmonsters/image/png?colored={colored}&size={size}"
		if background_color:
			url += f"&backgroundColor={background_color}"
		if edge_brightness:
			url += f"&edgeBrightness={edge_brightness}"
		if brightness_noise:
			url += f"&brightnessNoise={brightness_noise}"
		if color_variations:
			url += f"&colorVariations={color_variations}"
		if saturation:
			url += f"&saturation={saturation}"
		response = get(url, headers=self.headers).content
		return self.save_file(response)

	def get_random_planet(
			self,
			width: int = 1080,
			height: int = 1080,
			frame: int = None) -> bool:
		url = f"{self.first_api}/basic/planets?width={width}&height={height}"
		if frame:
			url += f"&frame={frame}"
		response = get(url, headers=self.headers).content
		return self.save_file(response)

	def get_planet(self, seed_id: int) -> bool:
		response = get(
			f"{self.first_api}/basic/planets/{seed_id}",
			headers=self.headers).content
		return self.save_file(response)
