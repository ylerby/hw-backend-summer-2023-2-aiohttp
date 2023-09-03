import json
from typing import Optional

from aiohttp.web_exceptions import HTTPConflict, HTTPBadRequest, HTTPNotImplemented

from app.quiz.schemes import (
    ThemeSchema,
)
from app.web.app import View
from app.web.utils import json_response

# TODO: добавить проверку авторизации для этого View
class ThemeAddView(View):
    # TODO: добавить валидацию с помощью aiohttp-apispec и marshmallow-схем
    async def post(self):

        data = await self.request.json()

        try:
            title: Optional[str] = data.get("title", None)
        except KeyError:
            raise HTTPBadRequest

        if title is None:
            raise HTTPBadRequest(text=json.dumps({"title": ["Missing data for required field."]}),
                                 reason="Title field is required")

        for titles in self.store.quizzes.app.database.themes:
            if title == titles.title:
                raise HTTPConflict

        theme = await self.store.quizzes.create_theme(title=title)
        return json_response(data=ThemeSchema().dump(theme))

    ''' title = (await self.request.json())[
            "title"
        ]  # TODO: заменить на self.data["title"] после внедрения валидации'''
        # TODO: проверять, что не существует темы с таким же именем, отдавать 409 если существует

    async def get(self):
        raise HTTPNotImplemented


class ThemeListView(View):
    async def get(self):
        themes = await self.request.app.store.quizzes.list_themes()
        raw_themes = [ThemeSchema().dump(theme) for theme in themes]
        return json_response(data={'themes': raw_themes})

    async def post(self):
        raise HTTPNotImplemented


class QuestionAddView(View):
    async def post(self):
        raise NotImplementedError


class QuestionListView(View):
    async def get(self):
        raise NotImplementedError
