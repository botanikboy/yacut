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
            Regexp(SHORT_ID_PATTERN,
                   message='короткий идентификатор должен быть не длинее '
                           '16 символов и содержать только буквы латинского '
                           'алфавита и цифры (a-z, A-Z, 0-9)')
        ]
    )
    submit = SubmitField('Создать')
