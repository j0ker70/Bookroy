from datetime import datetime
from flask import Blueprint, flash, redirect, url_for
from flask import render_template, request
from flask_login import login_required, current_user

from App import db
from App.main.forms import SearchForm, MessageForm
from App.models import Post, User, Message

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.datePosted.desc()).paginate(per_page=5, page=page)
    return render_template('home.html', books=posts)


@main.route('/about')
def about():
    return render_template('about.html', title='About')


@main.route('/search', methods=['GET', 'POST'])
def search():
    page = request.args.get('page', 1, type=int)
    form = SearchForm()
    posts = Post.query.order_by(Post.datePosted.desc()).paginate(per_page=5, page=page)
    if form.validate_on_submit():
        if form.book_name.data and form.max_price.data:
            posts = Post.query.filter_by(title=form.book_name.data).\
                filter(Post.price <= form.max_price.data).\
                order_by(Post.datePosted.desc()).\
                paginate(per_page=5, page=page)
        elif form.book_name.data:
            posts = Post.query.filter_by(title=form.book_name.data).\
                order_by(Post.datePosted.desc()).\
                paginate(per_page=5, page=page)
        elif form.max_price.data:
            posts = Post.query.filter(Post.price <= form.max_price.data).\
                order_by(Post.datePosted.desc()).\
                paginate(per_page=5, page=page)
        print(Post.query.all())
    elif request.method == 'GET':
        form.max_price.data = 10000
    return render_template('search.html', title='Search', form=form, books=posts)


@main.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(msg)
        db.session.commit()
        flash('Your message has been sent', 'success')
        return redirect(url_for('main.home', username=recipient))
    return render_template('send_message.html', title='Send Message',
                           form=form, recipient=recipient)


@main.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(
        Message.timestamp.desc()).paginate(per_page=5, page=page)
    next_url = url_for('main.messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('main.messages', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template('messages.html', messages=messages.items,
                           next_url=next_url, prev_url=prev_url, User=User)