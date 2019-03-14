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
	if current_user.is_admin():
		form = EditProfileForm('','')
		users = current_user.query.all()
		return render_template('admin/userlist.html', users=users, form=form)
	return redirect(url_for('main.feed'))

@bp.route('/editUser/<int:id>', methods=['GET','POST'])
@login_required
def editUser(id):
	user = User.query.get(id)
	form = EditProfileForm(user.username,user.email, obj=user)
	if request.method == 'POST' and form.validate():
		if request.form['action'] == 'edit':
			updatedUser=User(id=user.id, username=form.username.data, email=form.email.data,role=form.role.data)
			form.populate_obj(user)
			db.session.merge(user)
			db.session.flush()
			db.session.commit()
			flash('Your changes have been saved.')
			return redirect(url_for('admin.userList'))
		elif request.form['action'] == 'delete':

			form.populate_obj(user)
			current_user.delete_user(user)
			db.session.commit()

			flash('User Deleted')
			return redirect(url_for('admin.userList'))
		else:
			flash("submit authentication failed")
	#If form has not been submited or failed form validattion
	flash('did nothing')
	flash(form.errors)
	flash('Form validation funciton result:' + form.validate())
	for error in form.username.errors:
		flash(error)
	for error in form.email.errors:
		flash(error)
	return redirect(url_for('admin.userList'))
