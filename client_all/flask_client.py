from flask import Flask, send_file, render_template, url_for, redirect
import sys

app = Flask(__name__)


# czx
@app.route('/index')
def index():
    # 首页
    return render_template('index.html')


# czx
@app.route('/about')
def about():
    # 关于我们
    return render_template('about-us.html')


# @app.route('/aaaa')
# def aaaa():
#     return render_template('tests.html')


# czx
@app.route('/blog')
def show_blog_list():
    # 显示博客/文章列表
    return render_template('blog-list.html')


# czx
@app.route('/cart')
def show_cart():
    # 购物车页面
    return render_template('cart.html')


@app.route('/checkout')
def checkout():
    # 结算页面
    return render_template('checkout.html')


@app.route('/contact')
def contact():
    # 联系我们 / 提交意见
    return render_template('contact-us.html')


@app.route('/legal')
def legal():
    # 相关法律
    return render_template('legal.html')


# wwt
@app.route('/login')
def login():
    # 登陆
    return render_template('login.html')


@app.route('/single')
def single():
    # 具体文章
    return render_template('post-single_b.html')


@app.route('/product/<p_id>')
def product(p_id):
    # 具体商品页
    return render_template('product-single.html')


# wwt
@app.route('/register')
def register():
    # 注册
    return render_template('register.html')


# qxl
@app.route('/shop')
def shopping():
    # 商品列表
    return render_template('shop-v4.html')


# qxl
@app.route('/wishlist')
def wishlist():
    # 愿望列表
    return render_template('wishlist.html')


@app.route('/revamp')
def revamp():
    # 修改用户信息
    return render_template('revamp.html')


@app.route('/t1')
def test_api_1():
    # 测试接口
    return render_template('ztest_1.html')


@app.route('/t2')
def test_api_2():
    # 测试接口
    return render_template('404.html')


@app.route('/')
def homepage():
    # 重定向至index
    return redirect(url_for('index'))


@app.route('/goods/select')
def goods_select():
    return render_template('goods_select.html')

@app.route('/Myindent')
def my_indent():
    return render_template('Myindent.html')

@app.route('/zf')
def zf():
    return render_template('zf.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)
