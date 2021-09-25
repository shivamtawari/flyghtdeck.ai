import pandas as pd
import glob

class HandleCity:
    def __init__(self, city=None):
        self.city = city

    def set_city(self, city):
        self.city = city

    def get_images(self, city=None):
        if city:
            self.set_city(city)

        image_list = []
        for filename in glob.glob(f'static/img/{self.city}/carousel/*.jpg'): 
            image_list.append(filename)

        return image_list

    def get_restaurants(self, city=None):
        if city:
            self.set_city(city)

        self.restaurants = pd.read_csv(f'static/data/restaurants_{self.city}.csv')

        return self.restaurants.values.tolist()[:2]
    
    def get_menu(self, restaurant):
        self.restaurantpic = self.restaurants.loc[self.restaurants.iloc[:,0]==restaurant].values.tolist()[0][1]
        menu = pd.read_csv(f'static/data/restaurants_{self.city}_menu.csv')
        return menu.loc[menu.iloc[:, 0]==restaurant].values.tolist()
