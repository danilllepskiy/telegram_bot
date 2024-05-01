__all__ = ["handler_string"]


def handler_string(data) -> str:
    """
    Функция формирует строку с фильмами и рейтингом для вывода её пользователю Telegram

    :param data: List
        Список, внутри которого лежат Dict к каждому фильму с названием и рейтингом

    :return: str
        Возвращаем готовую строку для пользователя

    """

    info_string = ""
    count = 0

    for i_name in data:
        count += 1
        info_string += "{number}. Название: {name_movie}\nРейтинг: {rating}\nГод выпуска: {year}\nОписание: {description}\n\n".format(
            number=count,
            name_movie=i_name["name"],
            rating=i_name["rating"],
            year=i_name["year"],
            description=i_name["description"],
        )

    return info_string
