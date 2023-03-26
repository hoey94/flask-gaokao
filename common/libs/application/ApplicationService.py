import numpy as np
import pandas as pd

from common.models.application.YuCe import Yuce


class ApplicationService:

    @staticmethod
    def KNN(grade):
        data = pd.read_excel('预测成绩表_结果.xlsx')
        classify = data['classify']
        x = data[2022]
        k = 50
        distances = np.sqrt((x - grade) ** 2)
        from collections import Counter
        votes = Counter(classify[np.argpartition(distances, k)[:k]])
        return votes.most_common()[0][0]

    def getFirstList(self, grade, add_list):
        classify = int(self.KNN(grade+20))
        yuce_list = Yuce.query.filter_by(y_classify=classify).all()
        data_yuce_list = []
        for item in yuce_list:
            dic = item.to_dict()
            if dic['id'] in add_list:
                dic['active'] = True
            else:
                dic['active'] = False
            data_yuce_list.append(dic)
        return data_yuce_list

    def getMiddleList(self, grade, add_list):
        classify = int(self.KNN(grade))
        yuce_list = Yuce.query.filter_by(y_classify=classify).all()
        data_yuce_list = []
        for item in yuce_list:
            dic = item.to_dict()
            if dic['id'] in add_list:
                dic['active'] = True
            else:
                dic['active'] = False
            data_yuce_list.append(dic)
        return data_yuce_list

    def getLastList(self, grade, add_list):
        classify = int(self.KNN(grade-20))
        yuce_list = Yuce.query.filter_by(y_classify=classify).all()
        data_yuce_list = []
        for item in yuce_list:
            dic = item.to_dict()
            if dic['id'] in add_list:
                dic['active'] = True
            else:
                dic['active'] = False
            data_yuce_list.append(dic)
        return data_yuce_list
