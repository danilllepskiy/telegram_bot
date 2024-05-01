from aiogram.dispatcher.filters.state import StatesGroup, State

__all__ = ["High", "Low", "Custom"]


class High(StatesGroup):
    """
    Класс описывающий FSM состояния для команды /high и её callback

    """

    answer = State()  # Ожидание ответа от пользователя: с/без жанра
    genre = State()  # Ожидание выбора жанра
    page = State()  # Ожидание просмотра следующей страницы


class Low(StatesGroup):
    """
    Класс описывающий FSM состояния для команды /low и её callback

    """

    answer = State()  # Ожидание ответа от пользователя: с/без жанра
    genre = State()  # Ожидание выбора жанра
    page = State()  # Ожидание просмотра следующей страницы


class Custom(StatesGroup):
    """
    Класс описывающий FSM состояния для команды /custom и её callback и message handlers

    """

    rated = State()  # Ожидание ответа от пользователя(низкий/высокий жанр)
    genre = State()  # Ожидание выбора жанра
    start_year = State()  # Ожидание выбора стартового диапазона поиска по году
    end_year = State()  # Ожидание выбора конечного диапазона поиска по году
    page = State()  # Ожидание просмотра следующей страницы
