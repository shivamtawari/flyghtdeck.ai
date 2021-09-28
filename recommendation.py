from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

class RecommendationEngine:
    def __init__(self,):
        self.cv = CountVectorizer() 

    def find_title_from_index(self, index):
        return self.menu[self.menu.index == index]

    def find_index_from_title(self, item):
        return self.menu[self.menu.iloc[:,1] == item[1]].index[0]

    def get_similarity(self, product, menu, num=1):
        self.product = product
        self.menu = pd.DataFrame(menu)

        temp_menu = []
        for m in self.menu.values.tolist():
            t_m = [str(i) for i in m]
            t_m = ' '.join(t_m)
            temp_menu.append(t_m)
        temp_prod = [str(i) for i in self.product]
        temp_prod = ' '.join(temp_prod)

        count_matrix = self.cv.fit_transform(temp_menu)
        cosine_sim = cosine_similarity(count_matrix)

        item_index = self.find_index_from_title(self.product)

        similar_items = list(enumerate(cosine_sim[item_index]))
        sorted_similar_items = sorted(similar_items,key=lambda x:x[1],reverse=True)[1:]

        i=0
        recommended = []
        for element in sorted_similar_items:
            recommended.append(self.find_title_from_index(element[0]).values.tolist()[0])
            i=i+1
            if i>=num:
                break

        return recommended