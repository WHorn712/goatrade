import pandas as pd


class Accumulation:
    """Accumulation point"""
    def __init__(self, rates, dt_start, dt_end):
        self.point = 0
        self.calculate_accumulation_point(rates)
        self.dt_start = dt_start
        self.dt_end = dt_end

    def get_point(self):
        """Get the accumulation point"""
        return self.point

    def set_point(self, point):
        """Set the accumulation point"""
        self.point = point

    def calculate_accumulation_point(self, rates):
        """Calculates the main accumulation point in a Pandas DataFrame. It must mandatorily receive a Numpy ndarray;
        so, it goes into exception mode to handle a possible conversion error. If an error is reported,
        it returns zero. Otherwise, it configures the accumulation point of the object"""
        try:
            rates_frame = pd.DataFrame(rates)
            close = list(rates_frame['close'])
            low = list(rates_frame['low'])
            hig = list(rates_frame['high'])

            #Create a list in order of all possible points of the DataFrame
            points = []
            for i in range(len(close)):
                point = low[i]
                points.append(point)
                while (point <= hig[i]):
                    point += 0.00001
                    points.append(point)

            # Calculation of the accumulation point
            self.point = max(set(points), key=points.count)

        except:
            self.point = 0















