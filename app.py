import os
from flask import Flask, request, redirect, render_template
from multi_city import HandleCity
from recommendation import RecommendationEngine
from extract_keys import Extractor
from model import Model


userType = 'guest'          # guest / user / admin
## Login ::Temporary for prototype::
registered = {'admin.mumbai@adaniair.com':'admin.mumbai',
              'test.user1@email.com': 'test.user1',
              'test.user2@email.com': 'test.user2'}
loggedIn = None
history = {'test.user1@email.com': [],
           'test.user2@email.com': ['Cheese Melt Paneer Wrap', 'Malted Chocolate Fudge Ice cream'],
           }
city = 'mumbai'

app = Flask(__name__)
city_handler = HandleCity(city)
recommender = RecommendationEngine()
extractor = Extractor()
model = Model()

UPLOAD_FOLDER = os.path.join('static', 'img', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

corpus = extractor.clean()
extractor.set_city(city)
corpus = extractor.clean()
uni = extractor.single_imp(corpus)
bi = extractor.double_imp(corpus)
tri = extractor.triple_imp(corpus)
quad = extractor.four_imp(corpus)

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
    global loggedIn

    email = request.form.get("email")
    password = request.form.get("password")

    for em, pas in registered.items():
        if (email==em and password==pas):
            if email[-12:]=='adaniair.com':
                userType = 'admin'
                city = email.split('.')[1].split('@')[0]
                print(city)
            else:
                userType = 'user'
            loggedIn = email
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
    global uni
    global bi
    global tri
    global quad

    if 0:
        extractor.set_city(city)
        corpus = extractor.clean()
        uni = extractor.single_imp(corpus)
        bi = extractor.double_imp(corpus)
        tri = extractor.triple_imp(corpus)
        quad = extractor.four_imp(corpus)


    return render_template('dashboard-admin.html', userType=userType, city=city, uni=uni, bi=bi, tri=tri, quad=quad)

@app.route('/today')
def today():
    global userType
    global city
    global extractor

    corpus = extractor.clean(typ='today')
    print('>>>')
    print('enter')
    print('<<<')
    uni = extractor.single_imp(corpus, city)
    print('>>>')
    print('exit')
    print('<<<')
    bi = extractor.double_imp(corpus, city)
    tri = extractor.triple_imp(corpus, city)
    quad = extractor.four_imp(corpus, city)

    print(uni, bi, tri, quad)

    return render_template('dashboard-admin.html', userType=userType, city=city, uni=uni, bi=bi, tri=tri, quad=quad)

@app.route('/week')
def week():
    global userType
    global city
    global extractor

    corpus = extractor.clean(typ='week')
    uni = extractor.single_imp(corpus, city)
    bi = extractor.double_imp(corpus, city)
    tri = extractor.triple_imp(corpus, city)
    quad = extractor.four_imp(corpus, city)

    return render_template('dashboard-admin.html', userType=userType, city=city, uni=uni, bi=bi, tri=tri, quad=quad)

@app.route('/month')
def month():
    global userType
    global city
    global extractor

    corpus = extractor.clean(typ='month')
    uni = extractor.single_imp(corpus, city)
    bi = extractor.double_imp(corpus, city)
    tri = extractor.triple_imp(corpus, city)
    quad = extractor.four_imp(corpus, city)

    print(uni, bi, tri, quad)

    return render_template('dashboard-admin.html', userType=userType, city=city, uni=uni, bi=bi, tri=tri, quad=quad)

def minus(lst1, lst2):
    lst3 = [value for value in lst1 if value not in lst2]
    return lst3

@app.route('/menu',  methods=['GET', 'POST'])
def menu(restaurant=None):
    global userType
    global city

    menu = city_handler.get_menu(restaurant)
    recommended = []
    if loggedIn:
        hist = history[loggedIn]
        print(hist)
        if len(hist)==0:
            recommended = city_handler.get_bestsellers(restaurant)
        else:
            product = []
            for item in hist:
                for detailed_item in menu:
                    if item in detailed_item:
                        product.append(detailed_item)
            
            recommended = recommender.get_similarity(product[-1], menu, num=2)
            print(recommended)
    else:
        recommended = []

    menu = minus(menu, recommended)
    
    return render_template('product-page.html', userType=userType, city=city, restaurant=restaurant, menu=menu, recommended=recommended)

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

@app.route('/prediction')
def prediction(img_path=None, predicted=None):

    return render_template('prediction.html', userType=userType, city=city, img_path=img_path, predicted=predicted)

@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        img_path = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'], f.filename)
        f.save(img_path)
        predicted = round(model.predict(img_path), 5)
        img_path = 'static\\img\\uploads\\'+f.filename
        return prediction(img_path, predicted)



if __name__ == '__main__':
    app.run(debug=True)