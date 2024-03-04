import time
import requests
import json
from colorama import Fore, Style
import requests
import warnings
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import random
import re
import numpy as np
from decimal import Decimal
from pmdarima import auto_arima as arm
from tabulate import tabulate
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
import tkinter as tk
from tkinter import ttk as ttk
import sys
from tkinter import scrolledtext
import threading
from scipy.stats import randint, uniform
from sklearn.model_selection import RandomizedSearchCV
from sklearn.neural_network import MLPRegressor
from tqdm import tqdm
import pandas_ta as ta
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
warnings.filterwarnings("ignore")


api_key = 'RjCgL26lL8GoDagHA4Pb2wFC9414Oenhp5oGOfQMJrCJbWpU9yBtMPofuNAm3cXL'
api_secret = 'SGNelarbzwvaFVRpQXhfeX9EPbLFRYIIKi8B2PloNTepvT6Q12LIYsCXbgkn8DGF'


bist = [
    "A1CAP.IS", "ACSEL.IS", "ADEL.IS", "ADESE.IS", "ADGYO.IS", "AEFES.IS", "AFYON.IS", "AGESA.IS", "AGHOL.IS", "AGROT.IS",
    "AGYO.IS", "AHGAZ.IS", "AKBNK.IS", "AKCNS.IS", "AKENR.IS", "AKFGY.IS", "AKFYE.IS", "AKGRT.IS", "AKMGY.IS", "AKSA.IS",
    "AKSEN.IS", "AKSGY.IS", "AKSUE.IS", "AKYHO.IS", "ALARK.IS", "ALBRK.IS", "ALCAR.IS", "ALCTL.IS", "ALFAS.IS", "ALGYO.IS",
    "ALKA.IS", "ALKIM.IS", "ALMAD.IS", "ANELE.IS", "ANGEN.IS", "ANHYT.IS", "ANSGR.IS", "ARASE.IS", "ARCLK.IS", "ARDYZ.IS",
    "ARENA.IS", "ARSAN.IS", "ARZUM.IS", "ASELS.IS", "ASGYO.IS", "ASTOR.IS", "ASUZU.IS", "ATAGY.IS", "ATAKP.IS", "ATATP.IS",
    "ATEKS.IS", "ATLAS.IS", "ATSYH.IS", "AVGYO.IS", "AVHOL.IS", "AVOD.IS", "AVPGY.IS", "AVTUR.IS", "AYCES.IS", "AYDEM.IS",
    "AYEN.IS", "AYES.IS", "AYGAZ.IS", "AZTEK.IS", "BAGFS.IS", "BAKAB.IS", "BALAT.IS", "BANVT.IS", "BARMA.IS", "BASCM.IS",
    "BASGZ.IS", "BAYRK.IS", "BEGYO.IS", "BERA.IS", "BEYAZ.IS", "BFREN.IS", "BIENY.IS", "BIGCH.IS", "BIMAS.IS", "BINHO.IS",
    "BIOEN.IS", "BIZIM.IS", "BJKAS.IS", "BLCYT.IS", "BMSCH.IS", "BMSTL.IS", "BNTAS.IS", "BOBET.IS", "BORLS.IS", "BOSSA.IS",
    "BRISA.IS", "BRKO.IS", "BRKSN.IS", "BRKVY.IS", "BRLSM.IS", "BRMEN.IS", "BRSAN.IS", "BRYAT.IS", "BSOKE.IS", "BTCIM.IS",
    "BUCIM.IS", "BURCE.IS", "BURVA.IS", "BVSAN.IS", "BYDNR.IS", "CANTE.IS", "CASA.IS", "CATES.IS", "CCOLA.IS", "CELHA.IS",
    "CEMAS.IS", "CEMTS.IS", "CEOEM.IS", "CIMSA.IS", "CLEBI.IS", "CMBTN.IS", "CMENT.IS", "CONSE.IS", "COSMO.IS", "CRDFA.IS",
    "CRFSA.IS", "CUSAN.IS", "CVKMD.IS", "CWENE.IS", "DAGHL.IS", "DAGI.IS", "DAPGM.IS", "DARDL.IS", "DENGE.IS", "DERHL.IS",
    "DERIM.IS", "DESA.IS", "DESPC.IS", "DEVA.IS", "DGATE.IS", "DGGYO.IS", "DGNMO.IS", "DIRIT.IS", "DITAS.IS", "DJIST.IS",
    "DMRGD.IS", "DMSAS.IS", "DNISI.IS", "DOAS.IS", "DOBUR.IS", "DOCO.IS", "DOFER.IS", "DOGUB.IS", "DOHOL.IS", "DOKTA.IS",
    "DURDO.IS", "DYOBY.IS", "DZGYO.IS", "EBEBK.IS", "ECILC.IS", "ECZYT.IS", "EDATA.IS", "EDIP.IS", "EGEEN.IS", "EGEPO.IS",
    "EGGUB.IS", "EGPRO.IS", "EGSER.IS", "EKGYO.IS", "EKIZ.IS", "EKOS.IS", "EKSUN.IS", "ELITE.IS", "EMKEL.IS", "EMNIS.IS",
    "ENERY.IS", "ENJSA.IS", "ENKAI.IS", "ENSRI.IS", "EPLAS.IS", "ERBOS.IS", "ERCB.IS", "EREGL.IS", "ERSU.IS", "ESCAR.IS",
    "ESCOM.IS", "ESEN.IS", "ETILR.IS", "ETYAT.IS", "EUHOL.IS", "EUKYO.IS", "EUPWR.IS", "EUREN.IS", "EUYO.IS", "EYGYO.IS",
    "FADE.IS", "FENER.IS", "FLAP.IS", "FMIZP.IS", "FONET.IS", "FORMT.IS", "FORTE.IS", "FRIGO.IS", "FROTO.IS", "FZLGY.IS",
    "GARAN.IS", "GARFA.IS", "GEDIK.IS", "GEDZA.IS", "GENIL.IS", "GENTS.IS", "GEREL.IS", "Menkul.IS", "GESAN.IS", "GIPTA.IS",
    "GLBMD.IS", "GLCVY.IS", "GLDTR.IS", "GLRYH.IS", "GLYHO.IS", "GMSTR.IS", "GMTAS.IS", "GOKNR.IS", "GOLTS.IS", "GOODY.IS",
    "GOZDE.IS", "GRNYO.IS", "GRSEL.IS", "GRTRK.IS", "GSDDE.IS", "GSDHO.IS", "GSRAY.IS", "GUBRF.IS", "GWIND.IS", "GZNMI.IS",
    "HALKB.IS", "HATEK.IS", "HATSN.IS", "HDFGS.IS", "HEDEF.IS", "HEKTS.IS", "HKTM.IS", "HLGYO.IS", "HTTBT.IS", "HUBVC.IS",
    "HUNER.IS", "HURGZ.IS", "ICBCT.IS", "ICUGS.IS", "IDEAS.IS", "IDGYO.IS", "IEYHO.IS", "IHAAS.IS", "IHEVA.IS", "IHGZT.IS",
    "IHLAS.IS", "IHLGM.IS", "IHYAY.IS", "IMASM.IS", "INDES.IS", "INFO.IS", "INGRM.IS", "INTEM.IS", "INVEO.IS", "INVES.IS",
    "IPEKE.IS", "ISATR.IS", "ISBIR.IS", "ISBTR.IS", "ISCTR.IS", "ISDMR.IS", "ISFIN.IS", "ISGSY.IS", "ISGYO.IS", "ISIST.IS",
    "ISKPL.IS", "ISKUR.IS", "ISMEN.IS", "ISSEN.IS", "ISYAT.IS", "IZENR.IS", "IZFAS.IS", "IZINV.IS", "IZMDC.IS", "JANTS.IS",
    "KAPLM.IS", "KAREL.IS", "KARSN.IS", "KARTN.IS", "KARYE.IS", "KATMR.IS", "KAYSE.IS", "KBORU.IS", "KCAER.IS", "KCHOL.IS",
    "KENT.IS", "KERVN.IS", "KERVT.IS", "KFEIN.IS", "KGYO.IS", "KIMMR.IS", "KLGYO.IS", "KLKIM.IS", "KLMSN.IS", "KLNMA.IS",
    "KLRHO.IS", "KLSER.IS", "KLSYN.IS", "KMPUR.IS", "KNFRT.IS", "KONKA.IS", "KONTR.IS", "KONYA.IS", "KOPOL.IS", "KORDS.IS",
    "KOZAA.IS", "KOZAL.IS", "KRDMA.IS", "KRDMB.IS", "KRDMD.IS", "KRGYO.IS", "KRONT.IS", "KRPLS.IS", "KRSTL.IS", "KRTEK.IS",
    "KRVGD.IS", "KSTUR.IS", "KTLEV.IS", "KTSKR.IS", "KUTPO.IS", "KUVVA.IS", "KUYAS.IS", "KZBGY.IS", "KZGYO.IS", "LIDER.IS",
    "LIDFA.IS", "LINK.IS", "LKMNH.IS", "LOGO.IS", "LRSHO.IS", "LUKSK.IS", "MAALT.IS", "MACKO.IS", "MAGEN.IS", "MAKIM.IS",
    "MAKTK.IS", "MANAS.IS", "MARBL.IS", "MARKA.IS", "MARTI.IS", "MAVI.IS", "MEDTR.IS", "MEGAP.IS", "MEGAP.IS", "MEGMT.IS",
    "MEKAG.IS", "MEPET.IS", "MERCN.IS", "MERIT.IS", "MERKO.IS", "METRO.IS", "METUR.IS", "MGROS.IS", "MHRGY.IS", "MIATK.IS",
    "MIPAZ.IS", "MMCAS.IS", "MNDRS.IS", "MNDTR.IS", "MOBTL.IS", "MPARK.IS", "MRGYO.IS", "MRSHL.IS", "MSGYO.IS", "MTRKS.IS",
    "MTRYO.IS", "MZHLD.IS", "NATEN.IS", "NETAS.IS", "NIBAS.IS", "NTGAZ.IS", "NTHOL.IS", "NUGYO.IS", "NUHCM.IS", "OBASE.IS",
    "ODAS.IS", "OFSYM.IS", "ONCSM.IS", "ORCAY.IS", "ORGE.IS", "ORMA.IS", "OSMEN.IS", "OSTIM.IS", "OTKAR.IS", "OTTO.IS",
    "OYAKC.IS", "OYAYO.IS", "OYLUM.IS", "OYYAT.IS", "OZGYO.IS", "OZKGY.IS", "OZKGY.IS", "OZRDN.IS", "OZSUB.IS", "PAGYO.IS",
    "PAMEL.IS", "PAPIL.IS", "PARSN.IS", "PASEU.IS", "PCILT.IS", "PEGYO.IS", "PEKGY.IS", "PENGD.IS", "PENTA.IS", "PETKM.IS",
    "PETUN.IS", "PGSUS.IS", "PINSU.IS", "PKART.IS", "PKENT.IS", "Menkul.IS", "PLTUR.IS", "PNLSN.IS", "PNSUT.IS", "POLHO.IS",
    "POLTK.IS", "PRDGS.IS", "PRKAB.IS", "PRKME.IS", "PRZMA.IS", "PSDTC.IS", "PSDTC.IS", "PSDTC.IS", "PSDTC.IS", "PSGYO.IS",
    "QNBFB.IS", "QNBFL.IS", "QUAGR.IS", "RALYH.IS", "RAYSG.IS", "REEDR.IS", "RNPOL.IS", "RODRG.IS", "ROYAL.IS", "RTALB.IS",
    "RUBNS.IS", "RYGYO.IS", "RYSAS.IS", "SAFKR.IS", "SAHOL.IS", "SAMAT.IS", "SANEL.IS", "SANFM.IS", "SANKO.IS", "SARKY.IS",
    "SASA.IS", "SAYAS.IS", "SDTTR.IS", "SEGYO.IS", "SEKFK.IS", "SEKUR.IS", "SELEC.IS", "SELGD.IS", "SELVA.IS", "SEYKM.IS",
    "SILVR.IS", "SISE.IS", "SKBNK.IS", "SKTAS.IS", "SKYMD.IS", "SMART.IS", "SMRTG.IS", "SNGYO.IS", "SNICA.IS", "SNKRN.IS",
    "SNPAM.IS", "SODSN.IS", "SOKE.IS", "SOKM.IS", "SONME.IS", "SRVGY.IS", "SUMAS.IS", "SUNTK.IS", "SURGY.IS", "SUWEN.IS",
    "TABGD.IS", "TARKM.IS", "TATEN.IS", "TATGD.IS", "TAVHL.IS", "TBORG.IS", "TCELL.IS", "TDGYO.IS", "TEKTU.IS", "TERA.IS",
    "TETMT.IS", "TEZOL.IS", "TGSAS.IS", "THYAO.IS", "TKFEN.IS", "TKNSA.IS", "TLMAN.IS", "TMPOL.IS", "TMSN.IS", "TNZTP.IS",
    "TOASO.IS", "TRCAS.IS", "TRGYO.IS", "TRILC.IS", "TSGYO.IS", "TSKB.IS", "TSPOR.IS", "TTKOM.IS", "TTRAK.IS", "TUCLK.IS",
    "TUKAS.IS", "TUPRS.IS", "TUREX.IS", "TURGG.IS", "TURSG.IS", "UFUK.IS", "ULAS.IS", "ULKER.IS", "ULUFA.IS","ULKER.IS",
    "ULUFA.IS", "ULUSE.IS", "ULUUN.IS", "UMPAS.IS", "UNLU.IS", "USAK.IS", "USDTR.IS", "UZERB.IS", "VAKBN.IS",
    "VAKFN.IS", "VAKKO.IS", "VANGD.IS", "VBTYZ.IS", "VERTU.IS", "VERUS.IS", "VESBE.IS", "VESTL.IS", "VKFYO.IS",
    "VKGYO.IS", "VKING.IS", "VRGYO.IS", "X030S.IS", "X100S.IS", "XBANA.IS", "XBANK.IS", "XBLSM.IS", "XELKT.IS", "XFINK.IS",
    "XGIDA.IS", "XGMYO.IS", "XHARZ.IS", "XHOLD.IS", "XILTM.IS", "XINSA.IS", "XKAGT.IS", "XKMYA.IS", "XKOBI.IS", "XKURY.IS",
    "XMADN.IS", "XMANA.IS", "XMESY.IS", "XSADA.IS", "XSANK.IS", "XSANT.IS", "XSBAL.IS", "XSBUR.IS", "XSDNZ.IS", "XSGRT.IS",
    "XSIST.IS", "XSIZM.IS", "XSKAY.IS", "XSKOC.IS", "XSKON.IS", "XSPOR.IS", "XSTKR.IS", "XTAST.IS", "XTCRT.IS", "XTEKS.IS",
    "XTM25.IS", "XTMTU.IS", "XTRZM.IS", "XTUMY.IS", "XU030.IS", "XU050.IS", "XU100.IS", "XUHIZ.IS", "XULAS.IS", "XUMAL.IS",
    "XUSIN.IS", "XUSRD.IS", "XUTEK.IS", "XUTUM.IS", "XYLDZ.IS", "XYORT.IS", "XYUZO.IS", "YAPRK.IS", "YATAS.IS", "YAYLA.IS",
    "YBTAS.IS", "YEOTK.IS", "YESIL.IS", "YGGYO.IS", "YGYO.IS", "YKBNK.IS", "YKSLN.IS", "YONGA.IS", "YUNSA.IS", "YYAPI.IS",
    "YYLGD.IS", "Z30EA.IS", "Z30KE.IS", "Z30KP.IS", "ZEDUR.IS", "ZELOT.IS", "ZGOLD.IS", "ZOREN.IS", "ZPBDL.IS", "ZPLIB.IS",
    "ZPT10.IS", "ZPX30.IS", "ZRE20.IS", "ZRGYO.IS", "ZTM15.IS"]
random.shuffle(bist)
end = datetime.now() + timedelta(days=1)
end = end.strftime("%Y-%m-%d")
endcontrol = (datetime.now()).strftime("%Y-%m-%d")
enddate = str(endcontrol)+" 00:00:00"
startdate = datetime.now() - timedelta(days=58)
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

def indikator():

    api_key = 'RjCgL26lL8GoDagHA4Pb2wFC9414Oenhp5oGOfQMJrCJbWpU9yBtMPofuNAm3cXL'
    api_secret = 'SGNelarbzwvaFVRpQXhfeX9EPbLFRYIIKi8B2PloNTepvT6Q12LIYsCXbgkn8DGF'

    endpoint = 'https://api.binance.com/api/v3/exchangeInfo'

    def get_usdt_pairs(valid_pairs=None):
        response = requests.get(endpoint)
        data = json.loads(response.text)

        usdt_pairs = [symbol['symbol'] for symbol in data['symbols'] if symbol['quoteAsset'] == 'USDT']

        if valid_pairs:
            usdt_pairs = [pair for pair in usdt_pairs if pair in valid_pairs]

        return usdt_pairs

    def binance_api(endpoint, params=None):
        headers = {'X-MBX-APIKEY': api_key}
        response = requests.get(endpoint, headers=headers, params=params)
        return json.loads(response.text)

    usdt_pairs = get_usdt_pairs()
    pairs_list = []

    for pair in usdt_pairs:
        modified_pair = pair
        pairs_list.append(modified_pair)
    pairs_list = [eleman.replace("USDT", "-USD") for eleman in pairs_list]
    b=bist
    c=pairs_list
    symbols = c
    random.shuffle(symbols)
    aralık = 24
    interval = "1h"
    if symbols==pairs_list:
        dif=70
        rms=0.2
        testsize=0.2
        trainsize=0.8
    else:
        dif=30
        rms=0.2
        testsize=0.2
        trainsize=0.8

    symbols = [symbol for symbol in symbols if "PERP" not in symbol]
    symbols = [symbol for symbol in symbols if "DOWN" not in symbol]
    symbols = [symbol for symbol in symbols if "BEAR" not in symbol]
    symbols = [symbol for symbol in symbols if "UP" not in symbol]
    symbols = [symbol for symbol in symbols if "BULL" not in symbol]

    say=0
    say2=str(len(symbols))

    for symbol in symbols:
        try:
            say=say+1
            ilerleme = str(say) + "/" + say2

            print(Fore.MAGENTA + symbol +"-"+Fore.LIGHTBLUE_EX + ilerleme+ Style.RESET_ALL)

            # Finansal verileri indirin
            data = yf.download(symbol, start=startdate, progress=False, interval=interval, end=end)
            data['Date'] = data.index
            data = data.dropna()
            data = data[['Date', 'Close','Low','High']]


            df = data
            print(df['Date'][-1].strftime('%Y-%m-%d'))
            print(((datetime.now())).strftime('%Y-%m-%d'))
            if df['Date'][-1].strftime('%Y-%m-%d') != ((datetime.now())).strftime('%Y-%m-%d'):
                print(df['Date'][-1].strftime('%Y-%m-%d'))
                print("veri eksik veya hatalı")
                continue


            # Fiyat verilerini 10 gün kaydır
            df['target'] = df['Close'].shift(-aralık)


            if (df['Date'][-1]).strftime('%Y-%m-%d') == ((datetime.now())).strftime('%Y-%m-%d'):
                def calculate_CCI(data, window):
                    TP = (data['High'] + data['Low'] + data['Close']) / 3
                    CCI = (TP - TP.rolling(window=window).mean()) / (0.015 * TP.rolling(window=window).std())
                    return CCI

                data['CCI'] = calculate_CCI(data, 20)

                # Alım ve satım sinyalleri üretme
                data['CCI-Signal'] = 0
                buy_signal_threshold = -100  # Alım sinyali için eşik değeri
                sell_signal_threshold = 100  # Satım sinyali için eşik değeri
                data['CCI-Signal'][data['CCI'] < buy_signal_threshold] = 1  # Alım sinyali
                data['CCI-Signal'][data['CCI'] > sell_signal_threshold] = -1  # Satım sinyali
                if str(data['CCI-Signal'].iloc[-1]) == "1":


                    messageccı=symbol+" CCI Alım sinyali "+interval+"'lik aralıkta" + " son kapanış fiyatı: "+str(data['Close'].iloc[-1])
                    send_telegram_message(messageccı)
                elif str(data['CCI-Signal'].iloc[-1]) == "-1":

                    print(Fore.RED + "CCI Satım sinyali" + Style.RESET_ALL)
                    continue

                else:

                    print(Fore.YELLOW + "CCI sinyali yok" + Style.RESET_ALL)
                    continue



                data['20 Day MA'] = data['Close'].rolling(window=20).mean()
                data['Upper Band'] = data['20 Day MA'] + 2 * data['Close'].rolling(window=20).std()
                data['Lower Band'] = data['20 Day MA'] - 2 * data['Close'].rolling(window=20).std()

                # Alım ve satım sinyalleri üretin
                data['Signal'] = 0
                data['Signal'][data['Close'] < data['Lower Band']] = 1  # Alım sinyali
                data['Signal'][data['Close'] > data['Upper Band']] = -1  # Satım sinyali
                if str(data['Signal'].iloc[-1]) == "1":

                    print(Fore.GREEN + "Bolinger Alım sinyali" + Style.RESET_ALL)
                elif str(data['Signal'].iloc[-1]) == "-1":

                    print(Fore.RED + "Bolinger Satım sinyali" + Style.RESET_ALL)
                    continue
                else:

                    print(Fore.YELLOW + "Bolinger sinyali yok" + Style.RESET_ALL)


                # Giriş verilerini ve hedef değişkeni ayarlayın
                X = df.iloc[:-aralık][['Close']].values
                y = df['target'].dropna().values

                # Veriyi eğitim ve test setlerine bölelim
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=testsize, train_size=trainsize)

                # Hiperparametre dağılımını belirle
                param_dist = {
                    'hidden_layer_sizes': [(100,), (200,), (500,), (100, 100), (200, 200), (500, 500), (300, 200),
                                           (200, 200)],
                    'max_iter': randint(500, 1500),
                    'learning_rate': ['constant', 'adaptive'],
                    'activation': ['relu', 'tanh']
                }

                # MLPRegressor modelini oluştur
                mlp = MLPRegressor()


                random_search = RandomizedSearchCV(mlp, param_distributions=param_dist, n_iter=5, cv=5,
                                                   random_state=None)
                random_search.fit(X_train, y_train)
                print(random_search.best_params_)
                param = random_search.best_params_

                mlp = MLPRegressor(**param)

                mlp.fit(X_train, y_train)

                last_price = df['Close'].iloc[-1]
                forecast = []
                y_pred = mlp.predict(X_test)

                # Calculate Mean Squared Error
                mse = mean_squared_error(y_test, y_pred)

                # Calculate Root Mean Squared Error
                rmse = np.sqrt(mse)
                for i in range(aralık):
                    forecast.append(mlp.predict([[last_price]])[0])
                    last_price = forecast[-1]

                # lineer regresyon
                X = df[['Low', 'High']]
                y = df['Close']

                imputer = SimpleImputer(strategy='mean')
                X_imputed = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)

                model = LinearRegression()

                model.fit(X_imputed, y)

                last_date = df['Date'].max()
                future_date_10th = last_date + timedelta(days=aralık)
                future_features_10th = pd.DataFrame(index=[future_date_10th], columns=['Low', 'High'])

                future_features_10th_imputed = pd.DataFrame(imputer.transform(future_features_10th),
                                                            columns=future_features_10th.columns)

                forecast = model.predict(future_features_10th_imputed)[0]

                X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.2, random_state=42)
                y_pred = model.predict(X_test)
                rmse = np.sqrt(mean_squared_error(y_test, y_pred))

                print(f'RMSE: {rmse}')

                if rmse < 0.2:
                    print(f'Forecasted Close Price : {forecast}')
                    if float(df['Close'][-1]) < float(forecast):
                        difference=((float(forecast)-float(df['Close'][-1]))/float(df['Close'][-1]))*100
                        print(Fore.GREEN + 'Lineer Regresyon : yükselecek Değişim: '+ str(difference)+  "--->Hedef Fiyat:"+ str(forecast)+ Style.RESET_ALL)
                        message5='Lineer Regresyon : yükselecek Değişim: '+ str(difference) + "--->Hedef Fiyat:"+ str(forecast)
                    else:
                        print('Yükseliş yok')
                        message5=''
                else:
                    print('RMSE is above 0.2, and forecast is not shown.')
                    message5=''




                n=9
                m1 = 3
                m2 = 3
                df['Lowest_Low'] = df['Low'].rolling(window=n).min()
                df['Highest_High'] = df['High'].rolling(window=n).max()

                df['%K'] = ((df['Close'] - df['Lowest_Low']) / (df['Highest_High'] - df['Lowest_Low'])) * 100
                df['%D'] = df['%K'].rolling(window=m1).mean()
                df['%J'] = 3 * df['%K'] - 2 * df['%D']

                # Son %J değerini kontrol etme
                last_j = df['%J'].iloc[-1]
                last_d = df['%D'].iloc[-1]
                last_k = df['%K'].iloc[-1]
                #stokastik
                k_period = 14
                d_period = 3
                # Hesaplamaları yap
                data['Lowest_Low'] = data['Low'].rolling(window=k_period).min()
                data['Highest_High'] = data['High'].rolling(window=k_period).max()
                data['%K'] = 100 * ((data['Close'] - data['Lowest_Low']) / (data['Highest_High'] - data['Lowest_Low']))
                data['%D'] = data['%K'].rolling(window=d_period).mean()
                signals = []
                position = None

                for i in range(1, len(data)):
                    # Alım sinyali
                    if data['%K'][i] < 20 and data['%D'][i] < 20 and data['%K'][i - 1] >= data['%D'][i - 1]:
                        signals.append('AL')
                        position = 'UZUN'  # Uzun pozisyon alındı
                    # Satış sinyali
                    elif data['%K'][i] > 80 and data['%D'][i] > 80 and data['%K'][i - 1] <= data['%D'][i - 1]:
                        signals.append('SAT')
                        position = 'KISA'  # Kısa pozisyon alındı
                    else:
                        signals.append('BEKLE')
                print(Fore.LIGHTGREEN_EX + "STOKASTİK Osilatör:",signals[-1]+Style.RESET_ALL)
                if signals[-1]=='AL':
                    messagestokastik=symbol+" STOKASTİK AL SİNYALİ"+"fiyat:"+forecast
                    send_telegram_message(messagestokastik)
                    allgoingmessage= symbol + " tüm indikatörler OK"+" aralık:"+interval
                    send_telegram_message(allgoingmessage)
                period = 10
                multiplier = 3

                data['TR'] = 0.0
                data['ATR'] = 0.0
                data['UpperBand'] = 0.0
                data['LowerBand'] = 0.0
                data['SuperTrend'] = 0.0
                data['Position'] = 0

                for i in range(1, len(data)):
                    data['TR'].iloc[i] = max(data['High'].iloc[i] - data['Low'].iloc[i],
                                             abs(data['High'].iloc[i] - data['Close'].iloc[i - 1]),
                                             abs(data['Low'].iloc[i] - data['Close'].iloc[i - 1]))

                    if i > period:
                        data['ATR'].iloc[i] = (data['ATR'].iloc[i - 1] * (period - 1) + data['TR'].iloc[i]) / period
                    else:
                        data['ATR'].iloc[i] = data['TR'].iloc[1:i + 1].mean()

                    data['UpperBand'].iloc[i] = data['Close'].iloc[i - 1] + multiplier * data['ATR'].iloc[i]
                    data['LowerBand'].iloc[i] = data['Close'].iloc[i - 1] - multiplier * data['ATR'].iloc[i]

                    if data['Close'].iloc[i] > data['UpperBand'].iloc[i]:
                        data['SuperTrend'].iloc[i] = data['LowerBand'].iloc[i]
                        data['Position'].iloc[i] = 1  # Long position
                    elif data['Close'].iloc[i] < data['LowerBand'].iloc[i]:
                        data['SuperTrend'].iloc[i] = data['UpperBand'].iloc[i]
                        data['Position'].iloc[i] = -1  # Short position
                    else:
                        data['SuperTrend'].iloc[i] = data['SuperTrend'].iloc[i - 1]
                        data['Position'].iloc[i] = 0  # No position
                # Önceki örneği kullanarak alım ve satım sinyallerini ekleyin
                data['Buy_Signal'] = ((data['Close'] > data['SuperTrend']) & (
                            data['Close'].shift(1) <= data['SuperTrend'].shift(1))).astype(int)
                data['Sell_Signal'] = ((data['Close'] < data['SuperTrend']) & (
                            data['Close'].shift(1) >= data['SuperTrend'].shift(1))).astype(int)


                #calculate rsi

                data['rsi'] = ta.rsi(data['Close'], length=14)
                if data['rsi'].iloc[-1] > 70:
                    sinyal4=-1
                    rsi_sinyali = "SAT"
                    print(Fore.BLUE + "RSİ : " + rsi_sinyali + Style.RESET_ALL)
                    message3="RSİ:" + " " + rsi_sinyali
                elif data['rsi'].iloc[-1] < 30:
                    rsi_sinyali = "AL"
                    sinyal4=1
                    print(Fore.LIGHTGREEN_EX +"RSİ : " + rsi_sinyali + Style.RESET_ALL)
                    message3 = "RSİ:" + " " + rsi_sinyali
                else:
                    sinyal4 = 0
                    rsi_sinyali = "sinyal yok"
                    print(Fore.RED + "RSİ : " + rsi_sinyali + Style.RESET_ALL)
                    message3 = "RSİ:" + " " + rsi_sinyali



                if int(data['Buy_Signal'].iloc[-1]) == 1:
                    alım_sinyali = "Supertrend : AL"
                    sinyal=1
                    print(Fore.LIGHTGREEN_EX + alım_sinyali + Style.RESET_ALL)
                    message=symbol+" "+alım_sinyali
                    send_telegram_message(message)
                else:
                    sinyal = 0
                    alım_sinyali = "Supertrend : ALMA"
                    print(Fore.RED + alım_sinyali + Style.RESET_ALL)

                if int(data['Sell_Signal'].iloc[-1])==1:
                    sinyal5 = -1
                    satım_sinyali = "Supertrend : SAT"
                    print(Fore.LIGHTRED_EX + satım_sinyali + Style.RESET_ALL)
                else:
                    sinyal5 = 0
                    satım_sinyali = "Supertrend : HOLD"
                    print(Fore.BLUE + satım_sinyali + Style.RESET_ALL)


                if last_j > 80 or last_k > 80 :
                    print(Fore.RED + "KDJ: Aşırı Alımda, Düşecek " + symbol + "" + Style.RESET_ALL)
                    sinyal2=-1
                    message1 = "KDJ: Aşırı Alımda, Düşecek "
                elif last_k < 0 or last_j < 0 :
                    print(Fore.GREEN + "KDJ: Aşırı satışta, Yükselecek " + symbol + "" + Style.RESET_ALL)
                    sinyal2=1
                    message1 = "KDJ: Aşırı satışta, Yükselecek "
                else:
                    print(Fore.YELLOW + "J: " + str(Decimal(last_j).quantize(Decimal('0.00000'))) + " " +"D : " + str(Decimal(last_d).quantize(Decimal('0.00000'))) + " " + "K : " + str(Decimal(last_k).quantize(Decimal('0.00000'))) + Style.RESET_ALL)
                    sinyal2=0
                    message1 = " "

                macd = df['Close'].ewm(span=12, adjust=False).mean() - df['Close'].ewm(span=26, adjust=False).mean()
                if macd.iloc[-1] > 0:
                    print(Fore.GREEN + "MACD: yükseliş trendinde" + Style.RESET_ALL)
                    sinyal3=1
                    message2="MACD: yükseliş trendinde"

                else:
                    print(Fore.RED + "MACD: " + str(Decimal(macd.iloc[-1]).quantize(Decimal('0.00000'))) + " " + Style.RESET_ALL)
                    sinyal3=0
                    message2=" "
                if str(data['Buy_Signal'].iloc[-1]) == "1":
                    alım_sinyali = "AL"
                    message4=sinyal+sinyal2+sinyal3+sinyal4+sinyal5
                    message = (symbol + " " + alım_sinyali + " " + message1+ " " + message2 + " " +
                               message3+ " " +"Sinyal Gücü: " + str(message4)+"/4"+" -> "+str(message5))
                    send_telegram_message(message)
                    print("sinyal gücü:"+str(sinyal+sinyal2+sinyal3+sinyal4)+"/4")

            else:
                print(Fore.RED + "veri hatalı" + Style.RESET_ALL)
        except Exception as e:
            print(e)

while True:
    if __name__ == '__main__':
        indikator()
    time.sleep(14400)