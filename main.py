from typing import List
from fastapi import APIRouter, FastAPI, HTTPException, Response
from dataclasses import dataclass

app = FastAPI(description='Проектирование и реализация REST-API информационной системы для домашней видеотеки')

film_router = APIRouter(prefix='/films', tags=['Фильмы'])


# Класс фильма
@dataclass
class Film:
    id: int
    title: str = 'Оно'
    country: str = 'США'
    time: int = 130
    genre: str = 'Ужасы'
    year: int = 2017

# Класс со счетчиком
@dataclass
class FilmList:
    count: int
    films: List[Film]

# Список словарей
films = [
    {
        'id': 1,
        'title': 'Звездные войны: Эпизод IV - Новая надежда',
        'country': 'США',
        'time': 121,
        'genre': 'Фантастика',
        'year': 1977
    },
    {
        'id': 2,
        'title': 'Властелин колец: Братство кольца',
        'country': 'Новая Зеландия, США',
        'time': 178,
        'genre': 'Фэнтези',
        'year': 2001
    },
    {
        'id': 3,
        'title': 'Побег из Шоушенка',
        'country': 'США',
        'time': 142,
        'genre': 'Драма',
        'year': 1994
    }
]

# Эндпоинт для получения списка всех фильмов
@film_router.get('/', name='Все фильмы', response_model=FilmList)
def get_all_films():
    return FilmList(count=len(films), films=films)

# Эндпоинт для получения фильма по id
@film_router.get('/{film_id}', name='Получить фильм по id', response_model=Film)
def get_film(film_id: int):
    for film in films:
        if film['id'] == film_id:
            return film
    raise HTTPException(status_code=404, detail="Film not found")

# Эндпоинт для добавления фильма
@film_router.post('/', name='Добавить фильм', response_model=Film)
def create_film(Film: Film):
    new_film = {
        'id': len(films) + 1,
        'title': Film.title,
        'country': Film.country,
        'time': Film.time,
        'genre': Film.genre,
        'year': Film.year,
    }
    films.append(new_film)
    return new_film

# Эндпоинт для обновления данных фильма
@film_router.put('/{film_id}', name='Обновить данные фильма', response_model=Film)
def update_film(film_id: int, Film: Film):
    new_film = next((new_film for new_film in films if new_film['id'] == film_id), None)
    if new_film:
        new_film['id'] = Film.id
        new_film['title'] = Film.title
        new_film['country'] = Film.country
        new_film['time'] = Film.time
        new_film['genre'] = Film.genre
        new_film['year'] = Film.year
        return new_film
    raise HTTPException(status_code=404, detail="Film not found")

# Эндпоинт для удаления фильма
@film_router.delete('/{film_id}', name='Удалить фильм', response_class=Response)
def delete_film(film_id: int):
    for i, film in enumerate(tuple(films)):
        if film['id'] == film_id:
            del films[i]
            break
    return Response(status_code=204)


app.include_router(film_router)