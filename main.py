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
from binance.client import Client

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
startdate = datetime.now() - timedelta(days=1000)
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
def take_data():
    url="https://www.kap.org.tr/tr/bist-sirketler"

    response = requests.get(url)
    df=pd.read_html(response.content)[0]
all_tickers = yf.Tickers("IS")
b = [ticker for ticker in all_tickers.tickers if ticker.endswith('.IS')]



def newone():


    api_key = 'RjCgL26lL8GoDagHA4Pb2wFC9414Oenhp5oGOfQMJrCJbWpU9yBtMPofuNAm3cXL'
    api_secret = 'SGNelarbzwvaFVRpQXhfeX9EPbLFRYIIKi8B2PloNTepvT6Q12LIYsCXbgkn8DGF'

    endpoint = 'https://api.binance.com/api/v3/exchangeInfo'

    def get_usdt_pairs():

        client = Client(api_key, api_secret)

        # Binance'de listelenen tüm sembolleri alın
        exchange_info = client.get_exchange_info()

        # Sembollerin listesini alın
        symbols = exchange_info['symbols']

        # Yalnızca spot piyasada işlem gören sembollerin listesini filtreleyin
        spot_symbols = [symbol['symbol'] for symbol in symbols if
                        symbol['quoteAsset'] == 'USDT']  # USDT bazlı spot semboller
        usdt_pairs=spot_symbols
        return usdt_pairs

    def binance_api(endpoint, params=None):
        headers = {'X-MBX-APIKEY': api_key}
        response = requests.get(endpoint, headers=headers, params=params)
        return json.loads(response.text)

    usdt_pairs = get_usdt_pairs()
    #pairs_list = []

    #for pair in usdt_pairs:
    #    modified_pair = pair
    #    pairs_list.append(modified_pair)
    #pairs_list = [eleman.replace("USDT", "-USD") for eleman in pairs_list]
    b=bist
    c = usdt_pairs

    symbols = c
    random.shuffle(symbols)
    aralık = 14
    interval = "1d"

    say = 0
    say2 = str(len(symbols))

    for symbol in symbols:
        try:
            say = say + 1
            ilerleme = str(say) + "/" + say2

            print(Fore.MAGENTA + symbol + "-" + Fore.LIGHTBLUE_EX + ilerleme + Style.RESET_ALL)

            if symbols == c:

                client = Client(api_key, api_secret)
                klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, startdate, end)

                # Veriyi DataFrame'e dönüştürün
                data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                                     'quote_asset_volume', 'number_of_trades',
                                                     'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume',
                                                     'ignore'])

                # Unix zaman damgasını normal zamana dönüştürün
                data['ts']=data['timestamp']
                data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
                data = data[['ts','timestamp','close', 'low', 'high']]
                data['Date'] = data['timestamp'].dt.date
                data['Close'] = data['close'].astype(float)
                data['Low'] = data['low'].astype(float)
                data['High'] = data['high'].astype(float)
            elif symbols == b:
                data = yf.download(symbol, start=startdate, progress=False, interval=interval, end=end)
            # Gereksiz sütunları düşürün
            else:
                data = yf.download(symbol, start=startdate, progress=False, interval=interval, end=end)

            # Tarih sütununu indeks olarak ayarlayın
            data.set_index('Date', inplace=True)
            data['Date'] = data.index

            data = data[['ts','Date', 'Close', 'Low', 'High']]

            from pmdarima import auto_arima
            from statsmodels.tsa.arima.model import ARIMA


            model = auto_arima(data['Close'], start_p=1, start_q=1, max_p=3, max_q=3, m=aralık, start_P=0, seasonal=True,
                               D=1, trace=False, error_action='ignore', suppress_warnings=True, stepwise=True)

            model.fit(data['Close'])

            # Tahmin
            tahmin = model.predict(n_periods=1)
            tahmin = tahmin[0]
            tahmin = round(tahmin, 2)
            değişim = ((tahmin - data['Close'][-1])/data['Close'][-1])*100
            if değişim > 50:

                send_telegram_message(symbol + " - forecast: " + str(tahmin)+" - son fiyat: "+str(data['Close'][-1])+" - değişim%: "+str(değişim))
            else:
                print(symbol+" - forecast: " + str(tahmin) + "son fiyat: "+str(data['Close'][-1])+" - değişim%: "+str(değişim))

        except Exception as e:
            print(e)

while True:
    if __name__ == '__main__':
        newone()
        send_telegram_message("Bugünlük bu kadar")
        time.sleep(14400)
