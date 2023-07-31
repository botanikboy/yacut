import re
from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .constants import SHORT_ID_PATTERN
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_link(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap is not None:
        return jsonify({'url': urlmap.original}), HTTPStatus.OK
    raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)


@app.route('/api/id/', methods=['POST'])
def add_link():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    if not data.get('custom_id'):
        short_id = get_unique_short_id()
        while URLMap.query.filter_by(short=short_id).first():
            short_id = get_unique_short_id()
    else:
        if not re.match(SHORT_ID_PATTERN, data.get('custom_id')):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки')
        short_id = data.get('custom_id')

    if URLMap.query.filter_by(short=short_id).first():
        raise InvalidAPIUsage(f'Имя "{short_id}" уже занято.')

    urlmap = URLMap(
        original=data['url'],
        short=short_id
    )
    db.session.add(urlmap)
    db.session.commit()
    return jsonify({
        'url': urlmap.original,
        'short_link': f'{request.host_url}{urlmap.short}',
    }), HTTPStatus.CREATED
