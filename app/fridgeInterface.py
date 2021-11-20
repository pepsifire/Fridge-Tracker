from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from .auth import login_required
from .db import get_db

bp = Blueprint('fridgeInterface', __name__)

@bp.route('/')
def index():
    db = get_db()
    fridges = db.execute(
        'SELECT f.id, fridgeName, owner_id, created'
        ' FROM fridge f JOIN user u on f.owner_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('interface/index.html', fridges=fridges)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        fridgeName = request.form['name']
        error = None
        if not fridgeName:
         error = 'Name is required'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO fridge (owner_id, fridgeName)'
                ' VALUES (?, ?)',
                (g.user['id'], fridgeName)
            )
            db.commit()
            return redirect(url_for('fridgeInterface.index'))
    return render_template('interface/create.html')

def get_fridge(id, check_owner=True):
    fridge = get_db().execute(
        'SELECT f.id, fridgeName, owner_id, created'
        ' FROM fridge f JOIN user u on f.owner_id = u.id'
        ' WHERE f.id = ?',
        (id,)
    ).fetchone()

    if fridge is None:
        abort(404, "Fridge not found")
    if check_owner and fridge['owner_id'] != g.user['id']:
        abort(403, "Forbidden")
    return fridge
def get_items(fridgeId, check_owner=True):
    items = get_db().execute(
        'SELECT i.itemName, i.spoilDate, i.itemType, i.fridge, f.id, f.owner_id'
        ' FROM item i JOIN fridge f on f.id = i.fridge'
        ' WHERE f.id = ?',
        (fridgeId,)
    ).fetchall()

    return items

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    fridge = get_fridge(id)

    if request.method == 'POST':
        itemName = request.form['itemName']
        spoilDate = request.form['spoilDate']
        itemType = request.form['itemType']
        error = None

        if not itemName or not spoilDate or not itemType:
            error = "No item specified"
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO item ( itemName, spoilDate, itemType, fridge)'
                ' VALUES (?,?,?,?)',
                (itemName, spoilDate, itemType, id)
            )
            db.commit()
            return redirect(url_for('fridgeInterface.index'))
    return render_template('interface/update.html', fridge=fridge)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_fridge(id)
    db = get_db()
    db.execute('DELETE FROM fridge WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('fridgeInterface.index'))

@bp.route('/<int:id>/addItem', methods=('GET', 'POST'))
@login_required
def addItem(id):
    items = get_items(id)

    if request.method == 'POST':
        itemName = request.form['itemName']
        spoilDate = request.form['spoilDate']
        itemType = request.form['itemType']
        error = None

        if not itemName or not spoilDate or not itemType:
            error = "No item specified"
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO item ( itemName, spoilDate, itemType, fridge)'
                ' VALUES (?,?,?,?)',
                (itemName, spoilDate, itemType, id)
            )
            db.commit()
            return redirect(url_for('fridgeInterface.index'))
    return render_template('interface/addItem.html', items=items)

@bp.route('/<int:id>/view')
@login_required
def viewItems(id):
    items = get_items(id)
    return render_template('interface/view.html', items=items, fridgeId=id)

@bp.route('/deleteItem', methods=('POST',))
@login_required
def deleteItem():
    if request.method == 'POST':
        itemName = request.form['itemName']
        spoilDate = request.form['spoilDate']
        itemType = request.form['itemType']
        error = None

        if not itemName or not spoilDate or not itemType:
            error = "No item specified"
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute('DELETE FROM item WHERE (itemName, spoilDate, itemType) = (?,?,?)', (itemName, spoilDate, itemType))
            db.commit()
    return redirect(url_for('fridgeInterface.index'))