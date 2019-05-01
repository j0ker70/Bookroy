from flask import Blueprint
from flask import render_template, request

from App.main.forms import SearchForm
from App.models import Post

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
    return render_template('search.html', title='Search', form=form, books=posts)
