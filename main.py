#import Previsao
#import noticias
#import indicadores

import DataRates as dr
import MetaTrader5 as mt5
import pytz
from datetime import datetime


mt5.initialize()
timezone = pytz.timezone("Etc/UTC")
utc_from = datetime(2024, 7, 2, hour=2, minute=35, tzinfo=timezone)
utc_to = datetime(2024, 7, 3, hour=5, minute=45, tzinfo=timezone)
rates = mt5.copy_rates_range("EURUSD", mt5.TIMEFRAME_M5, utc_from, utc_to)
briga = dr.Accumulation(rates=rates, dt_start=utc_from, dt_end=utc_to)
print(briga.point)
mt5.shutdown()

#noticias.main_news()

#print("TESTE") #TODO: PRECISO FAZER ISSO E AQUILO TESTE

#screen = interface.Screen()

#print()