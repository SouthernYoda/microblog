from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from flask_wtf.csrf import CsrfProtect
from flask_babel import _, get_locale
from werkzeug.urls import url_parse

from app import db
from app.post import bp
from app.models import User, Post
from app.post.forms import PostForm

@bp.route('/view/<post_mapping>')
def post_mapping(post_mapping):
	post = Post.query.filter_by(url_mapping=post_mapping).first_or_404()
	user = User.query.filter_by(id=post.user_id).first()
	return render_template('post/view_post.html', post=post, username=user)

@bp.route('/export_posts')
@login_required
def export_posts():
	if current_user.get_task_in_progress('export_posts'):
		flash('An export task is currently in progress')
	else:
		current_user.launch_task('export_posts', 'Exporting posts...')
		db.session.commit()
	return redirect(url_for('main.user', username=current_user.username))

@bp.route('/newpost')
@login_required
def newpost():
		form = PostForm()
		if form.validate_on_submit():
			post = Post(body=form.post.data, author=current_user, visibility=form.visibility.data)
			post.add_mapping()
			db.session.add(post)
			db.session.commit()
			flash('Your post is now live!')
			return redirect(url_for('main.feed'))
		return	render_template('post/newpost.html', form=form)
