import json
from typing import Optional

from aiohttp.web_exceptions import HTTPConflict, HTTPBadRequest, HTTPNotImplemented, HTTPNotFound
from aiohttp_apispec import request_schema, response_schema

from app.quiz.schemes import (
    ThemeSchema, QuestionSchema,
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

    async def get(self):
        raise HTTPNotImplemented


class ThemeListView(View):
    async def get(self):
        themes = await self.request.app.store.quizzes.list_themes()
        raw_themes = [ThemeSchema().dump(theme) for theme in themes]
        return json_response(data={"themes": raw_themes})

    async def post(self):
        raise HTTPNotImplemented


class QuestionAddView(View):
    async def post(self):
        data = await self.request.json()
        title = data.get("title", None)
        theme_id = data.get("theme_id", None)
        answers = data.get("answers", None)

        answer_counter = 0
        for answer in answers:
            if answer["is_correct"]:
                answer_counter += 1
            if answer_counter > 1:
                raise HTTPBadRequest(text=json.dumps({"answers": ["all_answers_are_correct"]}))

        if answer_counter == 0:
            raise HTTPBadRequest(text=json.dumps({"answers": ["all_answers_are_incorrect"]}))

        if len(answers) == 1:
            raise HTTPBadRequest(text=json.dumps({"answers": ["only_one_answer"]}))

        theme_exist = await self.store.quizzes.get_theme_by_id(id_=theme_id)
        if not theme_exist:
            raise HTTPNotFound

        question_exist = await self.store.quizzes.get_question_by_title(title=title)
        if question_exist:
            raise HTTPConflict

        question = await self.store.quizzes.create_question(title=title, theme_id=theme_id, answers=answers)
        return json_response(data=QuestionSchema().dump(question))

    async def get(self):
        raise HTTPNotImplemented


class QuestionListView(View):
    async def get(self):
        try:
            theme_id = self.request.query["theme_id"]
        except KeyError:
            theme_id = 0

        questions = await self.request.app.store.quizzes.list_questions(int(theme_id))
        if not questions:
            return json_response(data={"questions": questions})

        raw_questions = [QuestionSchema().dump(question) for question in questions]
        return json_response(data={"questions": raw_questions})

    async def post(self):
        raise HTTPNotImplemented
