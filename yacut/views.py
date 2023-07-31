from random import random

from flask import flash, redirect, render_template, request

from . import app, db
from .forms import URLMapForm
from .models import URLMap


def get_unique_short_id():
    return str(random())[-6:]


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    # проблема в автотестах, если оставить проверку на уникальность
    # исходной ссылки, то срабатывает ошибка по проверке короткого
    # имени, аналогично и в api_views

    # original = form.original_link.data
    # urlmap = URLMap.query.filter_by(original=original).first()
    # if urlmap:
    #     flash('Такая ссылка уже есть в базе!')
    #     return render_template(
    #         'index.html', form=form,
    #         generated_link=request.base_url + urlmap.short)

    short_id = form.custom_id.data
    if short_id and URLMap.query.filter_by(short=short_id).first():
        flash(f'Имя {short_id} уже занято!')
        return render_template('index.html', form=form)
    if not short_id:
        short_id = get_unique_short_id()
        while URLMap.query.filter_by(short=short_id).first():
            short_id = get_unique_short_id()

    urlmap = URLMap(
        original=form.original_link.data,
        short=short_id
    )
    db.session.add(urlmap)
    db.session.commit()
    flash('Ваша новая ссылка готова: ')
    return render_template(
        'index.html',
        generated_link=f'{request.host_url}{urlmap.short}',
        form=form
    )


@app.route('/<short_id>')
def redirect_view(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(urlmap.original)
