from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.urls import url_parse
from flask_babel import _, get_locale
from app import db		
from app.admin import bp											  
from app.models import User
#from app.admin.forms import 

#@bp.route('/logout')
#def logout():
#	logout_user()
#	return redirect(url_for('main.index'))

@bp.route('/userlist')
@login_required
def userList():
	if current_user.is_admin(current_user):
		flash ('sucess')
		return render_template('admin/userlist.html')
	return redirect(url_for('main.index'))
	