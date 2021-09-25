import os
from flask import Flask, request, redirect, render_template
import glob


app = Flask(__name__)

userType = 'guest'          # guest / user / admin
## Login ::Temporary for prototype::
registered = {'admin.mumbai@adaniair.com':'admin.mumbai',
              'test.user@email.com': 'test.user'}
city = 'mumbai'


def reset_global():
    global userType
    global city
    userType = 'guest'
    city = 'mumbai'


def get_images(city):
    image_list = []
    for filename in glob.glob(f'static/img/{city}/carousel/*.jpg'): 
        image_list.append(filename)

    return image_list


@app.route('/', methods=['GET', 'POST'])
def index():

    carousel_images = get_images(city)
    print(carousel_images)
    return render_template('index.html', userType=userType, city=city, carousel_images=carousel_images)

@app.route('/shop-dine')
def shop_and_dine():
    return render_template('service-page.html', userType=userType, city=city)

@app.route('/cart')
def cart():
    if userType == 'guest':
        return render_template('restricted.html', userType=userType, city=city)
    return render_template('shopping-cart.html', userType=userType, city=city)

@app.route('/login',  methods=['GET', 'POST'])
def login():
    return render_template('login.html', userType=userType, city=city)

@app.route('/logout')
def logout():
    reset_global()
    return redirect("/")

@app.route('/register',  methods=['GET', 'POST'])
def signup():
    return render_template('registration.html', userType=userType, city=city)

@app.route('/feedback',  methods=['GET', 'POST'])
def feedback():
    return render_template('feedback.html', userType=userType, city=city)

@app.route('/suspicion',  methods=['GET', 'POST'])
def suspicion():
    return render_template('suspicious.html', userType=userType, city=city)

@app.route('/dine')
def dine():
    return render_template('dine.html', userType=userType, city=city)

@app.route('/payment',  methods=['GET', 'POST'])
def pay():
    return render_template('payment-page.html', userType=userType, city=city)

@app.route('/dash-admin',  methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard-admin.html', userType=userType)

@app.route('/menu',  methods=['GET', 'POST'])
def menu():
    return render_template('product-page.html', userType=userType, city=city)

@app.route('/mumbai')
def change_to_mumbai():
    global city
    city = 'mumbai'
    return redirect("/")

@app.route('/lucknow')
def change_to_lucknow():
    global city
    city = 'lucknow'
    return redirect("/")

@app.route('/ahmedabad')
def change_to_ahmedabad():
    global city
    city = 'ahmedabad'
    return redirect("/")

@app.route('/mangaluru')
def change_to_mangaluru():
    global city
    city = 'mangaluru'
    return redirect("/")

@app.route('/jaipur')
def change_to_jaipur():
    global city
    city = 'jaipur'
    return redirect("/")

@app.route('/guwahati')
def change_to_guwahati():
    global city
    city = 'guwahati'
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)