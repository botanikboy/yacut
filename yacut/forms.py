from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField, StringField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL

from .constants import SHORT_ID_PATTERN


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 512), URL(message='Неверный формат ссылки')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(1, 16),
            Optional(),
            Regexp(SHORT_ID_PATTERN, message='a-z, A-Z, 0-9 - only')
        ]
    )
    submit = SubmitField('Создать')
