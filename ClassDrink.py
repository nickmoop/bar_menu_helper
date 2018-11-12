# coding: utf8
import json

ALL_DRINKS = []


class Drink:
    """
    Класс для упрощения работы с напитками.
    Пока содержит название напитка, состав, в меню или не в меню напиток.
    """

    def __init__(self, name='', compounds=None, in_menu=False):
        self.name = name
        self.compounds = list(compounds)
        self.in_menu = in_menu

    def info(self):
        """
        Вся информация о напитке.
        Название, состав и нахождение в меню

        :return: форматированная строка с информацией о напитке
        """

        message = 'name: {}\ncomposition: {}\nin_menu: {}'.format(
            self.name, self.compounds, self.in_menu
        )

        return message

    @classmethod
    def load_all_drinks_from_file(cls, file_name):
        """
        Метод для загрузки всех напитков из текстового файла.
        Образец текста см. в Drink.load. Загружает всё в память

        :param file_name: имя файла с форматированным текстом о напитках
        """

        # открывваем указанный файл. читаем все напитки
        with open(file_name, 'r') as resource_file:
            data = json.load(resource_file)

        # обрабатываем все считанные из файла напитки
        for key, values in data.items():
            # создаем нужные объекты Drink и заполняем значениями (из файла)
            new_drink = cls(
                name=key,
                compounds=values['compounds'], in_menu=values['in_menu']
            )
            ALL_DRINKS.append(new_drink)


def get_drink_by_name(drink_name):
    """
    Метод для поиска напитка (объект Drink) по имени

    :param drink_name: имя напитка который хотим найти
    :return: Drink-объект или None если не найден напиток с указанным именем
    """

    # TODO переделать цикл
    for drink in ALL_DRINKS:
        if drink.name == drink_name:
            return drink

    return None


def get_menu_drinks_by_compound(menu_drinks, compound):
    """
    Метод для получения напитков (Drink) меню содержащих указанный ингридиент

    :param menu_drinks: напитки в текущем меню
    :param compound: ингридиент который должен быть в напитке
    :return: список напитков которые содержат искомый ингридиент (compound)
    """

    drinks = []

    for drink in menu_drinks:
        if compound in drink.composition:
            drinks.append(drink)

    return drinks
