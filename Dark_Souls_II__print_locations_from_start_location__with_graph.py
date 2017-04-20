#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def get_transitions_location(url_location):
    """
    Функция для поиска переходов из локации

    """

    import requests
    rs = requests.get(url_location)

    from bs4 import BeautifulSoup
    root = BeautifulSoup(rs.content, 'lxml')

    transitions = list()

    table_transitions = root.select_one('table.pi-horizontal-group')
    if not table_transitions or 'Переходы:' not in table_transitions.text:
        return transitions

    for a in table_transitions.select('a'):
        from urllib.parse import urljoin
        url = urljoin(rs.url, a['href'])

        transitions.append((url, a.text))

    return transitions


if __name__ == '__main__':
    global_transitions = set()

    # NOTE: For test rendering graph
    CACHE = True
    if CACHE:
        global_transitions = {('Святилище дракона', 'Убежище дракона'), ('Шульва, Священный город', 'Пещера мертвых'), ('Огненная Башня Хейда', 'Собор Лазурного Пути'), (' Ледяная Элеум Лойс', 'Большой собор'), ('Большой собор', 'Предвечный Хаос'), ('Двери Фарроса', 'Бухта Брайтстоун-Тселдора'), ('Маджула', 'Роща Охотника'), ('Лес Павших Гигантов', 'Память Ваммара'), ('Темнолесье', 'Цитадель Алдии'), ('Ледяная Элеум Лойс', 'Холодные Окраины'), ('Маджула', 'Могила Святых'), ('Железная цитадель', 'Башня Солнца'), ('Замок Дранглик', 'Трон Желания'), ('Темнолесье', 'Двери Фарроса'), ('Маджула', 'Лес Павших Гигантов'), ('Роща Охотника', 'Чистилище Нежити'), ('Долина Жатвы', 'Земляной Пик'), ('Храм Аманы', 'Склеп Нежити'), ('Мглистая Башня', 'Железный проход'), ('Темнолесье', 'Храм Зимы'), ('Бухта Брайтстоун-Тселдора', 'Личные Палаты Лорда'), ('Земляной Пик', 'Железная цитадель'), ('Склеп Нежити', 'Память Короля'), ('Забытая Крепость', 'Башня Луны'), ('Железная Цитадель', 'Мглистая Башня'), ('Могила Святых', 'Помойка'), ('Мглистая Башня', 'Память старого железного короля'), ('Гнездо Дракона', 'Храм Дракона'), ('Шульва, Священный город', 'Святилище дракона'), ('Лес Павших Гигантов', 'Память Орро'), ('Безлюдная Пристань', 'Огненная Башня Хейда'), ('Междумирье', 'Маджула'), ('Лес Павших Гигантов', 'Память Джейта'), ('Забытая Крепость', 'Холм Грешников'), ('Башня Солнца', 'Железная Цитадель'), ('Забытая Крепость', 'Безлюдная Пристань'), ('Большой собор', 'Ледяная Элеум Лойс'), ('Маджула', 'Темнолесье'), ('Замок Дранглик', 'Королевский проход'), ('Храм Зимы', 'Замок Дранглик'), ('Цитадель Алдии', 'Гнездо Дракона'), ('Помойка', 'Черная Расселина'), ('Лес Павших Гигантов', 'Забытая Крепость'), ('Храм Зимы', ' Ледяная Элеум Лойс'), ('Королевский проход', 'Храм Аманы'), ('Роща Охотника', 'Долина Жатвы'), ('Бухта Брайтстоун-Тселдора', 'Воспоминания Дракона'), ('Черная Расселина', 'Шульва, Священный город'), ('Храм Аманы', 'Королевский проход ')}

    else:
        visited_locations = list()

        def print_transitions(url, title):
            # if len(visited_locations) >= 7:
            #     return

            if title in visited_locations:
                return

            visited_locations.append(title)
            print(title, url)

            transitions = get_transitions_location(url)
            if not transitions:
                return transitions

            # Сначала напечатаем все связанные локации
            for url_trans, title_trans in transitions:
                print('    {} -> {}'.format(title_trans, url_trans))

            print('\n')

            # Поищем у этих локаций связаные с ними локации
            for url_trans, title_trans in transitions:
                if title_trans not in visited_locations:
                    # if len(global_transitions) >= 5:
                    #     return
                    #
                    global_transitions.add((title, title_trans))

                    print_transitions(url_trans, title_trans)


        url_start_location = 'http://ru.darksouls.wikia.com/wiki/%D0%9C%D0%B5%D0%B6%D0%B4%D1%83%D0%BC%D0%B8%D1%80%D1%8C%D0%B5'
        print_transitions(url_start_location, 'Междумирье')

        print()
        print(len(visited_locations), visited_locations)

    # TODO: pretty graph
    import networkx as nx
    G = nx.Graph()

    print(global_transitions)
    for title, title_trans in global_transitions:
        # print('{} -> {}'.format(title, title_trans))
        G.add_edge(title, title_trans)

    print()

    pos = nx.spring_layout(G)  # positions for all nodes

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=6)

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=70)

    # labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')

    import matplotlib.pyplot as plt
    # plt.figure(1)
    plt.axis('off')
    # plt.savefig("ds2_locations_graph.png")  # save as png
    plt.show()  # display