from flask import Flask, render_template, request, make_response, redirect, url_for, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from my_database import DataBase, UserLogin

app = Flask(__name__)
app.config['SECRET_KEY'] = '22d6g4kgc3f8ade0fr65d4bf1rms4e56c549380da3e7'
login_manager = LoginManager(app)
login_manager.login_view = 'register_page'
db = DataBase()


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, db)


@app.route('/')
def hello_world():  # put application's code here
    return redirect(url_for('main_page'))


@app.route('/main_page')
def main_page():
    products = db.get_all_product()
    context = {
        'title': 'Remova store',
        'products': products
    }
    return render_template('main_page.html', **context)


@app.route('/product/<int:id>')
def product(id):
    product = db.get_product_by_id(id)
    context = {
        'product': product,
    }

    return render_template('product.html', **context)


@app.route('/add_product')
def add_product():
    return render_template('add_product.html')


@app.route('/product/<int:id>/edit')
@login_required
def edit_product(id):
    user = db.get_user_by_id(current_user.get_id)
    if user[6]:
        product = db.get_product_by_id(id)
        context = {
            'product': product,
        }
        return render_template('edit_product.html', **context)
    return redirect(url_for('product', id=id))


@app.route('/product/<int:id>/delete', methods=['GET'])
@login_required
def delete_product(id):
    user = db.get_user_by_id(current_user.get_id)
    if user[6]:
        db.delete_product_by_id(id)
        return redirect(url_for('main_page'))
    return redirect(url_for('product', id=id))


@app.route('/profile')
@login_required
def profile_page():
    user = db.get_user_by_id(current_user.get_id())
    context = {
        'title': 'Profile',
        'first_name': user[1],
        'last_name': user[2],
        'email': user[3],
        'phone_num': user[4],
    }
    return render_template('profile_page.html', **context)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_page'))


@app.route('/cart')
@login_required
def cart_page():
    context = {
        'title': 'Cart'
    }
    return render_template('main_page.html', **context)


@app.route('/orders')
@login_required
def orders_page():
    context = {
        'title': 'Orders',
        'orders': db.get_all_orders(current_user.get_id())
    }
    return render_template('orders_page.html', **context)


@app.route('/favourite')
@login_required
def favourite_page():
    context = {
        'title': 'Favourite',
        'products': db.get_all_favourites(current_user.get_id())
    }
    return render_template('favourite_page.html', **context)


@app.route('/add_to_favourite/<int:product_id>')
@login_required
def add_to_favourite(product_id):
    db.add_to_favourite(current_user.get_id(), product_id)
    url_from = request.args.get('url_from')
    return redirect(url_from)


@app.route('/delete_from_favourite/<int:product_id>')
@login_required
def delete_from_favourite(product_id):
    db.delete_from_favourite(current_user.get_id(), product_id)
    url_from = request.args.get('url_from')
    return redirect(url_from)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone_num = request.form.get('phone_num')
        password = request.form.get('password')
        if db.check_user_email_phone(phone_num, email):
            print('Have user with this data')
        else:
            db.register_user(first_name, last_name, email, phone_num, password)
            user = db.get_user_by_email(email)
            user_login = UserLogin().create(user)
            login_user(user_login, remember=True)
            return redirect('main_page')

    context = {
        'title': 'Register'
    }
    return render_template('register_page.html', **context)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form.get('email')
        phone_num = request.form.get('phone_num')
        password = request.form.get('password')
        user = db.get_user_by_email(email)
        if user and user[4] == phone_num and user[5] == password:
            user_login = UserLogin().create(user)
            login_user(user_login, remember=True)
            return redirect('main_page')
        else:
            print("Wrong password/email/phone")

    context = {
        'title': 'Log In'
    }
    return render_template('login_page.html', **context)


@app.route('/gender/<string:gender>')
def sex_page(gender):
    context = {
        'title': gender
    }
    return render_template('main_page.html', **context)


if __name__ == '__main__':
    app.run()
