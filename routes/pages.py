from flask import Blueprint, render_template

pages_bp = Blueprint('pages', __name__)


@pages_bp.route('/')
def descripcion():
    return render_template('descripcion.html')


@pages_bp.route('/conceptos')
def conceptos():
    return render_template('conceptos.html')
