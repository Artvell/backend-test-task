import textwrap
from readability import Document
from bs4 import BeautifulSoup
import requests

class Parser:
    def __init__(
        self,
        url: str,
        width: int = 0,
        parse_images: bool = False
    ) -> None:
        """ Аргуметы:
            url: url сайта
            width: длина строки
            parse_images: добавить ссылки на картинки
        """
        headers = {
            'User-Agent': 'Mozilla/5.0',
        }
        self.width = width
        self.parse_images = parse_images
        try:
            response = requests.get(url, headers=headers)
            doc = Document(response.text)
            data = doc.summary()
        except requests.exceptions.MissingSchema:
            data = "ОШИБКА: Не указан http/https перед ссылкой"
        except requests.exceptions.ConnectionError:
            data = "ОШИБКА: Неверный адрес сайта или отсутствует Интернет-соединение"
        
        self.soup = BeautifulSoup(data, features="lxml")
        self.cleaned_data = ""
    
    def __img_to_string(self) -> None:
        """Переводит изобраения в ссылки"""
        for img in self.soup.find_all("img"):
            try:
                img.string = img["src"]
            except KeyError:
                pass
    
    def __clean_data(self) -> None:
        """Очищает данные от тегов"""
        self.cleaned_data = self.soup.get_text(" ", strip=True)
    
    def __line_alignment(self) -> None:
        """Выравнивает строку по кол-ву букв"""
        self.cleaned_data = textwrap.fill(self.cleaned_data, width=self.width, replace_whitespace=False)
    
    def parse(self) -> str:
        """Главный метод, вызывает все остальные"""
        if self.parse_images:
            self.__img_to_string()
        self.__clean_data()
        if self.width > 0:
            self.__line_alignment()
        return self.cleaned_data

