from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required

from App import db
from App.models import Post
from App.posts.forms import PostForm
from App.posts.utils import save_cover_picture

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        picture_file = save_cover_picture(form.picture.data)
        the_post = Post(title=form.title.data, content=form.content.data, coverPicture=picture_file,
                        price=form.price.data, author=current_user)
        db.session.add(the_post)
        db.session.commit()
        flash('Your post has been created', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@posts.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    the_post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=the_post.title, post=the_post)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    the_post = Post.query.get_or_404(post_id)
    if the_post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        the_post.title = form.title.data
        the_post.content = form.content.data
        the_post.price = form.price.data
        if form.picture.data:
            picture_file = save_cover_picture(form.picture.data)
            the_post.coverPicture = picture_file
        db.session.commit()
        flash('Update Successful', 'success')
        return redirect(url_for('posts.post', post_id=the_post.id))
    elif request.method == 'GET':
        form.title.data = the_post.title
        form.content.data = the_post.content
        form.price.data = the_post.price
    return render_template('create_post.html', title=the_post.title, form=form,
                           legend='Update Post')


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    the_post = Post.query.get_or_404(post_id)
    if the_post.author != current_user:
        abort(403)
    db.session.delete(the_post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
