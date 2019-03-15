from flask import render_template, redirect, url_for, flash, request, current_app, g, jsonify
from flask_login import login_user, current_user, login_required
from flask_babel import _, get_locale
from datetime import datetime

from app import db
from app.main import bp
from app.models import User, Post, Message, Notification
from app.main.forms import EditProfileForm, PostForm, SearchForm, MessageForm

@bp.before_app_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()
		g.search_form = SearchForm()
	g.locale = str(get_locale())

@bp.route('/')
@bp.route('/home')
def home():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.filter(Post.visibility != 'Private').order_by(Post.timestamp.desc()).paginate(
		page, current_app.config['POSTS_PER_PAGE'], False)
	return render_template('index.html', title='Explore', posts=posts.items)

@bp.route('/feed', methods=['GET', 'POST'])
@login_required
def feed():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(body=form.post.data, author=current_user, visibility=form.visibility.data)
		post.add_mapping()
		db.session.add(post)
		db.session.commit()
		flash('Your post is now live!')
		return redirect(url_for('main.feed'))
	page = request.args.get('page', 1, type=int)
	posts = current_user.followed_posts().paginate(
		page, current_app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('main.feed', page=posts.next_num) \
		if posts.has_next else None
	prev_url = url_for('main.feed', page=posts.prev_num) \
		if posts.has_prev else None
	return render_template('index.html', title='Home', form=form, posts=posts.items, next_url=next_url, prev_url=prev_url)

@bp.route('/login', methods=['GET', 'POST'])
@login_required
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.feed'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('main.feed')
		return redirect(next_page)
	return render_template('auth/login.html', title='Sign in', form=form)

@bp.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	page = request.args.get('page', 1, type=int)
	posts = user.posts.order_by(Post.timestamp.desc()).paginate(
		page, current_app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('main.user', username=user.username, page=posts.next_num) \
		if posts.has_next else None
	prev_url = url_for('main.user', username=user.username, page=posts.prev_num) \
		if posts.has_prev else None
	return render_template('user.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)

@bp.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
	form = EditProfileForm(current_user.username)
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('main.edit_profile'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', title='Edit Profile', form=form)

@bp.route('/search')
@login_required
def search():
	if not g.search_form.validate():
		return redirect(url_for('main.explore'))
	page = request.args.get('page', 1, type=int)
	posts, total = Post.search(g.search_form.q.data, page,
								current_app.config['POSTS_PER_PAGE'])
	next_url = url_for('main.search', q=g.search_form.q.data, page=page +1) \
		if total > page * current_app.config['POSTS_PER_PAGE'] else None
	prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
		if page > 1 else None
	return render_template('search.html', title='Search', posts=posts, next_url=next_url, prev_url=prev_url)

@bp.route('/follow/<username>')
@login_required
def follow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('User %(username)s not found.',username=username)
		return redirect(url_for('main.feed'))
	if user == current_user:
		flash('You cannot follow yourself!')
		return redirect(url_for('main.user',username=username))
	current_user.follow(user)
	db.session.commit()
	flash('You are following ' + username +'!')
	return redirect(url_for('main.user', username=username))

@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('User %{username}s not found.',username=username)
		return redirect(url_for('main.feed'))
	if user == current_user:
		flash('You cannot unfollow yourself!')
		return redirect(url_for('main.user', username=username))
	current_user.unfollow(user)
	db.session.commit()
	flash('You are not following %(username)s.', username=username)
	return redirect(url_for('main.user', username=username))

@bp.route('/user/<username>/popup')
@login_required
def user_popup(username):
	user = User.query.filter_by(username=username).first_or_404()
	return render_template('user_popup.html', user=user)

@bp.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
	user = User.query.filter_by(username=recipient).first_or_404()
	form = MessageForm()
	if form.validate_on_submit():
		msg = Message(author=current_user, recipient=user, body=form.message.data)
		db.session.add(msg)
		user.add_notification('unread_message_count', user.new_messages())
		db.session.commit()
		flash('Your message has been sent')
		return redirect(url_for('main.user', username=recipient))
	return render_template('send_message.html', title='Send Message', form=form, recipient=recipient)

@bp.route('/messages')
@login_required
def messages():
	current_user.last_message_read_time = datetime.utcnow()
	current_user.add_notification('unread_message_count', 0)
	db.session.commit()
	page = request.args.get('page', 1, type=int)
	messages = current_user.messages_received.order_by(
		Message.timestamp.desc()).paginate(
			page, current_app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('main.messages', page=messages.next_num) \
		if messages.has_next else None
	prev_url = url_for('main.messages', page=messages.prev_num) \
		if messages.has_prev else None
	return render_template('messages.html', messages=messages.items,
							next_url=next_url, prev_url=prev_url)

@bp.route('/notifications')
@login_required
def notifications():
	since = request.args.get('since', 0.0, type=float)
	notifications = current_user.notifications.filter(
		Notification.timestamp > since).order_by(Notification.timestamp.asc())
	return jsonify([{
		'name': n.name,
		'data': n.get_data(),
		'timestamp': n.timestamp
	} for n in notifications])
