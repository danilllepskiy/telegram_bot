from typing import Dict, Tuple, List, Any
from aiogram import types
from translate import Translator
from .handler_info_text import handler_string
from .check_photo import download_photo
from settings import Settings

import json
import requests

__all__ = ["get_start_info_high", "handler_response"]

site = Settings()


def get_start_info_high(
    user_data: Dict,
) -> Tuple[str, List[types.InputMediaPhoto]] | Tuple[None, None]:
    """
    Функция выполняет запрос к API и при помощи других функций формирует ответ

    :param user_data: Dict
        Получаем критерии запроса от пользователя

    :return: Tuple[str, List[types.InputMediaPhoto]]
        Возвращаем строку с описанием всех фильмов и фотографии фильмов
    """
    url = "https://moviesdatabase.p.rapidapi.com/titles"
    querystring = dict()

    match user_data:
        case {
            "search": "top_rated_english_250",
            "page": int(page),
            "genre": None,
            **kwargs,
        } if not kwargs:
            querystring = {
                "list": "top_rated_english_250",
                "page": str(page),
                "info": "base_info",
                "endYear": "2020",
            }

        case {
            "search": "top_rated_english_250",
            "page": int(page),
            "genre": str(genre),
            **kwargs,
        } if not kwargs:
            querystring = {
                "genre": genre,
                "list": "top_rated_english_250",
                "page": str(page),
                "info": "base_info",
                "endYear": "2020",
            }

        case {
            "search": "top_rated_lowest_100",
            "page": int(page),
            "genre": None,
            **kwargs,
        } if not kwargs:
            querystring = {
                "list": "top_rated_lowest_100",
                "page": str(page),
                "info": "base_info",
                "endYear": "2020",
            }

        case {
            "search": "top_rated_lowest_100",
            "page": int(page),
            "genre": str(genre),
            **kwargs,
        } if not kwargs:
            querystring = {
                "genre": genre,
                "list": "top_rated_lowest_100",
                "page": str(page),
                "info": "base_info",
                "endYear": "2020",
            }

    # print(querystring)

    headers = {
        "X-RapidAPI-Key": site.api_key.get_secret_value(),
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring)
    # print(response.json())
    data = json.loads(response.text)
    # Проверяем, если внутри ничего нет, то возвращаем None
    if data["entries"] == 0:
        return None, None

    all_info = handler_response(data)
    info_string = handler_string(all_info)
    photos = download_photo(all_info)

    return info_string, photos


def handler_response(info: Dict) -> List[Dict[str, Any | None]]:
    """
    Функция вытаскивает всю нужную информацию из полученного ответа от API

    :param info: Dict
        Получаем Dict от API в котором вся информация лежит

    :return: List[Dict[str, Any | None]]
        Возвращает List внутри которого находятся Dict для каждого фильма
    """

    data = []

    translator = Translator(from_lang="en", to_lang="ru")

    for i_count in info["results"]:

        photo_movie = i_count.get("primaryImage")
        if photo_movie is not None:
            photo_movie = photo_movie.get("url")

        rating_movie = i_count.get("ratingsSummary")
        if rating_movie is not None:
            rating_movie = rating_movie.get("aggregateRating")

        name_movie = i_count.get("titleText")
        if name_movie is not None:
            name_movie = name_movie.get("text")

        name_movie_ru = translator.translate(name_movie)

        release_year = i_count.get("releaseYear")
        if release_year is not None:
            release_year = release_year.get("year")

        description = i_count.get("plot")
        if description is not None:
            description = description.get("plotText")
            if description is not None:
                description = description.get("plainText")
        if description is not None and len(description) <= 1000:
            description_ru = translator.translate(description)
        else:
            description_ru = "Извините, описание на русском языке отсутствует."

        info_of_film = {
            "name": name_movie_ru,
            "rating": rating_movie,
            "image": photo_movie,
            "year": release_year,
            "description": description_ru,
        }

        data.append(info_of_film)

    return data
