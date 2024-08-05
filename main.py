import time
import requests
import json
from colorama import Fore, Style
import warnings
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import random
import re
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from tabulate import tabulate
from binance.client import Client
from pmdarima import auto_arima
import traceback
import openpyxl
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.ensemble import VotingRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor
from sklearn.svm import SVR
from sklearn.linear_model import ElasticNet
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import GridSearchCV

api_key = 'RjCgL26lL8GoDagHA4Pb2wFC9414Oenhp5oGOfQMJrCJbWpU9yBtMPofuNAm3cXL'
api_secret = 'SGNelarbzwvaFVRpQXhfeX9EPbLFRYIIKi8B2PloNTepvT6Q12LIYsCXbgkn8DGF'


end = datetime.now() + timedelta(days=1)
end = end.strftime("%Y-%m-%d")

startdate = datetime.now() - timedelta(days=980)
startdate = startdate.strftime("%Y-%m-%d")

def send_telegram_message(message):
    bot_token = '6490925202:AAFoJrRj8l428Q1P8czlUfcoeTEF0dFlbZ4'
    chat_id = '@dorecast'
    message = str(message)
    print(Fore.GREEN + message + Style.RESET_ALL)

    cleaned_message = re.sub(r'\[|\]', '', message)
    cleaned_message2 = re.sub(r'\'|\,', '', cleaned_message)
    table = tabulate([cleaned_message2.split(',')], headers="firstrow")
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={table}"

    response = requests.get(url)
    return response
def send_telegram_file(file_path):
    bot_token = '6490925202:AAFoJrRj8l428Q1P8czlUfcoeTEF0dFlbZ4'
    chat_id = '@dorecast'
    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"

    with open(file_path, 'rb') as file:
        response = requests.post(url, data={'chat_id': chat_id}, files={'document': file})

    return response


def bisto():
    # Web sayfasının URL'si
    url = 'https://www.kap.org.tr/tr/bist-sirketler'

    # Web sayfasını iste
    response = requests.get(url)
    html_content = response.content

    # BeautifulSoup ile HTML içeriğini parse et
    soup = BeautifulSoup(html_content, 'html.parser')

    # "comp-cell _04 vtable" sınıfına sahip elemanları bul
    comp_cells = soup.find_all('div', class_='comp-cell _04 vtable')

    # Her bir "comp-cell _04 vtable" elemanının altındaki <a> etiketlerinin içeriğini al
    text_list = []
    for cell in comp_cells:
        links = cell.find_all('a')
        for link in links:
            text_list.append(link.text)

    # Sonucu yazdır
    return text_list

bist_list=bisto()
bist=[]

for item in bist_list:
    parts = item.split(',')  # Split each item by comma
    if len(parts) >= 1:
        first_part = parts[0].strip()  # Get the first part and remove any leading/trailing spaces
        first_part = first_part[0].upper() + first_part[1:]  # Convert first character to uppercase
        bist.append(first_part + ".IS")


def crypto():
    from binance.client import Client

    client = Client(api_key, api_secret)
    exchange_info = client.get_exchange_info()
    c=[]
    for s in exchange_info['symbols']:
        #end with USDT
        if s['symbol'].endswith('USDT'):
            c.append(s['symbol'].upper())
    cr = []
    for s in c:
        new_symbol = s.replace('USDT', '-USD')

        if new_symbol.endswith('DOWN-USD'):
            pass
        elif new_symbol.endswith('UP-USD'):
            pass
        elif new_symbol.endswith('BEAR-USD'):
            pass
        elif new_symbol.endswith('BULL-USD'):
            pass
        else:
            cr.append(new_symbol)

    return cr

cr=crypto()
liste=cr+bist
print(str("kripto: "+str(len(cr))))
print(str("bist: "+str(len(bist))))
def newthe(liste):
    sepet = pd.DataFrame(columns=["symbol","close","difference",
                                  "forecast","date",
                                  "hedef_tarih","rmse"])
    estimators=150
    süre=7

    beklenen_sinyal=3
    randomstate=42
    sell=pd.DataFrame(columns=["symbol","close","date"])
    say1 = 0

    for symbol in liste:
        say1 += 1

        if symbol.endswith(".IS"):
            beklenen_degisim = 15
        else:
            beklenen_degisim = 20
        print(Fore.CYAN + str(say1)+"/"+str(len(liste))+" "+symbol+" "+ Style.RESET_ALL)
        try:

            data = yf.download(symbol, start=startdate, progress=False, interval='1d', end=end)
            data['close'] = data['Close']
            ortalama = data['close'].mean()

            son_tarih=datetime.now()-timedelta(days=6)


            if son_tarih < data.index[-1] < datetime.now():
                pass
            else:
                print("tarih hatası")
                print(data.index[-1])
                continue
            def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
                data['EMA12'] = data['close'].ewm(span=short_window, adjust=False).mean()
                data['EMA26'] = data['close'].ewm(span=long_window, adjust=False).mean()
                data['MACD'] = data['EMA12'] - data['EMA26']
                data['Signal Line'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
                data['MACD Signal'] = np.where(data['MACD'] > data['Signal Line'], 1, -1)
            def calculate_rsi(data, window=14):
                delta = data['close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
                rs = gain / loss
                data['RSI'] = 100 - (100 / (1 + rs))
                data['RSI Signal'] = np.where(data['RSI'] < 30, 1, np.where(data['RSI'] > 70, -1, 0))
            def calculate_sma(data, short_window=50, long_window=200):
                data['SMA50'] = data['close'].rolling(window=short_window).mean()
                data['SMA200'] = data['close'].rolling(window=long_window).mean()
                data['SMA Signal'] = np.where(data['SMA50'] > data['SMA200'], 1, -1)
            def calculate_bollinger_bands(data, window=20):
                data['SMA20'] = data['close'].rolling(window=window).mean()
                data['BB_upper'] = data['SMA20'] + 2 * data['close'].rolling(window=window).std()
                data['BB_lower'] = data['SMA20'] - 2 * data['close'].rolling(window=window).std()
                data['BB Signal'] = np.where(data['close'] > data['BB_upper'], -1,
                                             np.where(data['close'] < data['BB_lower'], 1, 0))
            def calculate_EMA(data):
                data['EMA20'] = data['close'].ewm(span=20, adjust=False).mean()
                data['EMA120'] = data['close'].ewm(span=120, adjust=False).mean()
                data['EMA Signal'] = np.where(data['EMA20'] > data['EMA120'], 1, -1)
            def calculate_indicators(data):
                calculate_macd(data)
                calculate_rsi(data)
                calculate_sma(data)
                calculate_bollinger_bands(data)
                calculate_EMA(data)
            def generate_signals(data):
                data['Signal'] = data[['MACD Signal', 'RSI Signal', 'SMA Signal', 'BB Signal','EMA Signal']].sum(axis=1)

            calculate_indicators(data)
            generate_signals(data)
            if data['Signal'].iloc[-1] >=beklenen_sinyal:
                data.fillna(0, inplace=True)
                def create_lagged_features(data, lag=süre):
                    df = data.copy()
                    for i in range(1, lag + 1):
                        df[f'lag_{i}'] = df['close'].shift(i)
                    return df

                data_with_lags = create_lagged_features(data)
                data_with_lags.dropna(inplace=True)
                X = data_with_lags.drop(['close', 'Signal Line', 'MACD Signal', 'RSI Signal',
                                         'SMA Signal','BB Signal', 'EMA Signal', 'Signal'],axis=1)
                y = data_with_lags['close']
                X_train, X_test, y_train, y_test = X.iloc[:-süre], X.iloc[-süre:], y.iloc[:-süre], y.iloc[-süre:]

                models = {
                    'rf': RandomForestRegressor(n_estimators=estimators, random_state=42),
                    'gb': GradientBoostingRegressor(n_estimators=estimators, learning_rate=0.1, max_depth=3,
                                                    random_state=42),
                    'ab': AdaBoostRegressor(n_estimators=estimators, learning_rate=1.0, random_state=42),
                    'xgb': XGBRegressor(n_estimators=estimators, learning_rate=0.1, max_depth=6, random_state=42,
                                        verbosity=0),
                    'lgbm': LGBMRegressor(n_estimators=estimators, learning_rate=0.05, random_state=42, verbosity=-1)
                }


                ensemble_model = VotingRegressor(estimators=[(name, model) for name, model in models.items()])

                # Ensemble modelini eğit
                ensemble_model.fit(X_train, y_train)


                future_predictions = []
                last_known_features = X_test.iloc[-1].values
                for i in range(süre):
                    prediction = ensemble_model.predict(last_known_features.reshape(1, -1))[0]
                    future_predictions.append(prediction)

                    # Gecikmeli özellikleri güncelleyin
                    last_known_features = np.roll(last_known_features, -1)
                    last_known_features[-1] = prediction
                beklenen_rmse=ortalama/(ortalama*ortalama)
                y_pred = ensemble_model.predict(X_test)
                rmse = np.sqrt(mean_squared_error(y_test, y_pred))

                seventh_day_prediction = future_predictions[-1]
                if rmse > beklenen_rmse or rmse > 0.1:
                    print(Fore.RED + "BEKLENEN RMSE: " + str(beklenen_rmse) + Style.RESET_ALL)
                    print(Fore.RED +symbol+ " YÜKSEK RMSE: " + str(rmse) + Style.RESET_ALL)
                elif rmse <= beklenen_rmse or rmse <=0.1:
                    if seventh_day_prediction > data[['close']].tail(1).values[0][0]:
                        difference_percent=((seventh_day_prediction-data[['close']].tail(1).values[0][0])/data[['close']].tail(1).values[0][0])*100
                        if difference_percent>beklenen_degisim:
                            print(Fore.GREEN + "Değişim oranı: " + str(difference_percent) + "%" + Style.RESET_ALL)
                            print(Fore.GREEN + symbol + Style.RESET_ALL)
                            hedef_tarih=(datetime.now()+timedelta(days=süre)).strftime("%d.%m.%Y")
                            add_data=pd.DataFrame({'symbol':[symbol],
                                                   'close':[data[['close']].tail(1).values[0][0]],
                                                   'difference':[difference_percent],
                                                   'forecast':[seventh_day_prediction],
                                                   'date':[datetime.now().strftime("%d.%m.%Y")],
                                                   'hedef_tarih':[hedef_tarih],
                                                   'rmse':[rmse]})
                            add_data = add_data.dropna(axis=1, how='all')
                            sepet=pd.concat([sepet,add_data],ignore_index=True)

                        else:
                            print(Fore.RED + "Değişim oranı yetersiz: " + str(difference_percent) + "%" + Style.RESET_ALL)
                    else:
                        print(Fore.RED + symbol+" yetersiz .....değişim : "+str(seventh_day_prediction-data[['close']].tail(1).values[0][0]) + Style.RESET_ALL)
                else:
                    print(Fore.RED + "BEKLENEN RMSE: " + str(beklenen_rmse) + Style.RESET_ALL)
                    print(Fore.RED + symbol + " YÜKSEK RMSE: " + str(rmse) + Style.RESET_ALL)
            elif data['Signal'].iloc[-1] <=-3:
                print(Fore.RED + symbol + " Düşecek!!! " + Style.RESET_ALL)

                add_data_sell=pd.DataFrame({'symbol':[symbol],'close':[data[['close']].tail(1).values[0][0]],'date':[datetime.now().strftime("%d.%m.%Y")]})
                sell = sell.dropna(axis=1, how='all')
                add_data_sell = add_data_sell.dropna(axis=1, how='all')
                sell=pd.concat([sell,add_data_sell],ignore_index=True)
            else:
                print(Fore.RED + symbol + " sinyal gücü!  : " +str(data['Signal'].iloc[-1])+ Style.RESET_ALL)


        except Exception as e:
            print(e)

    file='buy_list.xlsx'
    old_data=pd.read_excel(file)
    sepet=sepet.sort_values(by='difference', ascending=False)
    sepet.dropna()
    old_data.dropna()
    buylist = pd.concat([old_data, sepet], ignore_index=True)
    send_telegram_message("Buy sinyali verenler: " )
    send_telegram_message(str(sepet))
    send_telegram_message("Sell sinyali verenler: " + str(sell))
    #make an excel
    df = pd.DataFrame(buylist)
    df.sort_values(by='difference', ascending=False)
    df.to_excel('buy_list.xlsx',index=False,engine='openpyxl')
    dfsell=pd.DataFrame(sell)
    dfsell.to_excel('sell_list.xlsx')
    send_telegram_file('sell_list.xlsx')
    send_telegram_file('buy_list.xlsx')

def gpt():
    import matplotlib.pyplot as plt
    from statsmodels.tsa.arima.model import ARIMA
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    from sklearn.preprocessing import MinMaxScaler

    for symbol in liste:

        def load_data(symbol, start, end):
            data = yf.download(symbol, start=start, end=end, interval='1d', progress=False)
            data['close'] = data['Close']
            return data

        # Veri hazırlığı
        def preprocess_data(df):
            scaler = MinMaxScaler(feature_range=(0, 1))
            scaled_data = scaler.fit_transform(df[['close']].values)
            return scaled_data, scaler

        # ARIMA modeli oluşturma ve tahmin yapma
        def arima_forecast(train_data):
            model = ARIMA(train_data, order=(5, 1, 0))
            model_fit = model.fit()
            forecast = model_fit.forecast(steps=30)
            return forecast

        # SARIMA modeli oluşturma ve tahmin yapma
        def sarima_forecast(train_data):
            model = SARIMAX(train_data, order=(5, 1, 0), seasonal_order=(1, 1, 1, 30))
            model_fit = model.fit()
            forecast = model_fit.forecast(steps=30)
            return forecast

        # Tahminleri birleştirme
        def combined_forecast(arima_forecast, sarima_forecast):
            combined = (arima_forecast + sarima_forecast) / 2
            return combined

        # Ana fonksiyon
        def main():
            symbol = 'BTC-USD'  # Kripto sembolü
            start = '2020-01-01'  # Başlangıç tarihi
            end = '2023-12-31'  # Bitiş tarihi

            df = load_data(symbol, start, end)
            scaled_data, scaler = preprocess_data(df)

            train_data = scaled_data[:int(len(scaled_data) * 0.8)]
            test_data = scaled_data[int(len(scaled_data) * 0.8):]

            arima_forecast = arima_forecast(train_data)
            sarima_forecast = sarima_forecast(train_data)

            forecast = combined_forecast(arima_forecast, sarima_forecast)
            forecast = scaler.inverse_transform(forecast.reshape(-1, 1))

            plt.plot(df.index[-len(forecast):], forecast, label='Tahmin')
            plt.plot(df.index, df['close'], label='Gerçek')
            plt.legend()
            plt.show()

        if __name__ == "__main__":
            main()


while True:
      newthe(liste)
      print("bitti...")
      time.sleep(60*60*24)

