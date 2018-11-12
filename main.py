# coding: utf8

import gui
from ClassDrink import Drink


if __name__ == '__main__':
    # загружаем все напитки из файла
    file_name = 'drinks.json'
    Drink.load_all_drinks_from_file(file_name)

    # нарисуем gui со всеми столбиками
    gui.fill_list_boxes()
    gui.main_window.mainloop()
