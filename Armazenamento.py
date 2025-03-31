

import MetaTrader5 as mt5
from datetime import datetime
import pytz
import pandas as pd


from sklearn.neighbors import KNeighborsClassifier
import numpy as np

class Movement:
    """Class that represents a specific movement, with beginning and end, of the financial market."""

    def __init__(self,month1, day1, hour1, minute1, month2, day2, hour2, minute2):
        self.year = 2023
        self.month1 = month1
        self.day1 = day1
        self.hour1 = hour1
        self.minute1 = minute1
        self.month2 = month2
        self.day2 = day2
        self.hour2 = hour2
        self.minute2 = minute2


    def get_close(self):
        """Returns a list of movement close points"""
        mt5.initialize()
        timezone = pytz.timezone("Etc/UTC")
        utc_from = datetime(year=self.year, month=self.month1, day=self.day1, hour=self.hour1, minute=self.minute1, tzinfo=timezone)
        utc_to = datetime(year=self.year, month=self.month2, day=self.day2, hour=self.hour2, minute=self.minute2, tzinfo=timezone)
        rates = mt5.copy_rates_range("EURUSD", mt5.TIMEFRAME_M5, utc_from, utc_to)

        mt5.shutdown()

        rates_frame = pd.DataFrame(rates)

        return list(rates_frame['close'])





class Storage:
    """Data collection and training for machine learning"""

    @staticmethod
    def main_():
        """Main of class"""

        knn, max_len = Storage.training_model()
        type_move, probability = Storage.get_classification_new_model(knn,
                                                    Movement(11, 29, 16, 5, 11, 29, 17, 0).get_close(), max_len=max_len)
        print(type_move, probability)


    @staticmethod
    def training_model():
        """Model training with data collected from the financial market"""

        #Collects specific data from the 3 movement patterns -> leg 1 leg 2 of hight / leg 1 leg 2 of low
        #/ lateralization
        high_list = [Movement(12, 14, 15, 30, 12, 14, 16, 30).get_close(),
                     Movement(12, 14, 14, 35, 12, 14, 15, 25).get_close(),
                     Movement(12, 12, 9, 10, 12, 12, 10, 0).get_close(),
                     Movement(11, 28, 16, 30, 11, 28, 16, 55).get_close(),
                     Movement(11, 27, 2, 0, 11, 27, 3, 20).get_close()]
        low_list = [Movement(12, 12, 14, 25, 12, 12, 15, 15).get_close(),
                    Movement(12, 1, 15, 35, 12, 1, 16, 0).get_close(),
                    Movement(11, 30, 19, 25, 11, 30, 20, 5).get_close(),
                    Movement(11, 29, 20, 15, 11, 29, 20, 55).get_close(),
                    Movement(11, 29, 7, 55, 11, 29, 9, 10).get_close()]
        lateralization_list = [Movement(12, 5, 11, 5, 12, 5, 12, 20).get_close(),
                               Movement(12, 4, 1, 45, 12, 4, 3, 20).get_close(),
                               Movement(12, 1, 9, 40, 12, 1, 10, 30).get_close(),
                               Movement(12, 1, 6, 35, 12, 1, 8, 35).get_close(),
                               Movement(12, 1, 2, 10, 12, 1, 3, 20).get_close()]

        #the following list contains all the movements of the initial samples, already classified
        first_samples = [high_list[0], high_list[1], high_list[2], high_list[3], high_list[4], low_list[0], low_list[1],
                         low_list[2], low_list[3], low_list[4], lateralization_list[0], lateralization_list[1],
                         lateralization_list[2], lateralization_list[3], lateralization_list[4]]

        #max_len contains the maximum number of candles from one movement of all initial samples
        max_len = max(len(first_sample) for first_sample in first_samples)

        #all sample lists smaller than the largest sample are padded with 0 so they are the same size
        first_samples = [first_sample + [0] * (max_len - len(first_sample)) for first_sample in first_samples]

        #x array numpy with all initial samples
        #y array numpy with the classification of all initial samples
        x = np.array(first_samples)
        y = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2])

        #creating the model knn
        knn = KNeighborsClassifier(n_neighbors=3)

        #training the model with the initial samples
        knn.fit(x, y)

        return knn, max_len

    @staticmethod
    def get_classification_new_model(knn, new_movement, max_len=20):
        """Classifies 'new_movement' database, according to training 'knn' passed as a parameter"""

        #shapes the new list to the same size as the initial samples
        if max_len >= len(new_movement):
            new_movement = [new_movement + [0] * (max_len - len(new_movement))]
        else:
            new_movement = new_movement[0:max_len]

        #new_movement array numpy
        new_movement = np.array(new_movement)

        #Using the trained model to predict the pattern of the new list
        prediction = knn.predict(new_movement)

        #type_move
        type_move = prediction[0]

        last_number = 0
        c = 0
        for i in new_movement[0]:
            c -= 1
            if new_movement[0][c] > 0:
                last_number = new_movement[0][c]
                break

        #checks whether the movement is bullish or bearish
        if type_move == 0 or type_move == 1:
            if new_movement[0][0] < last_number:
                type_move = 1
            else:
                type_move = 0

        probability = knn.predict_proba(new_movement)

        return type_move, probability

    @staticmethod
    def coleta_padrao_em_movimento_maior():

        lista = Movement(11, 28, 18, 15, 11, 29, 5, 30).get_close()






