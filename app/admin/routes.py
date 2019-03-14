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
	
@app.route('/feed')
@login_required
def feed():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(page, app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('index', page=posts.next_num) \
    if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
    if posts.has_prev else None
    return render_template('index.html', title='Home', form=form,posts=posts.items, next_url=next_url,prev_url=prev_url)
