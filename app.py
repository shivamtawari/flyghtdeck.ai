import os
from flask import Flask, request, redirect, render_template
from multi_city import HandleCity


userType = 'user'          # guest / user / admin
## Login ::Temporary for prototype::
registered = {'admin.mumbai@adaniair.com':'admin.mumbai',
              'test.user@email.com': 'test.user'}
city = 'mumbai'


app = Flask(__name__)
city_handler = HandleCity(city)


def reset_global():
    global userType
    global city
    userType = 'guest'
    city = 'mumbai'


@app.route('/', methods=['GET', 'POST'])
def index():
    global userType
    global city

    carousel_images = city_handler.get_images(city)
    print(carousel_images)
    return render_template('index.html', userType=userType, city=city, carousel_images=carousel_images)

@app.route('/shop-dine')
def shop_and_dine():
    global userType
    global city

    return render_template('service-page.html', userType=userType, city=city)

@app.route('/cart')
def cart():
    global userType
    global city

    if userType == 'guest':
        return render_template('restricted.html', userType=userType, city=city)
    return render_template('shopping-cart.html', userType=userType, city=city, order=False)

@app.route('/login',  methods=['GET', 'POST'])
def login():
    global userType
    global city

    email = request.form.get("email")
    password = request.form.get("password")

    for em, pas in registered.items():
        if (email==em and password==pas):
            if email[-12:]=='adaniair.com':
                userType = 'admin'
            else:
                userType = 'user'
            return redirect("/")
    ## Wrong EmailId or Pass
    return render_template('login.html', userType=userType, city=city)

@app.route('/logout')
def logout():
    reset_global()
    return redirect("/")

@app.route('/register',  methods=['GET', 'POST'])
def signup():
    global userType
    global city

    return render_template('registration.html', userType=userType, city=city)

@app.route('/feedback',  methods=['GET', 'POST'])
def feedback():
    global userType
    global city

    return render_template('feedback.html', userType=userType, city=city)

@app.route('/suspicion',  methods=['GET', 'POST'])
def suspicion():
    global userType
    global city

    return render_template('suspicious.html', userType=userType, city=city)

@app.route('/dine')
def dine():
    global userType
    global city
    restaurants = city_handler.get_restaurants(city)
    return render_template('dine.html', userType=userType, city=city, restaurants=restaurants)

@app.route('/payment',  methods=['GET', 'POST'])
def pay():
    global userType
    global city

    return render_template('payment-page.html', userType=userType, city=city)

@app.route('/dash-admin',  methods=['GET', 'POST'])
def dashboard():
    global userType
    global city

    return render_template('dashboard-admin.html', userType=userType)

@app.route('/menu',  methods=['GET', 'POST'])
def menu(restaurant=None):
    global userType
    global city

    menu = city_handler.get_menu(restaurant)
    return render_template('product-page.html', userType=userType, city=city, restaurant=restaurant, menu=menu)

@app.route('/mumbai')
def change_to_mumbai():
    global city
    city = 'mumbai'
    city_handler.set_city(city)
    return redirect("/")

@app.route('/lucknow')
def change_to_lucknow():
    global city
    city = 'lucknow'
    city_handler.set_city(city)
    return redirect("/")

@app.route('/ahmedabad')
def change_to_ahmedabad():
    global city
    city = 'ahmedabad'
    city_handler.set_city(city)
    return redirect("/")

@app.route('/mangaluru')
def change_to_mangaluru():
    global city
    city = 'mangaluru'
    city_handler.set_city(city)
    return redirect("/")

@app.route('/jaipur')
def change_to_jaipur():
    global city
    city = 'jaipur'
    city_handler.set_city(city)
    return redirect("/")

@app.route('/guwahati')
def change_to_guwahati():
    global city
    city = 'guwahati'
    city_handler.set_city(city)
    return redirect("/")

@app.route('/<tag>')
def restaurant(tag):
    global city
    return menu(tag.title())

@app.route('/<item>_<price>')
def buynow(item, price):
    # return item + ' ' + price
    return render_template('shopping-cart.html', userType=userType, city=city, item=item, price=price, restaurantpic=city_handler.restaurantpic, order=True)

@app.route('/sucess')
def pay_successful():
    return render_template('pay-successful.html', userType=userType, city=city)

if __name__ == '__main__':
    app.run(debug=True)