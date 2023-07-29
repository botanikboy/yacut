import re

from flask import jsonify, request

from . import app, db
from .models import URLMap
from .error_handlers import InvalidAPIUsage
from .views import get_unique_short_id
from .constants import SHORT_ID_PATTERN


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_link(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap is not None:
        return jsonify({'url': urlmap.original}), 200
    raise InvalidAPIUsage('Указанный id не найден', 404)


@app.route('/api/id/', methods=['POST'])
def add_link():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    if data.get('custom_id') is None or data.get('custom_id') == '':
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
        'short_link': request.host_url + urlmap.short,
    }), 201
