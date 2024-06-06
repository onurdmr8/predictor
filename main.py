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
from tabulate import tabulate
from binance.client import Client
from pmdarima import auto_arima



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
startdate = datetime.now() - timedelta(days=3)
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

cr_list = ['BTC-USD', 'ETH-USD', 'BNB-USD', 'BCC-USD', 'NEO-USD', 'LTC-USD', 'QTUM-USD', 'ADA-USD', 'XRP-USD',
               'EOS-USD', 'TUSD-USD', 'IOTA-USD', 'XLM-USD', 'ONT-USD', 'TRX-USD', 'ETC-USD', 'ICX-USD', 'VEN-USD',
               'NULS-USD', 'VET-USD', 'PAX-USD', 'BCHABC-USD', 'BCHSV-USD', 'USDC-USD', 'LINK-USD', 'WAVES-USD',
               'BTT-USD', 'USDS-USD', 'ONG-USD', 'HOT-USD', 'ZIL-USD', 'ZRX-USD', 'FET-USD', 'BAT-USD', 'XMR-USD',
               'ZEC-USD', 'IOST-USD', 'CELR-USD', 'DASH-USD', 'NANO-USD', 'OMG-USD', 'THETA-USD', 'ENJ-USD', 'MITH-USD',
               'MATIC-USD', 'ATOM-USD', 'TFUEL-USD', 'ONE-USD', 'FTM-USD', 'ALGO-USD', 'USDSB-USD', 'GTO-USD',
               'ERD-USD', 'DOGE-USD', 'DUSK-USD', 'ANKR-USD', 'WIN-USD', 'COS-USD', 'NPXS-USD', 'COCOS-USD', 'MTL-USD',
               'TOMO-USD', 'PERL-USD', 'DENT-USD', 'MFT-USD', 'KEY-USD', 'STORM-USD', 'DOCK-USD', 'WAN-USD', 'FUN-USD',
               'CVC-USD', 'CHZ-USD', 'BAND-USD', 'BUSD-USD', 'BEAM-USD', 'XTZ-USD', 'REN-USD', 'RVN-USD', 'HC-USD',
               'HBAR-USD', 'NKN-USD', 'STX-USD', 'KAVA-USD', 'ARPA-USD', 'IOTX-USD', 'RLC-USD', 'MCO-USD', 'CTXC-USD',
               'BCH-USD', 'TROY-USD', 'VITE-USD', 'FTT-USD', 'EUR-USD', 'OGN-USD', 'DREP-USD', 'BULL-USD', 'BEAR-USD',
               'ETHBULL-USD', 'ETHBEAR-USD', 'TCT-USD', 'WRX-USD', 'BTS-USD', 'LSK-USD', 'BNT-USD', 'LTO-USD',
               'EOSBULL-USD', 'EOSBEAR-USD', 'XRPBULL-USD', 'XRPBEAR-USD', 'STRAT-USD', 'AION-USD', 'MBL-USD',
               'COTI-USD', 'BNBBULL-USD', 'BNBBEAR-USD', 'STPT-USD', 'WTC-USD', 'DATA-USD', 'XZC-USD', 'SOL-USD',
               'CTSI-USD', 'HIVE-USD', 'CHR-USD', 'BTCUP-USD', 'BTCDOWN-USD', 'GXS-USD', 'ARDR-USD', 'LEND-USD',
               'MDT-USD', 'STMX-USD', 'KNC-USD', 'REP-USD', 'LRC-USD', 'PNT-USD', 'COMP-USD', 'BKRW-USD', 'SC-USD',
               'ZEN-USD', 'SNX-USD', 'ETHUP-USD', 'ETHDOWN-USD', 'ADAUP-USD', 'ADADOWN-USD', 'LINKUP-USD',
               'LINKDOWN-USD', 'VTHO-USD', 'DGB-USD', 'GBP-USD', 'SXP-USD', 'MKR-USD', 'DAI-USD', 'DCR-USD',
               'STORJ-USD', 'BNBUP-USD', 'BNBDOWN-USD', 'XTZUP-USD', 'XTZDOWN-USD', 'MANA-USD', 'AUD-USD', 'YFI-USD',
               'BAL-USD', 'BLZ-USD', 'IRIS-USD', 'KMD-USD', 'JST-USD', 'SRM-USD', 'ANT-USD', 'CRV-USD', 'SAND-USD',
               'OCEAN-USD', 'NMR-USD', 'DOT-USD', 'LUNA-USD', 'RSR-USD', 'PAXG-USD', 'WNXM-USD', 'TRB-USD', 'BZRX-USD',
               'SUSHI-USD', 'YFII-USD', 'KSM-USD', 'EGLD-USD', 'DIA-USD', 'RUNE-USD', 'FIO-USD', 'UMA-USD', 'EOSUP-USD',
               'EOSDOWN-USD', 'TRXUP-USD', 'TRXDOWN-USD', 'XRPUP-USD', 'XRPDOWN-USD', 'DOTUP-USD', 'DOTDOWN-USD',
               'BEL-USD', 'WING-USD', 'LTCUP-USD', 'LTCDOWN-USD', 'UNI-USD', 'NBS-USD', 'OXT-USD', 'SUN-USD',
               'AVAX-USD', 'HNT-USD', 'FLM-USD', 'UNIUP-USD', 'UNIDOWN-USD', 'ORN-USD', 'UTK-USD', 'XVS-USD',
               'ALPHA-USD', 'AAVE-USD', 'NEAR-USD', 'SXPUP-USD', 'SXPDOWN-USD', 'FIL-USD', 'FILUP-USD', 'FILDOWN-USD',
               'YFIUP-USD', 'YFIDOWN-USD', 'INJ-USD', 'AUDIO-USD', 'CTK-USD', 'BCHUP-USD', 'BCHDOWN-USD', 'AKRO-USD',
               'AXS-USD', 'HARD-USD', 'DNT-USD', 'STRAX-USD', 'UNFI-USD', 'ROSE-USD', 'AVA-USD', 'XEM-USD',
               'AAVEUP-USD', 'AAVEDOWN-USD', 'SKL-USD', 'SUSD-USD', 'SUSHIUP-USD', 'SUSHIDOWN-USD', 'XLMUP-USD',
               'XLMDOWN-USD', 'GRT-USD', 'JUV-USD', 'PSG-USD', '1INCH-USD', 'REEF-USD', 'OG-USD', 'ATM-USD', 'ASR-USD',
               'CELO-USD', 'RIF-USD', 'BTCST-USD', 'TRU-USD', 'CKB-USD', 'TWT-USD', 'FIRO-USD', 'LIT-USD', 'SFP-USD',
               'DODO-USD', 'CAKE-USD', 'ACM-USD', 'BADGER-USD', 'FIS-USD', 'OM-USD', 'POND-USD', 'DEGO-USD',
               'ALICE-USD', 'LINA-USD', 'PERP-USD', 'RAMP-USD', 'SUPER-USD', 'CFX-USD', 'EPS-USD', 'AUTO-USD',
               'TKO-USD', 'PUNDIX-USD', 'TLM-USD', '1INCHUP-USD', '1INCHDOWN-USD', 'BTG-USD', 'MIR-USD', 'BAR-USD',
               'FORTH-USD', 'BAKE-USD', 'BURGER-USD', 'SLP-USD', 'SHIB-USD', 'ICP-USD', 'AR-USD', 'POLS-USD', 'MDX-USD',
               'MASK-USD', 'LPT-USD', 'NU-USD', 'XVG-USD', 'ATA-USD', 'GTC-USD', 'TORN-USD', 'KEEP-USD', 'ERN-USD',
               'KLAY-USD', 'PHA-USD', 'BOND-USD', 'MLN-USD', 'DEXE-USD', 'C98-USD', 'CLV-USD', 'QNT-USD', 'FLOW-USD',
               'TVK-USD', 'MINA-USD', 'RAY-USD', 'FARM-USD', 'ALPACA-USD', 'QUICK-USD', 'MBOX-USD', 'FOR-USD',
               'REQ-USD', 'GHST-USD', 'WAXP-USD', 'TRIBE-USD', 'GNO-USD', 'XEC-USD', 'ELF-USD', 'DYDX-USD', 'POLY-USD',
               'IDEX-USD', 'VIDT-USD', 'USDP-USD', 'GALA-USD', 'ILV-USD', 'YGG-USD', 'SYS-USD', 'DF-USD', 'FIDA-USD',
               'FRONT-USD', 'CVP-USD', 'AGLD-USD', 'RAD-USD', 'BETA-USD', 'RARE-USD', 'LAZIO-USD', 'CHESS-USD',
               'ADX-USD', 'AUCTION-USD', 'DAR-USD', 'BNX-USD', 'RGT-USD', 'MOVR-USD', 'CITY-USD', 'ENS-USD', 'KP3R-USD',
               'QI-USD', 'PORTO-USD', 'POWR-USD', 'VGX-USD', 'JASMY-USD', 'AMP-USD', 'PLA-USD', 'PYR-USD', 'RNDR-USD',
               'ALCX-USD', 'SANTOS-USD', 'MC-USD', 'ANY-USD', 'BICO-USD', 'FLUX-USD', 'FXS-USD', 'VOXEL-USD',
               'HIGH-USD', 'CVX-USD', 'PEOPLE-USD', 'OOKI-USD', 'SPELL-USD', 'UST-USD', 'JOE-USD', 'ACH-USD', 'IMX-USD',
               'GLMR-USD', 'LOKA-USD', 'SCRT-USD', 'API3-USD', 'BTTC-USD', 'ACA-USD', 'ANC-USD', 'XNO-USD', 'WOO-USD',
               'ALPINE-USD', 'T-USD', 'ASTR-USD', 'GMT-USD', 'KDA-USD', 'APE-USD', 'BSW-USD', 'BIFI-USD', 'MULTI-USD',
               'STEEM-USD', 'MOB-USD', 'NEXO-USD', 'REI-USD', 'GAL-USD', 'LDO-USD', 'EPX-USD', 'OP-USD', 'LEVER-USD',
               'STG-USD', 'LUNC-USD', 'GMX-USD', 'NEBL-USD', 'POLYX-USD', 'APT-USD', 'OSMO-USD', 'HFT-USD', 'PHB-USD',
               'HOOK-USD', 'MAGIC-USD', 'HIFI-USD', 'RPL-USD', 'PROS-USD', 'AGIX-USD', 'GNS-USD', 'SYN-USD', 'VIB-USD',
               'SSV-USD', 'LQTY-USD', 'AMB-USD', 'BETH-USD', 'USTC-USD', 'GAS-USD', 'GLM-USD', 'PROM-USD', 'QKC-USD',
               'UFT-USD', 'ID-USD', 'ARB-USD', 'LOOM-USD', 'OAX-USD', 'RDNT-USD', 'WBTC-USD', 'EDU-USD', 'SUI-USD',
               'AERGO-USD', 'PEPE-USD', 'FLOKI-USD', 'AST-USD', 'SNT-USD', 'COMBO-USD', 'MAV-USD', 'PENDLE-USD',
               'ARKM-USD', 'WBETH-USD', 'WLD-USD', 'FDUSD-USD', 'SEI-USD', 'CYBER-USD', 'ARK-USD', 'CREAM-USD',
               'GFT-USD', 'IQ-USD', 'NTRN-USD', 'TIA-USD', 'MEME-USD', 'ORDI-USD', 'BEAMX-USD', 'PIVX-USD', 'VIC-USD',
               'BLUR-USD', 'VANRY-USD', 'AEUR-USD', 'JTO-USD', '1000SATS-USD', 'BONK-USD', 'ACE-USD', 'NFP-USD',
               'AI-USD', 'XAI-USD', 'MANTA-USD', 'ALT-USD', 'JUP-USD', 'PYTH-USD', 'RONIN-USD', 'DYM-USD', 'PIXEL-USD',
               'STRK-USD', 'PORTAL-USD', 'PDA-USD', 'AXL-USD', 'WIF-USD', 'METIS-USD', 'AEVO-USD', 'BOME-USD',
               'ETHFI-USD', 'ENA-USD', 'W-USD', 'TNSR-USD', 'SAGA-USD', 'TAO-USD', 'OMNI-USD', 'REZ-USD', 'BB-USD',
               'NOT-USD']
c=cr_list

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

        cr_list=['BTC-USD', 'ETH-USD', 'BNB-USD', 'BCC-USD', 'NEO-USD', 'LTC-USD', 'QTUM-USD', 'ADA-USD', 'XRP-USD', 'EOS-USD', 'TUSD-USD', 'IOTA-USD', 'XLM-USD', 'ONT-USD', 'TRX-USD', 'ETC-USD', 'ICX-USD', 'VEN-USD', 'NULS-USD', 'VET-USD', 'PAX-USD', 'BCHABC-USD', 'BCHSV-USD', 'USDC-USD', 'LINK-USD', 'WAVES-USD', 'BTT-USD', 'USDS-USD', 'ONG-USD', 'HOT-USD', 'ZIL-USD', 'ZRX-USD', 'FET-USD', 'BAT-USD', 'XMR-USD', 'ZEC-USD', 'IOST-USD', 'CELR-USD', 'DASH-USD', 'NANO-USD', 'OMG-USD', 'THETA-USD', 'ENJ-USD', 'MITH-USD', 'MATIC-USD', 'ATOM-USD', 'TFUEL-USD', 'ONE-USD', 'FTM-USD', 'ALGO-USD', 'USDSB-USD', 'GTO-USD', 'ERD-USD', 'DOGE-USD', 'DUSK-USD', 'ANKR-USD', 'WIN-USD', 'COS-USD', 'NPXS-USD', 'COCOS-USD', 'MTL-USD', 'TOMO-USD', 'PERL-USD', 'DENT-USD', 'MFT-USD', 'KEY-USD', 'STORM-USD', 'DOCK-USD', 'WAN-USD', 'FUN-USD', 'CVC-USD', 'CHZ-USD', 'BAND-USD', 'BUSD-USD', 'BEAM-USD', 'XTZ-USD', 'REN-USD', 'RVN-USD', 'HC-USD', 'HBAR-USD', 'NKN-USD', 'STX-USD', 'KAVA-USD', 'ARPA-USD', 'IOTX-USD', 'RLC-USD', 'MCO-USD', 'CTXC-USD', 'BCH-USD', 'TROY-USD', 'VITE-USD', 'FTT-USD', 'EUR-USD', 'OGN-USD', 'DREP-USD', 'BULL-USD', 'BEAR-USD', 'ETHBULL-USD', 'ETHBEAR-USD', 'TCT-USD', 'WRX-USD', 'BTS-USD', 'LSK-USD', 'BNT-USD', 'LTO-USD', 'EOSBULL-USD', 'EOSBEAR-USD', 'XRPBULL-USD', 'XRPBEAR-USD', 'STRAT-USD', 'AION-USD', 'MBL-USD', 'COTI-USD', 'BNBBULL-USD', 'BNBBEAR-USD', 'STPT-USD', 'WTC-USD', 'DATA-USD', 'XZC-USD', 'SOL-USD', 'CTSI-USD', 'HIVE-USD', 'CHR-USD', 'BTCUP-USD', 'BTCDOWN-USD', 'GXS-USD', 'ARDR-USD', 'LEND-USD', 'MDT-USD', 'STMX-USD', 'KNC-USD', 'REP-USD', 'LRC-USD', 'PNT-USD', 'COMP-USD', 'BKRW-USD', 'SC-USD', 'ZEN-USD', 'SNX-USD', 'ETHUP-USD', 'ETHDOWN-USD', 'ADAUP-USD', 'ADADOWN-USD', 'LINKUP-USD', 'LINKDOWN-USD', 'VTHO-USD', 'DGB-USD', 'GBP-USD', 'SXP-USD', 'MKR-USD', 'DAI-USD', 'DCR-USD', 'STORJ-USD', 'BNBUP-USD', 'BNBDOWN-USD', 'XTZUP-USD', 'XTZDOWN-USD', 'MANA-USD', 'AUD-USD', 'YFI-USD', 'BAL-USD', 'BLZ-USD', 'IRIS-USD', 'KMD-USD', 'JST-USD', 'SRM-USD', 'ANT-USD', 'CRV-USD', 'SAND-USD', 'OCEAN-USD', 'NMR-USD', 'DOT-USD', 'LUNA-USD', 'RSR-USD', 'PAXG-USD', 'WNXM-USD', 'TRB-USD', 'BZRX-USD', 'SUSHI-USD', 'YFII-USD', 'KSM-USD', 'EGLD-USD', 'DIA-USD', 'RUNE-USD', 'FIO-USD', 'UMA-USD', 'EOSUP-USD', 'EOSDOWN-USD', 'TRXUP-USD', 'TRXDOWN-USD', 'XRPUP-USD', 'XRPDOWN-USD', 'DOTUP-USD', 'DOTDOWN-USD', 'BEL-USD', 'WING-USD', 'LTCUP-USD', 'LTCDOWN-USD', 'UNI-USD', 'NBS-USD', 'OXT-USD', 'SUN-USD', 'AVAX-USD', 'HNT-USD', 'FLM-USD', 'UNIUP-USD', 'UNIDOWN-USD', 'ORN-USD', 'UTK-USD', 'XVS-USD', 'ALPHA-USD', 'AAVE-USD', 'NEAR-USD', 'SXPUP-USD', 'SXPDOWN-USD', 'FIL-USD', 'FILUP-USD', 'FILDOWN-USD', 'YFIUP-USD', 'YFIDOWN-USD', 'INJ-USD', 'AUDIO-USD', 'CTK-USD', 'BCHUP-USD', 'BCHDOWN-USD', 'AKRO-USD', 'AXS-USD', 'HARD-USD', 'DNT-USD', 'STRAX-USD', 'UNFI-USD', 'ROSE-USD', 'AVA-USD', 'XEM-USD', 'AAVEUP-USD', 'AAVEDOWN-USD', 'SKL-USD', 'SUSD-USD', 'SUSHIUP-USD', 'SUSHIDOWN-USD', 'XLMUP-USD', 'XLMDOWN-USD', 'GRT-USD', 'JUV-USD', 'PSG-USD', '1INCH-USD', 'REEF-USD', 'OG-USD', 'ATM-USD', 'ASR-USD', 'CELO-USD', 'RIF-USD', 'BTCST-USD', 'TRU-USD', 'CKB-USD', 'TWT-USD', 'FIRO-USD', 'LIT-USD', 'SFP-USD', 'DODO-USD', 'CAKE-USD', 'ACM-USD', 'BADGER-USD', 'FIS-USD', 'OM-USD', 'POND-USD', 'DEGO-USD', 'ALICE-USD', 'LINA-USD', 'PERP-USD', 'RAMP-USD', 'SUPER-USD', 'CFX-USD', 'EPS-USD', 'AUTO-USD', 'TKO-USD', 'PUNDIX-USD', 'TLM-USD', '1INCHUP-USD', '1INCHDOWN-USD', 'BTG-USD', 'MIR-USD', 'BAR-USD', 'FORTH-USD', 'BAKE-USD', 'BURGER-USD', 'SLP-USD', 'SHIB-USD', 'ICP-USD', 'AR-USD', 'POLS-USD', 'MDX-USD', 'MASK-USD', 'LPT-USD', 'NU-USD', 'XVG-USD', 'ATA-USD', 'GTC-USD', 'TORN-USD', 'KEEP-USD', 'ERN-USD', 'KLAY-USD', 'PHA-USD', 'BOND-USD', 'MLN-USD', 'DEXE-USD', 'C98-USD', 'CLV-USD', 'QNT-USD', 'FLOW-USD', 'TVK-USD', 'MINA-USD', 'RAY-USD', 'FARM-USD', 'ALPACA-USD', 'QUICK-USD', 'MBOX-USD', 'FOR-USD', 'REQ-USD', 'GHST-USD', 'WAXP-USD', 'TRIBE-USD', 'GNO-USD', 'XEC-USD', 'ELF-USD', 'DYDX-USD', 'POLY-USD', 'IDEX-USD', 'VIDT-USD', 'USDP-USD', 'GALA-USD', 'ILV-USD', 'YGG-USD', 'SYS-USD', 'DF-USD', 'FIDA-USD', 'FRONT-USD', 'CVP-USD', 'AGLD-USD', 'RAD-USD', 'BETA-USD', 'RARE-USD', 'LAZIO-USD', 'CHESS-USD', 'ADX-USD', 'AUCTION-USD', 'DAR-USD', 'BNX-USD', 'RGT-USD', 'MOVR-USD', 'CITY-USD', 'ENS-USD', 'KP3R-USD', 'QI-USD', 'PORTO-USD', 'POWR-USD', 'VGX-USD', 'JASMY-USD', 'AMP-USD', 'PLA-USD', 'PYR-USD', 'RNDR-USD', 'ALCX-USD', 'SANTOS-USD', 'MC-USD', 'ANY-USD', 'BICO-USD', 'FLUX-USD', 'FXS-USD', 'VOXEL-USD', 'HIGH-USD', 'CVX-USD', 'PEOPLE-USD', 'OOKI-USD', 'SPELL-USD', 'UST-USD', 'JOE-USD', 'ACH-USD', 'IMX-USD', 'GLMR-USD', 'LOKA-USD', 'SCRT-USD', 'API3-USD', 'BTTC-USD', 'ACA-USD', 'ANC-USD', 'XNO-USD', 'WOO-USD', 'ALPINE-USD', 'T-USD', 'ASTR-USD', 'GMT-USD', 'KDA-USD', 'APE-USD', 'BSW-USD', 'BIFI-USD', 'MULTI-USD', 'STEEM-USD', 'MOB-USD', 'NEXO-USD', 'REI-USD', 'GAL-USD', 'LDO-USD', 'EPX-USD', 'OP-USD', 'LEVER-USD', 'STG-USD', 'LUNC-USD', 'GMX-USD', 'NEBL-USD', 'POLYX-USD', 'APT-USD', 'OSMO-USD', 'HFT-USD', 'PHB-USD', 'HOOK-USD', 'MAGIC-USD', 'HIFI-USD', 'RPL-USD', 'PROS-USD', 'AGIX-USD', 'GNS-USD', 'SYN-USD', 'VIB-USD', 'SSV-USD', 'LQTY-USD', 'AMB-USD', 'BETH-USD', 'USTC-USD', 'GAS-USD', 'GLM-USD', 'PROM-USD', 'QKC-USD', 'UFT-USD', 'ID-USD', 'ARB-USD', 'LOOM-USD', 'OAX-USD', 'RDNT-USD', 'WBTC-USD', 'EDU-USD', 'SUI-USD', 'AERGO-USD', 'PEPE-USD', 'FLOKI-USD', 'AST-USD', 'SNT-USD', 'COMBO-USD', 'MAV-USD', 'PENDLE-USD', 'ARKM-USD', 'WBETH-USD', 'WLD-USD', 'FDUSD-USD', 'SEI-USD', 'CYBER-USD', 'ARK-USD', 'CREAM-USD', 'GFT-USD', 'IQ-USD', 'NTRN-USD', 'TIA-USD', 'MEME-USD', 'ORDI-USD', 'BEAMX-USD', 'PIVX-USD', 'VIC-USD', 'BLUR-USD', 'VANRY-USD', 'AEUR-USD', 'JTO-USD', '1000SATS-USD', 'BONK-USD', 'ACE-USD', 'NFP-USD', 'AI-USD', 'XAI-USD', 'MANTA-USD', 'ALT-USD', 'JUP-USD', 'PYTH-USD', 'RONIN-USD', 'DYM-USD', 'PIXEL-USD', 'STRK-USD', 'PORTAL-USD', 'PDA-USD', 'AXL-USD', 'WIF-USD', 'METIS-USD', 'AEVO-USD', 'BOME-USD', 'ETHFI-USD', 'ENA-USD', 'W-USD', 'TNSR-USD', 'SAGA-USD', 'TAO-USD', 'OMNI-USD', 'REZ-USD', 'BB-USD', 'NOT-USD']

        for i in usdt_pairs:
            i = i.replace("USDT", "-USD")

            cr_list.append(i)
        print(cr_list)

        return usdt_pairs
    def binance_api(endpoint, params=None):
        headers = {'X-MBX-APIKEY': api_key}
        response = requests.get(endpoint, headers=headers, params=params)
        return json.loads(response.text)
    usdt_pairs = cr_list
    b=bist
    c = usdt_pairs
    symbols = c
    random.shuffle(symbols)
    aralık = 4*4
    interval = "15m"
    say = 0
    say2 = str(len(symbols))

    for symbol in symbols:
        try:
            say += 1
            ilerleme = f"{say}/{say2}"
            print(Fore.MAGENTA + symbol + "-" + Fore.LIGHTBLUE_EX + ilerleme + Style.RESET_ALL)

            # Download data from Yahoo Finance
            data = yf.download(symbol, start=startdate, progress=False, interval=interval, end=end)

            # Calculate KDJ indicators
            data['K'] = data['Close'].shift(1)
            data['D'] = data['K'].rolling(3).mean()
            data['J'] = (3 * data['K'] + 2 * data['D'] + data['Close']) / 6

            # Convert to float and drop NaN values
            data = data.astype(float).dropna()

            # Determine initial KDJ score
            if data['J'].iloc[0] > 80:
                puan1 = -1
            elif data['J'].iloc[0] > 20 and data['J'].iloc[0] < 80:
                puan1 = 0
            elif data['J'].iloc[0] < 20:
                puan1 = 1
            else:
                print("KDJ not satisfied.")
                puan1 = 0

            # Check if J > D and J > K
            if data['J'].iloc[0] > data['D'].iloc[0] and data['J'].iloc[0] > data['K'].iloc[0]:
                puan2= 1
            else:
                puan2 = 0

            # Calculate EMAs and assign score based on their relationship
            data['EMA20'] = data['Close'].ewm(span=20, adjust=False).mean()
            data['EMA50'] = data['Close'].ewm(span=50, adjust=False).mean()
            data['EMA120'] = data['Close'].ewm(span=120, adjust=False).mean()
            data.dropna(inplace=True)

            if (data['EMA20'].iloc[0] > data['EMA50'].iloc[0] > data['EMA120'].iloc[0]
                    and data['EMA20'].iloc[1] < data['EMA50'].iloc[1]):
                puan3 = 1
            elif (data['EMA20'].iloc[0] < data['EMA50'].iloc[0] < data['EMA120'].iloc[0]
                    and data['EMA20'].iloc[1] > data['EMA50'].iloc[1]):
                puan3=-1
            else:
                puan3= 0
            # Calculate MACD and adjust score
            data['EMA12'] = data['Close'].ewm(span=12, adjust=False).mean()
            data['EMA26'] = data['Close'].ewm(span=26, adjust=False).mean()
            data['MACD'] = data['EMA12'] - data['EMA26']

            if data['MACD'].iloc[0] > 0:
                puan4 = 1
            else:
                puan4 = 0


            puan = puan1 + puan2 + puan3 + puan4

            if puan >= 2:

                print(Fore.GREEN + f"{symbol} {puan}" + Style.RESET_ALL)
                model=auto_arima(data['Close'],
                                 start_p=1, start_q=1, max_p=3, max_q=3, m=aralık, start_P=0,
                                 seasonal=True, d=1, D=1, trace=False, error_action='ignore',
                                 suppress_warnings=True, stepwise=True)
                model.fit(data['Close'])
                future_forecast = model.predict(n_periods=aralık)
                sonfiyat=data['Close'].iloc[-1]
                forecastsonfiyat=future_forecast.iloc[-1]

                if forecastsonfiyat > sonfiyat:
                    difference_percent = ((forecastsonfiyat - sonfiyat) / sonfiyat) * 100

                    if difference_percent > 20:
                        send_telegram_message(f"BUY {symbol} puan:{puan} forecast: {future_forecast.iloc[-1]} son fiyat: {data['Close'].iloc[-1]}")
                        print(Fore.GREEN + f"{symbol} {puan}" + Style.RESET_ALL)
                    else:

                        print("yeterli yükseliş görülmedi")
                else:
                    print("yükseliş yok")
            else:
                print(Fore.RED + f"{symbol} {puan}" + Style.RESET_ALL)

        except Exception as e:
            print(e)



if __name__ == "__main__":
    while True:
        newone()
