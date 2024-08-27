import time
import requests
from colorama import Fore, Style
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import re
import numpy as np
from tabulate import tabulate
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.ensemble import VotingRegressor
from bs4 import BeautifulSoup
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.model_selection import cross_val_score
import streamlit as st

st.set_page_config(layout="wide", page_title="Dorecast")
api_key = 'RjCgL26lL8GoDagHA4Pb2wFC9414Oenhp5oGOfQMJrCJbWpU9yBtMPofuNAm3cXL'
api_secret = 'SGNelarbzwvaFVRpQXhfeX9EPbLFRYIIKi8B2PloNTepvT6Q12LIYsCXbgkn8DGF'

end = datetime.now() + timedelta(days=1)


startdate = datetime.now() - timedelta(days=41)
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
liste=cr
print(str("kripto: "+str(len(cr))))
print(str("bist: "+str(len(bist))))
def newthe(liste,end=end):
    sepet = pd.DataFrame(columns=["symbol","close","difference",
                                  "forecast","date",
                                  "hedef_tarih","MAPE"])
    interval='1h'


    süre=24*3
    beklenen_sinyal=1
    sell=pd.DataFrame(columns=["symbol","close","date"])
    say1 = 0
    for symbol in liste:
        try:
            say1 += 1


            if symbol.endswith(".IS"):
                beklenen_degisim = 5
            else:
                beklenen_degisim = 100
            print(Fore.CYAN + str(say1)+"/"+str(len(liste))+" "+symbol+" "+ Style.RESET_ALL)

            data = yf.download(symbol,threads=True,repair=True,start=startdate, progress=False, interval=interval, end=end)
            data['close'] = data['Close']
            data.reset_index(inplace=True)
            ortalama = data['close'].mean()

            data['Datetime'] = pd.to_datetime(data['Datetime']).dt.tz_localize(None)





            # Teknik göstergeleri hesapla
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

            def calculate_kdj(data, window=14):
                low_min = data['Low'].rolling(window=window).min()
                high_max = data['High'].rolling(window=window).max()
                data['%K'] = 100 * ((data['close'] - low_min) / (high_max - low_min))
                data['%D'] = data['%K'].rolling(window=3).mean()
                data['%J'] = 3 * data['%K'] - 2 * data['%D']
                data['KDJ Signal'] = np.where(data['%J'] < 20, 1, np.where(data['%J'] > 80, -1, 0))

            def calculate_EMA(data):
                data['EMA20'] = data['close'].ewm(span=20, adjust=False).mean()
                data['EMA120'] = data['close'].ewm(span=120, adjust=False).mean()
                data['EMA Signal'] = np.where(data['EMA20'] > data['EMA120'], 1, -1)

            def calculate_indicators(data):
                calculate_macd(data)
                calculate_rsi(data)
                calculate_EMA(data)
                calculate_kdj(data)

            def generate_signals(data):
                data['Signal'] = data[['MACD Signal', 'KDJ Signal', 'RSI Signal', 'EMA Signal']].sum(axis=1)

            # Teknik göstergeleri hesapla ve sinyalleri oluştur
            calculate_indicators(data)
            generate_signals(data)

            if data['Signal'].iloc[-1] >= 1:
                data.fillna(0, inplace=True)

                def create_lagged_features(data, lag=süre):
                    df = data.copy()
                    for i in range(1, lag + 1):
                        df[f'lag_{i}'] = df['close'].shift(i)
                    return df

                data_with_lags = create_lagged_features(data)
                data_with_lags.dropna(inplace=True)
                X = data_with_lags.drop(['Datetime', 'close', 'Signal Line', 'MACD Signal', 'RSI Signal',
                                         'KDJ Signal', 'EMA Signal', 'Signal'], axis=1)
                y = data_with_lags['close']
                X_train, X_test, y_train, y_test = X.iloc[:-süre], X.iloc[-süre:], y.iloc[:-süre], y.iloc[-süre:]

                estimators1 = [10, 100, 50, 150, 200]
                for estimators in estimators1:
                    models = {
                        'rf': RandomForestRegressor(n_estimators=estimators, random_state=42),
                        'gb': GradientBoostingRegressor(n_estimators=estimators, learning_rate=0.1, max_depth=3,
                                                        random_state=42),
                        'ab': AdaBoostRegressor(n_estimators=estimators, learning_rate=1.0, random_state=42),
                        'xgb': XGBRegressor(n_estimators=estimators, learning_rate=0.1, max_depth=6, random_state=42,
                                            verbosity=0),
                        'lgbm': LGBMRegressor(n_estimators=estimators, learning_rate=0.05, random_state=42,
                                              verbosity=-1)
                    }

                # Modelleri ve performanslarını depolamak için bir sözlük
                model_performance = {}

                # Modelleri deneyin ve performanslarını değerlendirin
                for name, model in models.items():
                    scores = cross_val_score(model, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
                    model_performance[name] = np.mean(np.sqrt(-scores))

                # Performansları karşılaştırın
                sorted_models = sorted(model_performance.items(), key=lambda x: x[1])
                best_models = sorted_models[:2]

                # Seçilen modellerle ensemble modeli oluşturun
                best_model_objects = [(name, models[name]) for name, _ in best_models]
                ensemble_model = VotingRegressor(estimators=best_model_objects)

                # Ensemble modelini eğitin
                ensemble_model.fit(X_train, y_train)

                future_predictions = []
                last_known_features = X_test.iloc[-1].values
                for i in range(süre):
                    prediction = ensemble_model.predict(last_known_features.reshape(1, -1))[0]
                    future_predictions.append(prediction)

                    # Gecikmeli özellikleri güncelleyin
                    last_known_features = np.roll(last_known_features, -1)
                    last_known_features[-1] = prediction

                y_pred = ensemble_model.predict(X_test)
                beklenen_MAPE = 10
                MAPE=np.mean(np.abs((y_test - y_pred) / y_test)) * 100

                seventh_day_prediction = future_predictions[-1]
                if MAPE > beklenen_MAPE:
                    print(Fore.RED + "BEKLENEN MAPE: " + str(beklenen_MAPE) + Style.RESET_ALL)
                    print(Fore.RED +symbol+ " YÜKSEK MAPE: " + str(MAPE) + Style.RESET_ALL)
                elif MAPE <= beklenen_MAPE:

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
                                                   'MAPE':[MAPE]})
                            add_data = add_data.dropna(axis=1, how='all')
                            sepet=pd.concat([sepet,add_data],ignore_index=True)

                        else:
                            print(Fore.RED + "Değişim oranı yetersiz: " + str(difference_percent) + "%" + Style.RESET_ALL)
                    else:
                        print(Fore.RED + symbol+" yetersiz .....değişim : "+str(seventh_day_prediction-data[['close']].tail(1).values[0][0]) + Style.RESET_ALL)
                else:
                    print(Fore.RED + "BEKLENEN MAPE: " + str(beklenen_MAPE) + Style.RESET_ALL)
                    print(Fore.RED + symbol + " YÜKSEK MAPE: " + str(MAPE) + Style.RESET_ALL)
            elif data['Signal'].iloc[-1] <=-3:
                print(Fore.RED + symbol + " Düşecek!!! " + Style.RESET_ALL)

                add_data_sell=pd.DataFrame({'symbol':[symbol],'close':[data[['close']].tail(1).values[0][0]],'date':[datetime.now().strftime("%d.%m.%Y")]})
                sell = sell.dropna(axis=1, how='all')
                add_data_sell = add_data_sell.dropna(axis=1, how='all')
                sell=pd.concat([sell,add_data_sell],ignore_index=True)
            else:
                print(Fore.RED + symbol + " sinyal gücü!  : " +str(data['Signal'].iloc[-1])+ Style.RESET_ALL)

        except Exception as e:
            print(Fore.RED + str(e) + Style.RESET_ALL)

    file='buy_list.xlsx'
    old_data=pd.read_excel(file)
    sepet=sepet.sort_values(by='difference', ascending=False)
    sepet.dropna()
    old_data.dropna()
    if sepet.empty:
        buylist = old_data.copy()  # Avoid modifying old_data
    else:
        # Check for columns with only NA values in sepet (optional)
        na_cols = sepet.columns[sepet.isna().all()]
        if len(na_cols) > 0:
            sepet.drop(na_cols, axis=1, inplace=True)  # Drop NA columns (optional)
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



if st.button("Analiz"):
    while True:
        baslangıc=datetime.now()
        newthe(liste)
        print("bitti...")
        print("Analiz süresi:",str(datetime.now()-baslangıc))
        send_telegram_message("Analiz süresi: " + str(datetime.now()-baslangıc))
        time.sleep(60*60)

