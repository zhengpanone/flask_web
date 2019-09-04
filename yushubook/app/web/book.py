from flask import jsonify, request, render_template, flash
from app.lib.helper import is_isbn_or_key
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook
from app.forms.book import SearchForm
from app.view_models.trade import TradeInfo
from . import web
from app.view_models.book import BookViewModel, BookCollection
from flask_login import current_user
import json

# import json

__author__ = 'zhengpanone'


@web.route('/test2')
def test2():
    r = {
        'name': 'zhengpanone',
        'age': 28
    }
    r2 = {
        'name': '',
        'age': 18
    }
    return render_template('test.html', data=r, data2=r2)


@web.route('/test')
def test1():
    from app.lib.none_local import n
    print(n.v)
    n.v = 2
    print('===========================')
    print(getattr(request, 'v', None))
    setattr(request, 'v', 2)
    print('============================')
    return ''


# @web.route('/book/search/<q>/<page>')
@web.route('/book/search')
def search():
    # isbn isbn13 13个0-9的数字组成
    # q = request.args['q']
    # page = request.args['page']  # 不可变字典
    # a = request.args.to_dict()  # 不可变字典转换为可变字典
    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()

        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q, page)

        books.fill(yushu_book, q)
        # dict 序列化
        # API
        # return json.dumps(result),200,{'content-type':'application/json'}
        # jsonify() 序列化字典
        # return json.dumps(books, default=lambda o: o.__dict__)
    else:
        flash("搜索的关键字不符合要求，请重新输入关键字")  # 消息闪现
        # return jsonify(form.errors)

    return render_template('search_result.html', books=books, form=form)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_gifts = False
    has_in_wises = False
    # 取书籍详情数据
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)

    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_wises = True

    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()
    trade_gifts_model = TradeInfo(trade_gifts)
    trade_wishes_model = TradeInfo(trade_wishes)
    return render_template('book_detail.html',
                           book=book,
                           wishes=trade_wishes_model,
                           gifts=trade_gifts_model,
                           has_in_gifts=has_in_gifts,
                           has_in_wishs=has_in_wises)
