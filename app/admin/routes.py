from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from flask_wtf.csrf import CsrfProtect
from flask_babel import _, get_locale
from werkzeug.urls import url_parse

from app import db		
from app.admin import bp											  
from app.models import User
from app.admin.forms import EditProfileForm

@bp.route('/userlist')
@login_required
def userList():
	if current_user.is_admin(current_user):
		users = current_user.query.all()
		return render_template('admin/userlist.html', users=users)
	return redirect(url_for('main.index'))

@bp.route('/editUser/<int:id>', methods=['GET','POST'])
@login_required
def editUser(id):
	user = User.query.get(id)
	form = EditProfileForm(user.username,user.email, obj=user)
	if request.method == 'POST' and form.validate():
		form.populate_obj(user)
		db.session.add(user)
		db.session.commit()
		flash(id)
		flash('Your changes have been saved.')
		return redirect(url_for('admin.userList'))
	for error in form.username.errors:
		flash(error)
	for error in form.email.errors:
		flash(error)
	return redirect(url_for('admin.userList')) 