# coding: utf8

from collections import defaultdict
from tkinter import *

from ClassDrink import ALL_DRINKS, get_drink_by_name, get_menu_drinks_by_compound


# TODO сделать по человечи
main_window = Tk()
main_window.resizable(False, False)
main_window.geometry("800x600+0+20")

scrollbar_all = Scrollbar(main_window)
all_drinks_listbox = Listbox(main_window, yscrollcommand=scrollbar_all.set)
all_drinks_listbox.place(x=20, y=20, width=200, height=400)
scrollbar_menu = Scrollbar(main_window)
menu_drinks_listbox = Listbox(main_window, yscrollcommand=scrollbar_menu.set)
menu_drinks_listbox.place(x=300, y=20, width=200, height=400)

scrollbar_ingredients = Scrollbar(main_window)
field_ingredients = Canvas(
    main_window, bg='white', yscrollcommand=scrollbar_ingredients.set
)
field_ingredients.place(x=540, y=20, width=240, height=400)

all_compounds = field_ingredients.create_text(
    0, 0, anchor='nw', fill='black', activefill='lavender'
)
info_compound = field_ingredients.create_text(
    0, 0, anchor='nw', fill='black'
)

scrollbar_all.config(command=all_drinks_listbox.yview)
scrollbar_all.place(x=220, y=20, height=400)
scrollbar_menu.config(command=menu_drinks_listbox.yview)
scrollbar_menu.place(x=500, y=20, height=400)
scrollbar_ingredients.config(command=field_ingredients.yview)
scrollbar_ingredients.place(x=780, y=20, height=400)

SORTED_COMPOUNDS = []


def fill_list_boxes():
    """
    Заполним все списки в gui на основе загруженных данных
    """

    for drink in ALL_DRINKS:
        # заполним список со всем напитками
        all_drinks_listbox.insert(END, drink.name)

        if drink.in_menu:
            # заполним список с напитками которые есть в меню (по дефолту)
            menu_drinks_listbox.insert(END, drink.name)

    # заполним список с ингридиентами напитков меню
    update_ingredients()


def add_to_menu(drink):
    """
    Метод для добавления напитков в меню.
    Меняет флаг in_menu на True

    :param drink: напиток (Drink) который хотим добавить в меню
    """

    menu_drinks = menu_drinks_listbox.get(0, END)
    # добавим напиток только если его еще нет в меню.
    # дублирование не нужно
    if drink.name not in menu_drinks:
        menu_drinks_listbox.insert(END, drink.name)


def clear():
    """
    Очистим меню от всех напитков
    Очистим список ингридиентов
    """

    try:
        # Чистим список с напитками меню
        menu_drinks_listbox.delete(0, END)
        # Чистим список с ингридиентами меню
        update_ingredients()
    # TODO make me!!!
    except:
        print('something wrong in clear')


def append_to_menu():
    """
    Добавим напиток в меню
    Добавим ингридиенты напитка в список ингридиентов меню
    """

    try:
        # получим объект Drink по имени выбранного напитка
        drink_name = all_drinks_listbox.get(all_drinks_listbox.curselection())
        drink = get_drink_by_name(drink_name)
        # добавим напиток в меню
        add_to_menu(drink)
        # добавим ингридиенты напитка
        update_ingredients()
    # TODO make me!!!
    except:
        print('something wrong in append to menu')


def remove_from_menu():
    """
    Удалим напиток из меню
    Удалим ингридиенты напитка из списка ингридиентов меню
    """

    try:
        # удаляем напиток из меню
        menu_drinks_listbox.delete(ANCHOR)
        # удаляем ингридиенты напитка
        update_ingredients()
    # TODO make me!!!
    except:
        print('something wrong in remove from menu')


def update_ingredients():
    """
    Метод для обновления (добавление\удаление)
    названий ингридиентов напитков меню и их количества.
    Сортирует ингридиенты по частоте использования в меню.
    """

    # глобальная переменная содержащая готовый текст вида:
    # количество_напитков_меню  название_ингридиента\n
    global SORTED_COMPOUNDS

    # получим ингридиенты и частоту их использования в напитках меню
    menu_compounds_dict = defaultdict(int)
    menu_drinks = menu_drinks_listbox.get(0, END)
    for drink_name in menu_drinks:
        drink = get_drink_by_name(drink_name)
        for compound in drink.compounds:
            menu_compounds_dict[compound] += 1

    # отсортируем все ингридиенты по частоте использования
    SORTED_COMPOUNDS = sort_compounds_by_count(menu_compounds_dict)

    # сделаем форматированную строку для отображения
    ingredients_text = ''
    for compound in SORTED_COMPOUNDS:
        ingredients_text += '{}  {}\n'.format(compound[1], compound[0])

    # пишем форматированную строку в gui
    field_ingredients.itemconfig(1, text=ingredients_text)


def sort_compounds_by_count(compounds_dict):
    """
    Метод для сортировки ингридиентов напитков меню по частоте их использования
    Возвращет сортированный список списков:
    [[название_ингридиента, частота_использования], [...], ...]

    :param compounds_dict: словарь с используемыми ингридиентами и
                                                        частотой использования
    :return: сортированный список пар ингридиент, частота использования
    """

    sorted_compounds_string = [
        (key, compounds_dict[key]) for key in sorted(
            compounds_dict, key=compounds_dict.get)
    ]

    return sorted_compounds_string


def field_ingredients_motion(event):
    """
    Метод для рисования сообщения со списком напитков
    в которых используется ингридиент, на название которого наведен курсор

    :param event: event motion с координатами курсора мыши
    """

    # получим порядковый номер названия ингридиента, по координатам курсора
    y = int(event.y / 15)
    # очистим текущее сообщение с напитками
    field_ingredients.itemconfig(2, text='')
    # если курсор наведен на какойто напиток, то работаем
    if SORTED_COMPOUNDS and y < len(SORTED_COMPOUNDS):
        # получим название ингридиента под курсором
        compound = SORTED_COMPOUNDS[y][0]

        # получим названия напитков меню, в которых есть ингридиент,
        # на который сейчас наведен курсор
        menu_drinks = []
        menu_drinks_names = menu_drinks_listbox.get(0, END)
        for drink_name in menu_drinks_names:
            drink = get_drink_by_name(drink_name)
            menu_drinks.append(drink)

        # получим список напитков (Drink) меню,
        # которые используют выбранный ингридиент
        menu_drinks_with_compound = get_menu_drinks_by_compound(
            menu_drinks, compound
        )

        # сделаем строку сообщение с названиями напитков меню,
        # которые содержат выбранный ингридиент
        message = ''
        for drink in menu_drinks_with_compound:
            message += '{}\n'.format(drink.name)

        # отобразим сообщение с названиями напитков меню
        field_ingredients.coords(2, (event.x + 10, y * 15))
        field_ingredients.itemconfig(2, text=message)


# TODO make me!
label_all_drinks = Label(main_window, text='All drinks')
label_all_drinks.place(x=20, y=0, height=20)

label_in_menu_drinks = Label(main_window, text='In menu')
label_in_menu_drinks.place(x=300, y=0, height=20)

label_menu_compounds = Label(main_window, text='Menu compounds')
label_menu_compounds.place(x=540, y=0, height=20)

field_ingredients.bind('<Motion>', field_ingredients_motion)

button_append_to_menu = Button(main_window, text='-->', command=append_to_menu)
button_append_to_menu.place(x=240, y=50, width=50, height=20)

button_remove_from_menu = Button(
    main_window, text='<--', command=remove_from_menu
)
button_remove_from_menu.place(x=240, y=70, width=50, height=20)

button_clear = Button(main_window, text='Clear', command=clear)
button_clear.place(x=300, y=420, width=100, height=20)
