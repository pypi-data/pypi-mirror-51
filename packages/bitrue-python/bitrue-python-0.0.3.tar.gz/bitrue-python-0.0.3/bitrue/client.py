# coding=utf-8
import sys
import logging
import configparser
from tabulate import tabulate
import multiprocessing as mp
from selenium import webdriver
import hashlib
import hmac
import requests
import time
from operator import itemgetter
from .helpers import date_to_milliseconds, interval_to_milliseconds
from .exceptions import BitrueAPIException, BitrueRequestException, BitrueWithdrawException
import atexit
from multiprocessing import Queue
from apscheduler.schedulers.background import BackgroundScheduler
from selenium.webdriver.firefox.options import Options as FireFox_Options
from selenium.webdriver.chrome.options import Options as Chrome_Options
import os

q = Queue()

class Client(object):

    API_URL = 'https://www.bitrue.com/api'
    WITHDRAW_API_URL = 'https://api.bitrue.com/wapi'
    WEBSITE_URL = 'https://www.bitrue.com'
    PUBLIC_API_VERSION = 'v1'
    PRIVATE_API_VERSION = 'v1'
    WITHDRAW_API_VERSION = 'v1'  #NOT ACTIVE

    SYMBOL_TYPE_SPOT = 'SPOT'

    ORDER_STATUS_NEW = 'NEW'
    ORDER_STATUS_PARTIALLY_FILLED = 'PARTIALLY_FILLED'
    ORDER_STATUS_FILLED = 'FILLED'
    ORDER_STATUS_CANCELED = 'CANCELED'
    ORDER_STATUS_PENDING_CANCEL = 'PENDING_CANCEL'
    ORDER_STATUS_REJECTED = 'REJECTED'
    ORDER_STATUS_EXPIRED = 'EXPIRED'

    KLINE_INTERVAL_1MINUTE = '1m'
    #KLINE_INTERVAL_3MINUTE = '3m'
    KLINE_INTERVAL_5MINUTE = '5m'
    KLINE_INTERVAL_15MINUTE = '15m'
    KLINE_INTERVAL_30MINUTE = '30m'
    KLINE_INTERVAL_1HOUR = '1h'
    #KLINE_INTERVAL_2HOUR = '2h'
    #KLINE_INTERVAL_4HOUR = '4h'
    #KLINE_INTERVAL_6HOUR = '6h'
    #KLINE_INTERVAL_8HOUR = '8h'
    #KLINE_INTERVAL_12HOUR = '12h'
    KLINE_INTERVAL_1DAY = '1d'
    #KLINE_INTERVAL_3DAY = '3d'
    KLINE_INTERVAL_1WEEK = '1w'
    KLINE_INTERVAL_1MONTH = '1M'

    SIDE_BUY = 'BUY'
    SIDE_SELL = 'SELL'

    ORDER_TYPE_LIMIT = 'LIMIT'
    ORDER_TYPE_MARKET = 'MARKET'
    ORDER_TYPE_STOP_LOSS = 'STOP_LOSS'
    ORDER_TYPE_STOP_LOSS_LIMIT = 'STOP_LOSS_LIMIT'
    ORDER_TYPE_TAKE_PROFIT = 'TAKE_PROFIT'
    ORDER_TYPE_TAKE_PROFIT_LIMIT = 'TAKE_PROFIT_LIMIT'
    ORDER_TYPE_LIMIT_MAKER = 'LIMIT_MAKER'

    TIME_IN_FORCE_GTC = 'GTC'  # Good till cancelled
    TIME_IN_FORCE_IOC = 'IOC'  # Immediate or cancel
    TIME_IN_FORCE_FOK = 'FOK'  # Fill or kill

    ORDER_RESP_TYPE_ACK = 'ACK'
    ORDER_RESP_TYPE_RESULT = 'RESULT'
    ORDER_RESP_TYPE_FULL = 'FULL'

    # For accessing the data returned by Client.aggregate_trades().
    AGG_ID = 'a'
    AGG_PRICE = 'p'
    AGG_QUANTITY = 'q'
    AGG_FIRST_TRADE_ID = 'f'
    AGG_LAST_TRADE_ID = 'l'
    AGG_TIME = 'T'
    AGG_BUYER_MAKES = 'm'
    AGG_BEST_MATCH = 'M'

    def __init__(self, api_key, api_secret, requests_params=None, coil_enabled=True, headless=True, browser='firefox'):
        atexit.register(self._close_coil)

        """
        Bitrue API Client constructor

                :param api_key: Api Key
                :type api_key: str.
                :param api_secret: Api Secret
                :type api_secret: str.
                :param requests_params: optional - Dictionary of requests params to use for all calls
                :type requests_params: dict.
                :param coil_enabled: optional - Brings up firefox browser (headless) for streaming payments.
                :type coil_enabled: str

        """


        self.API_KEY = api_key
        self.API_SECRET = api_secret
        self.session = self._init_session()
        self._requests_params = requests_params
        self.ff_coil_extId = 'coilfirefoxextension@coil.com.xpi'
        self.chrome_coil_extId = 'locbifcbeldmnphbgkdigjmkbfkhbnca'
        self.chrome_coil_extId = 'locbifcbeldmnphbgkdigjmkbfkhbnca'
        self.chrome_bin = '/usr/bin/google-chrome-stable'

        # Locations
        self.coilurl = 'https://coil.com/p/nerf_herder/Python-Package-Coil-Enabled/GRn2W-j5t'


        self.gecko_source_win64 = 'https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-win64.zip'
        self.gecko_source_linux64 = 'https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz'
        self.gecko_source_linux32 = 'https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux32.tar.gz'

        self.chrome_driver74_win_url = 'https://chromedriver.storage.googleapis.com/74.0.3729.6/chromedriver_win32.zip'
        self.chrome_driver74_mac_url = 'https://chromedriver.storage.googleapis.com/74.0.3729.6/chromedriver_mac64.zip'
        self.chrome_driver74_linux_url = 'https://chromedriver.storage.googleapis.com/74.0.3729.6/chromedriver_linux64.zip'

        self.chrome_driver75_win_url = 'https://chromedriver.storage.googleapis.com/75.0.3770.8/chromedriver_win32.zip'
        self.chrome_driver75_mac_url = 'https://chromedriver.storage.googleapis.com/75.0.3770.8/chromedriver_mac64.zip'
        self.chrome_driver75_linux_url = 'https://chromedriver.storage.googleapis.com/75.0.3770.8/chromedriver_linux64.zip'

        self.chrome_driver76_win_url = 'https://chromedriver.storage.googleapis.com/76.0.3809.12/chromedriver_win32.zip'
        self.chrome_driver76_mac_url = 'https://chromedriver.storage.googleapis.com/76.0.3809.12/chromedriver_mac64.zip'
        self.chrome_driver76_linux_url = 'https://chromedriver.storage.googleapis.com/76.0.3809.12/chromedriver_linux64.zip'

        # init DNS and SSL cert
        self.ping()
        if coil_enabled:
            # self.open_coil()
            self.p1_coil = mp.Process(target=self.open_coil, args=(q,headless,browser,))
            self.p1_coil.daemon = True
            self.p1_coil.start()

            # threading.Thread(target=self.open_coil())
        else:
            logging.warning('Consider signing up for Coil when using pyton-bitrue as a contribution. \n https://coil.com/signup ')



    def _init_session(self):

        session = requests.session()
        session.headers.update({'Accept': 'application/json',
                                    'User-Agent': 'bitrue/python',
                                'X-MBX-APIKEY': self.API_KEY})
        return session

    def _close_coil(self):
        q.put('goodbye')
        # return self.p1_coil.join()

    def _create_api_uri(self, path, signed=True, version=PUBLIC_API_VERSION):
        v = self.PRIVATE_API_VERSION if signed else version
        return self.API_URL + '/' + v + '/' + path

    def _create_withdraw_api_uri(self, path):
        return self.WITHDRAW_API_URL + '/' + self.WITHDRAW_API_VERSION + '/' + path

    def _create_website_uri(self, path):
        return self.WEBSITE_URL + '/' + path

    def _generate_signature(self, data):

        ordered_data = self._order_params(data)
        query_string = '&'.join(["{}={}".format(d[0], d[1]) for d in ordered_data])
        m = hmac.new(self.API_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256)
        return m.hexdigest()

    def file_zunip(self, file, path):
        import zipfile
        zip_ref = zipfile.ZipFile(file, 'r')
        zip_ref.extractall(path=path)
        zip_ref.close()

    def file_unzip_tar(self, file, path):
        import tarfile
        file = tarfile.open(file)
        file.extractall(path=path)
        file.close()

    def get_coil_url(self):
        return self.driver.get(self.coilurl)

    def get_firefox_profile_dir(self):
        from pathlib import Path
        self.gecko_path = os.path.dirname(__file__)

        if sys.platform in ['linux', 'linux2']:
            import subprocess

            self.ff_gecko = Path(self.gecko_path + '/geckodriver')

            bits = 'uname -m'
            ver_32_64 = subprocess.getstatusoutput(bits)

            cmd = "ls -d /home/$USER/.mozilla/firefox/*.default/"
            fp = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
            FF_PRF_DIR = fp.communicate()[0][0:-2]
            FF_PRF_DIR_DEFAULT = str(FF_PRF_DIR, 'utf-8')

            ff_ext_path = os.path.join(FF_PRF_DIR_DEFAULT, 'extensions')
            self.ff_coil_loc = os.path.join(ff_ext_path, self.ff_coil_extId)
            ff_coil_enabled = os.path.exists(self.ff_coil_loc)
            if ff_coil_enabled:
                if 'x86_64' in ver_32_64:
                    if not self.ff_gecko.is_file():
                        import wget
                        self.gecko_targz = self.gecko_path + '/' + self.gecko_source_linux64.split('/')[-1]
                        wget.download(self.gecko_source_linux64, self.gecko_path)
                        self.file_unzip_tar(self.gecko_path + '/' + self.gecko_targz)
                        os.remove(self.gecko_path + '/' + self.gecko_targz)
                    if self.ff_gecko.is_file():
                            self.data_path = FF_PRF_DIR_DEFAULT
                            self.gecko = self.ff_gecko

                if 'i368' in ver_32_64:
                    if not self.ff_gecko.is_file():
                        import wget
                        self.gecko_targz = self.gecko_path + '/' + self.gecko_source_linux32.split('/')[-1]
                        wget.download(self.gecko_source_linux32, self.gecko_path)
                        self.file_unzip_tar(self.gecko_path + '/' + self.gecko_targz)
                        os.remove(self.gecko_path + '/' + self.gecko_targz)
                    if self.ff_gecko.is_file():
                            self.data_path = FF_PRF_DIR_DEFAULT
                            self.gecko = self.ff_gecko

        elif sys.platform == 'win32' or 'nt': 
            from pathlib import Path
            self.gecko = self.gecko_path + "\geckodriver.exe"
            mozilla_profile = os.path.join(os.getenv('APPDATA'), r'Mozilla\Firefox')
            mozilla_profile_ini = os.path.join(mozilla_profile, r'profiles.ini')
            profile = configparser.ConfigParser()
            profile.read(mozilla_profile_ini)
            FF_PRF_DIR_DEFAULT = os.path.normpath(os.path.join(mozilla_profile, profile.get('Profile0', 'Path')))
            ff_ext_path = os.path.join(FF_PRF_DIR_DEFAULT, 'extensions')
            self.ff_coil_loc = os.path.join(ff_ext_path, self.ff_coil_extId)
            ff_coil_enabled = os.path.exists(self.ff_coil_loc)

            if ff_coil_enabled:
                ff_gecko = Path(self.gecko)
                if ff_gecko.is_file():
                    self.data_path = FF_PRF_DIR_DEFAULT
                else:
                    import wget
                    wget.download(self.gecko_source_win64,self.gecko_path)
                    gecko_win64zip = self.gecko_path + '\\' + self.gecko_source_win64.split('/')[-1]
                    self.file_zunip(gecko_win64zip, self.gecko_path)
                    if ff_gecko.is_file():
                        os.remove(gecko_win64zip)
                        self.data_path = FF_PRF_DIR_DEFAULT


    def get_chrome_profile_dir(self):
        from pathlib import Path
        self.chrome_driver_dir = os.path.dirname(__file__)

        if sys.platform in ['linux', 'linux2']:
            import subprocess
            self.chromedriver = 'chromedriver'
            chrome_ver = subprocess.Popen("google-chrome --version", stdout=subprocess.PIPE, universal_newlines=True,
                                          shell=True).communicate()[0]
            chrome_ver = chrome_ver.replace('Google Chrome ', '')
            chrome_ver = chrome_ver.split('.')[0]
            self.chrome_driver_file_path = self.chrome_driver_dir + self.chromedriver + chrome_ver
            self.chrome_driver76_linux_url = 'https://chromedriver.storage.googleapis.com/76.0.3809.12/chromedriver_linux64.zip'

            if not Path.is_file(self.chrome_driver_file_path):
                import wget
                self.chrome_zip = 'chromedriver_linux64.zip'
                self.chrome_url = 'self.chrome_driver' + chrome_ver + 'linux_url'
                if chrome_ver == '76':
                    getattr(wget,'download')(self.chrome_url)
                    # wget.download(self.chrome_url, self.chrome_driver_dir)
                    self.file_zunip(self.chrome_driver_file_path + '/' + self.chrome_zip)
                    os.remove(self.chrome_driver_file_path + '/' + self.chrome_zip)
                    os.rename('chromedriver','chromedriver' + chrome_ver)
                elif chrome_ver == '75':
                    wget.download(self.chrome_driver75_linux_url)
                elif chrome_ver == '74':
                    wget.download(self.chrome_driver74_linux_url)
        elif sys.platform in ['win32']:
            
            self.chrome_winzip = 'chromedriver_win32.zip'
            chrome_driver_exe = 'chromedriver.exe'
            
            self.chrome_profile = os.path.join(os.getenv('LOCALAPPDATA'), r'Google\Chrome\User Data\Default')
            self.chrome_profile_ext = os.path.join(self.chrome_profile, r'Extensions')
            self.coil_ext_id = 'locbifcbeldmnphbgkdigjmkbfkhbnca'
            self.coil_ext_id_path = os.path.join(self.chrome_profile_ext, self.coil_ext_id)
            if os.path.isdir(self.coil_ext_id_path):
                # CHECK CHROME VERSION
                chrome_ver = os.popen(
                    r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version').read()
                chrome_ver = chrome_ver.split(r'REG_SZ')[1]
                chrome_ver = chrome_ver.split('.')[0].replace(' ', '')

            if chrome_ver == '76':
                chrome_driver_ver_exe = 'chromedriver76.exe'

                if not os.path.isfile(self.chrome_driver_dir + '\\' + chrome_driver_ver_exe):  # DOWNLOAD CHROMEDRIVER
                    import wget
                    wget.download(self.chrome_driver76_win_url, self.chrome_driver_dir)
                    self.file_zunip(self.chrome_driver_dir + '\\' + self.chrome_winzip,
                                    self.chrome_driver_dir)
                    os.rename(self.chrome_driver_dir + '\\' + chrome_driver_exe,
                              self.chrome_driver_dir + '\\' + chrome_driver_ver_exe)
                    os.remove(self.chrome_driver_dir + '\\' + self.chrome_winzip)
                if os.path.isfile(self.chrome_driver_dir + '\\' + chrome_driver_ver_exe):
                    self.chrome_profile = os.path.join(os.getenv('LOCALAPPDATA'),r'Google\Chrome\User Data')
                    self.options.add_argument("user-data-dir=" + self.chrome_profile)
                    self.driver = webdriver.Chrome(chrome_options=self.options,executable_path=self.chrome_driver_dir + '\\' + chrome_driver_ver_exe)

            elif chrome_ver == '75':
                chrome_driver_ver_exe = 'chromedriver75.exe'

                if not os.path.isfile(self.chrome_driver_dir + '\\' + chrome_driver_ver_exe):  # DOWNLOAD CHROMEDRIVER
                    import wget
                    wget.download(self.chrome_driver75_win_url, self.chrome_driver_dir)
                    self.file_zunip(self.chrome_driver_dir + '\\' + self.chrome_winzip,
                                    self.chrome_driver_dir)
                    os.rename(self.chrome_driver_dir + '\\' + chrome_driver_exe,
                              self.chrome_driver_dir + '\\' + chrome_driver_ver_exe)
                    os.remove(self.chrome_driver_dir + '\\' + self.chrome_winzip)
                if os.path.isfile(self.chrome_driver_dir + '\\' + chrome_driver_ver_exe):
                    self.chrome_profile = os.path.join(os.getenv('LOCALAPPDATA'),r'Google\Chrome\User Data')
                    self.options.add_argument("user-data-dir=" + self.chrome_profile)
                    self.driver = webdriver.Chrome(chrome_options=self.options,executable_path=self.chrome_driver_dir + '\\' + chrome_driver_ver_exe)

            elif chrome_ver == '74':
                chrome_driver_ver_exe = 'chromedriver74.exe'
                if not os.path.isfile(self.chrome_driver_dir + '\\' + chrome_driver_ver_exe):  # DOWNLOAD CHROMEDRIVER
                    import wget
                    wget.download(self.chrome_driver74_win_url, self.chrome_driver_dir)
                    self.file_zunip(self.chrome_driver_dir + '\\' + self.chrome_winzip, self.chrome_driver_dir)
                    os.rename(self.chrome_driver_dir + '\\' + chrome_driver_exe,
                              self.chrome_driver_dir + '\\' + chrome_driver_ver_exe)
                    os.remove(self.chrome_driver_dir + '\\' + self.chrome_winzip)
                if os.path.isfile(self.chrome_driver_dir + '\\' + chrome_driver_ver_exe):
                    self.chrome_profile = os.path.join(os.getenv('LOCALAPPDATA'),r'Google\Chrome\User Data')
                    self.options.add_argument("user-data-dir=" + self.chrome_profile)
                    self.driver = webdriver.Chrome(chrome_options=self.options,executable_path=self.chrome_driver_dir + '\\' + chrome_driver_ver_exe)

            else:
                logging.info('No Chrome browser supported')


    def schedule(self):
        scheduler = BackgroundScheduler() # SCHEDULE PAGE REFRESH EVERY 5 MINS
        scheduler.add_job(self.get_coil_url, 'interval',seconds=300)
        scheduler.start()
    def open_coil(self, q, headless=True, browser='firefox'):

        if browser == 'chrome':
            try:
                self.options = webdriver.chrome.options.Options()
                self.options.headless = headless
                self.get_chrome_profile_dir()
                self.driver.get(self.coilurl)  # OPEN URL
                self.schedule()
            except:
                logging.info('No Chrome Browser Supported for Coil')
        elif browser == 'firefox':
            try: # firefox + coil
                self.options = FireFox_Options()
                self.options.headless = headless
                self.get_firefox_profile_dir()
                self.driver = webdriver.Firefox(options=self.options, firefox_profile=self.data_path, executable_path=self.gecko)
                # FIX TO ENSURE EXTENSION LOADS.
                self.driver.get(self.coilurl)  # OPEN URL
                time.sleep(3)
                self.driver.install_addon(self.coil_ext_id_path)
                # END FIX TO ENSURE EXTENSION LOADS.
                self.driver.get(self.coilurl)  # OPEN URL
                self.schedule()

            except:
                logging.info('No \' Firefox Browser\' Supported for Coil')

        while True:
            if q.empty():
                pass
            else:
                print(q)
                self.driver.close()

    def _order_params(self, data):
        """Convert params to list with signature as last element

        :param data:
        :return:

        """
        has_signature = False
        params = []
        for key, value in data.items():
            if key == 'signature':
                has_signature = True
            else:
                params.append((key, value))
        # sort parameters by key
        params.sort(key=itemgetter(0))
        if has_signature:
            params.append(('signature', data['signature']))
        return params

    def _request(self, method, uri, signed, force_params=False, **kwargs):

        # set default requests timeout
        kwargs['timeout'] = 10

        # add our global requests params
        if self._requests_params:
            kwargs.update(self._requests_params)

        data = kwargs.get('data', None)
        if data and isinstance(data, dict):
            kwargs['data'] = data

            # find any requests params passed and apply them
            if 'requests_params' in kwargs['data']:
                # merge requests params into kwargs
                kwargs.update(kwargs['data']['requests_params'])
                del(kwargs['data']['requests_params'])

        if signed:
            # generate signature
            kwargs['data']['timestamp'] = int(time.time() * 1000)
            kwargs['data']['signature'] = self._generate_signature(kwargs['data'])

        # sort get and post params to match signature order
        if data:
            # sort post params
            kwargs['data'] = self._order_params(kwargs['data'])

        # if get request assign data array to params value for requests lib
        if data and (method == 'get' or force_params):
            kwargs['params'] = kwargs['data']
            del(kwargs['data'])

        response = getattr(self.session, method)(uri, **kwargs)
        return self._handle_response(response)

    def _request_api(self, method, path, signed=False, version=PUBLIC_API_VERSION, **kwargs):
        uri = self._create_api_uri(path, signed, version)

        return self._request(method, uri, signed, **kwargs)

    def _request_withdraw_api(self, method, path, signed=False, **kwargs):
        uri = self._create_withdraw_api_uri(path)

        return self._request(method, uri, signed, True, **kwargs)

    def _request_website(self, method, path, signed=False, **kwargs):

        uri = self._create_website_uri(path)

        return self._request(method, uri, signed, **kwargs)

    def _handle_response(self, response):
        """Internal helper for handling API responses from the Bitrue server.
        Raises the appropriate exceptions when necessary; otherwise, returns the
        response.
        """
        if not str(response.status_code).startswith('2'):
            raise BitrueAPIException(response)
        try:
            return response.json()
        except ValueError:

            raise BitrueRequestException('Invalid Response: %s' % response.text)

    def _order_format_print(self, dataset, orient='h'):
        if orient == 'v':
            # 'v' is still under construction - do not use.
            headers = ['Field', 'Value']
            data = [(k, v) for k, v in dataset.items()]
            return tabulate(data, headers=headers)

        elif orient == 'h':
            # Only use for order status currently
            header = dataset[0].keys()
            rows = [x.values() for x in dataset]
            return tabulate(rows, header)
    def _get(self, path, signed=False, version=PUBLIC_API_VERSION, **kwargs):
        return self._request_api('get', path, signed, version, **kwargs)

    def _post(self, path, signed=False, version=PUBLIC_API_VERSION, **kwargs):
        return self._request_api('post', path, signed, version, **kwargs)

    def _put(self, path, signed=False, version=PUBLIC_API_VERSION, **kwargs):
        return self._request_api('put', path, signed, version, **kwargs)

    def _delete(self, path, signed=False, version=PUBLIC_API_VERSION, **kwargs):
        return self._request_api('delete', path, signed, version, **kwargs)

    # Exchange Endpoints

    def get_products(self): #DELETE
        """Return list of products currently listed on Bitrue

        Use get_exchange_info() call instead

        :returns: list - List of product dictionaries

        :raises: BitrueRequestException, BitrueAPIException

        """

        products = self._request_website('get', 'exchange/public/product')
        return products

    def get_exchange_info(self): #PRODREADY
        """Return rate limits and list of symbols
        ref: https://github.com/Bitrue-exchange/bitrue-official-api-docs#exchange-information-some-fields-not-support-only-reserved

        :returns: list - List of product dictionaries

        .. code-block:: python

                {
                  "timezone": "UTC",
                  "serverTime": 1508631584636,
                  "rateLimits": [{
                      "rateLimitType": "REQUESTS_WEIGHT",
                      "interval": "MINUTE",
                      "limit": 1200
                    },
                    {
                      "rateLimitType": "ORDERS",
                      "interval": "SECOND",
                      "limit": 10
                    },
                    {
                      "rateLimitType": "ORDERS",
                      "interval": "DAY",
                      "limit": 100000
                    }
                  ],
                  "exchangeFilters": [],
                  "symbols": [{
                    "symbol": "ETHBTC",
                    "status": "TRADING",
                    "baseAsset": "ETH",
                    "baseAssetPrecision": 8,???
                    "quoteAsset": "BTC",
                    "quotePrecision": 8,
                    "orderTypes": ["LIMIT", "MARKET"],
                    "icebergAllowed": false,  ???
                    "filters": [{   ??
                      "filterType": "PRICE_FILTER", ??
                      "minPrice": "0.00000100", ??
                      "maxPrice": "100000.00000000", ??
                      "tickSize": "0.00000100" ??
                    }, {
                      "filterType": "LOT_SIZE",
                      "minQty": "0.00100000",
                      "maxQty": "100000.00000000",
                      "stepSize": "0.00100000"
                    }, {
                      "filterType": "MIN_NOTIONAL",
                      "minNotional": "0.00100000"
                    }]
                  }]
                }

        :raises: BitrueRequestException, BitrueAPIException

        """

        return self._get('exchangeInfo')

    def get_symbol_info(self, symbol): #PRODREADY
        """Return information about a symbol
        ref: https://github.com/Bitrue-exchange/bitrue-official-api-docs#exchange-information-some-fields-not-support-only-reserved
        :param symbol: required e.g BNBBTC
        :type symbol: str

        :returns: Dict if found, None if not

        .. code-block:: python

               {'baseAsset': 'xrp',
                 'baseAssetPrecision': 1,
                 'filters': [{'filterType': 'PRICE_FILTER',
                              'maxPrice': '0.537810000000000000000',
                              'minPrice': '0.041370000000000000000',
                              'priceScale': 5},
                             {'filterType': 'LOT_SIZE',
                              'maxQty': '1410065408.0000000000000000',
                              'minQty': '0.1000000000000000',
                              'volumeScale': 1}],
                 'icebergAllowed': False,
                 'orderTypes': ['MARKET', 'LIMIT'],
                 'quoteAsset': 'usdt',
                 'quotePrecision': 5,
                 'status': 'TRADING',
                 'symbol': 'XRPUSDT'}


        :raises: BitrueRequestException, BitrueAPIException

        """

        res = self._get('exchangeInfo')

        for item in res['symbols']:
            if item['symbol'] == symbol.upper():
                return item

        return None

    # General Endpoints

    def ping(self): #PRODREADY
        """Test connectivity to the Rest API.

        ref: https://github.com/Bitrue-exchange/bitrue-official-api-docs#test-connectivity
        :returns: Empty array

        .. code-block:: python

            {}

        :raises: BitrueRequestException, BitrueAPIException

        """
        return self._get('ping')

    def get_server_time(self): #PRODREADY
        """Test connectivity to the Rest API and get the current server time.

        ref: https://github.com/Bitrue-exchange/bitrue-official-api-docs#check-server-time

        :returns: Current server time

        .. code-block:: python

            {
                "serverTime": 1499827319559
            }

        :raises: BitrueRequestException, BitrueAPIException

        """
        return self._get('time')

    # Market Data Endpoints

    def get_ticker_price(self, symbol): #PRODREADY
        """Latest price for one symbols.

        ref: https://github.com/Bitrue-exchange/bitrue-official-api-docs#symbol-price-ticker

        :returns: Price of a market ticker

        .. code-block:: python

            [
                {'price': '0.40680', 'symbol': 'XRPUSDT'}
            ]

        :raises: BitrueRequestException, BitrueAPIException

        """
        params = {'symbol': symbol}
        return self._get('ticker/price', data=params)

    # def get_orderbook_tickers(self):  #TBD
    #     """Best price/qty on the order book for all symbols.
    #
    #     ref: https://github.com/Bitrue-exchange/bitrue-official-api-docs#symbol-order-book-ticker
    #
    #     :returns: List of order book market entries
    #
    #     .. code-block:: python
    #
    #         [
    #             {
    #                 "symbol": "LTCBTC",
    #                 "bidPrice": "4.00000000",
    #                 "bidQty": "431.00000000",
    #                 "askPrice": "4.00000200",
    #                 "askQty": "9.00000000"
    #             },
    #             {
    #                 "symbol": "ETHBTC",
    #                 "bidPrice": "0.07946700",
    #                 "bidQty": "9.00000000",
    #                 "askPrice": "100000.00000000",
    #                 "askQty": "1000.00000000"
    #             }
    #         ]
    #
    #     :raises: BitrueRequestException, BitrueAPIException
    #
    #     """
    #     return self._get('ticker/allBookTickers')

    def get_order_book(self, **params): #PRODREADY
        """Get the Order Book for the market

        https://github.com/Bitrue-exchange/bitrue-official-api-docs#order-book

        :param symbol: required
        :type symbol: str
        :param limit:  Default 100; 5, 10, 20, 50, 100
        :type limit: int

        :returns: API response

        .. code-block:: python

            {
              "lastUpdateId": 1027024,
              "bids": [
                [
                  "4.00000000",     // PRICE
                  "431.00000000",   // QTY
                  []                // Ignore.
                ]
              ],
              "asks": [
                [
                  "4.00000200",
                  "12.00000000",
                  []
                ]
              ]
            }

        :raises: BitrueRequestException, BitrueAPIException

        """
        return self._get('depth', data=params)

    def get_recent_trades(self, **params): #PRODREADY
        """Get recent trades (up to last 500).

        ref: https://github.com/Bitrue-exchange/bitrue-official-api-docs#recent-trades-list

        :param symbol: required
        :type symbol: str
        :param limit:  Default 100; max 1000.
        :type limit: int

        :returns: API response

        .. code-block:: python

            [
              {
                "id": 28457,
                "price": "4.00000100",
                "qty": "12.00000000",
                "time": 1499865549590,
                "isBuyerMaker": true,
                "isBestMatch": true  //预留
              }
            ]

        :raises: BitrueRequestException, BitrueAPIException

        """
        return self._get('trades', data=params)

    def get_historical_trades(self, **params): #PRODREADY
        """Get older trades.

        ref: https://github.com/Bitrue-exchange/bitrue-official-api-docs#old-trade-lookup-market_data

        :param symbol: required
        :type symbol: str
        :param limit:  Default 100; max 1000.
        :type limit: int
        :param fromId:  TradeId to fetch from. Default gets most recent trades.
        :type fromId: str

        :returns: API response

        .. code-block:: python

            [
                {
                    "id": 28457,
                    "price": "4.00000100",
                    "qty": "12.00000000",
                    "time": 1499865549590,
                    "isBuyerMaker": true,
                    "isBestMatch": true
                }
            ]

        :raises: BitrueRequestException, BitrueAPIException

        """
        return self._get('historicalTrades', data=params)

    def get_aggregate_trades(self, **params): #PRODREADY
        """Get compressed, aggregate trades. Trades that fill at the time,
        from the same order, with the same price will have the quantity aggregated.

        ref: https://github.com/Bitrue-exchange/bitrue-official-api-docs#compressedaggregate-trades-list

        :param symbol: required
        :type symbol: str
        :param fromId:  ID to get aggregate trades from INCLUSIVE.
        :type fromId: str
        :param startTime: Timestamp in ms to get aggregate trades from INCLUSIVE.
        :type startTime: int
        :param endTime: Timestamp in ms to get aggregate trades until INCLUSIVE.
        :type endTime: int
        :param limit:  Default 500; max 500.
        :type limit: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "a": 26129,         # Aggregate tradeId
                    "p": "0.01633102",  # Price
                    "q": "4.70443515",  # Quantity
                    "f": 27781,         # First tradeId
                    "l": 27781,         # Last tradeId
                    "T": 1498793709153, # Timestamp
                    "m": true,          # Was the buyer the maker?
                    "M": true           # Was the trade the best price match?
                }
            ]

        :raises: BitrueRequestException, BitrueAPIException

        """
        return self._get('aggTrades', data=params)

    def aggregate_trade_iter(self, symbol, start_str=None, last_id=None): #TBD
        """Iterate over aggregate trade data from (start_time or last_id) to
        the end of the history so far.

        If start_time is specified, start with the first trade after
        start_time. Meant to initialise a local cache of trade data.

        If last_id is specified, start with the trade after it. This is meant
        for updating a pre-existing local trade data cache.

        Only allows start_str or last_id—not both. Not guaranteed to work
        right if you're running more than one of these simultaneously. You
        will probably hit your rate limit.

        See dateparser docs for valid start and end string formats http://dateparser.readthedocs.io/en/latest/

        If using offset strings for dates add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"

        :param symbol: Symbol string e.g. ETHBTC
        :type symbol: str
        :param start_str: Start date string in UTC format or timestamp in milliseconds. The iterator will
        return the first trade occurring later than this time.
        :type start_str: str|int
        :param last_id: aggregate trade ID of the last known aggregate trade.
        Not a regular trade ID. See ref: https://github.com/Bitrue-exchange/bitrue-official-api-docs#compressedaggregate-trades-list

        :returns: an iterator of JSON objects, one per trade. The format of
        each object is identical to Client.aggregate_trades().

        :type last_id: int
        """
        if start_str is not None and last_id is not None:
            raise ValueError(
                'start_time and last_id may not be simultaneously specified.')

        # If there's no last_id, get one.
        if last_id is None:
            # Without a last_id, we actually need the first trade.  Normally,
            # we'd get rid of it. See the next loop.
            if start_str is None:
                trades = self.get_aggregate_trades(symbol=symbol, fromId=0)
            else:
                # The difference between startTime and endTime should be less
                # or equal than an hour and the result set should contain at
                # least one trade.
                if type(start_str) == int:
                    start_ts = start_str
                else:
                    start_ts = date_to_milliseconds(start_str)
                # If the resulting set is empty (i.e. no trades in that interval)
                # then we just move forward hour by hour until we find at least one
                # trade or reach present moment
                while True:
                    end_ts = start_ts + (60 * 60 * 1000)
                    trades = self.get_aggregate_trades(
                        symbol=symbol,
                        startTime=start_ts,
                        endTime=end_ts)
                    if len(trades) > 0:
                        break
                    # If we reach present moment and find no trades then there is
                    # nothing to iterate, so we're done
                    if end_ts > int(time.time() * 1000):
                        return
                    start_ts = end_ts
            for t in trades:
                yield t
            last_id = trades[-1][self.AGG_ID]

        while True:
            # There is no need to wait between queries, to avoid hitting the
            # rate limit. We're using blocking IO, and as long as we're the
            # only thread running calls like this, Bitrue will automatically
            # add the right delay time on their end, forcing us to wait for
            # data. That really simplifies this function's job. Bitrue is
            # fucking awesome.
            trades = self.get_aggregate_trades(symbol=symbol, fromId=last_id)
            # fromId=n returns a set starting with id n, but we already have
            # that one. So get rid of the first item in the result set.
            trades = trades[1:]
            if len(trades) == 0:
                return
            for t in trades:
                yield t
            last_id = trades[-1][self.AGG_ID]

    def get_klines(self, **params):
        """Kline/candlestick bars for a symbol. Klines are uniquely identified by their open time.

        ref:
        :param symbol: required
        :type symbol: str
        :param interval: -
        :type interval: str
        :param limit: - Default 500; max 500.
        :type limit: int
        :param startTime:
        :type startTime: int
        :param endTime:
        :type endTime: int

        :returns: API response

        .. code-block:: python

            [
                [
                    1499040000000,      # Open time
                    "0.01634790",       # Open
                    "0.80000000",       # High
                    "0.01575800",       # Low
                    "0.01577100",       # Close
                    "148976.11427815",  # Volume
                    1499644799999,      # Close time
                    "2434.19055334",    # Quote asset volume
                    308,                # Number of trades
                    "1756.87402397",    # Taker buy base asset volume
                    "28.46694368",      # Taker buy quote asset volume
                    "17928899.62484339" # Can be ignored
                ]
            ]

        :raises: BitrueRequestException, BitrueAPIException

        """
        return self._get('ticker/1h', data=params)

    def _get_earliest_valid_timestamp(self, symbol, interval):
        """Get earliest valid open timestamp from Bitrue

        :param symbol: Name of symbol pair e.g BNBBTC
        :type symbol: str
        :param interval: Bitrue Kline interval
        :type interval: str

        :return: first valid timestamp

        """
        kline = self.get_klines(
            symbol=symbol,
            interval=interval,
            limit=1,
            startTime=0,
            endTime=None
        )
        return kline[0][0]

    def get_historical_klines(self, symbol, interval, start_str, end_str=None,
                              limit=500):
        """Get Historical Klines from Bitrue

        See dateparser docs for valid start and end string formats http://dateparser.readthedocs.io/en/latest/

        If using offset strings for dates add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"

        :param symbol: Name of symbol pair e.g BNBBTC
        :type symbol: str
        :param interval: Bitrue Kline interval
        :type interval: str
        :param start_str: Start date string in UTC format or timestamp in milliseconds
        :type start_str: str|int
        :param end_str: optional - end date string in UTC format or timestamp in milliseconds (default will fetch everything up to now)
        :type end_str: str|int
        :param limit: Default 500; max 1000.
        :type limit: int

        :return: list of OHLCV values

        """
        # init our list
        output_data = []

        # setup the max limit
        limit = limit

        # convert interval to useful value in seconds
        timeframe = interval_to_milliseconds(interval)

        # convert our date strings to milliseconds
        if type(start_str) == int:
            start_ts = start_str
        else:
            start_ts = date_to_milliseconds(start_str)

        # establish first available start timestamp
        first_valid_ts = self._get_earliest_valid_timestamp(symbol, interval)
        start_ts = max(start_ts, first_valid_ts)

        # if an end time was passed convert it
        end_ts = None
        if end_str:
            if type(end_str) == int:
                end_ts = end_str
            else:
                end_ts = date_to_milliseconds(end_str)

        idx = 0
        while True:
            # fetch the klines from start_ts up to max 500 entries or the end_ts if set
            temp_data = self.get_klines(
                symbol=symbol,
                interval=interval,
                limit=limit,
                startTime=start_ts,
                endTime=end_ts
            )

            # handle the case where exactly the limit amount of data was returned last loop
            if not len(temp_data):
                break

            # append this loops data to our output data
            output_data += temp_data

            # set our start timestamp using the last value in the array
            start_ts = temp_data[-1][0]

            idx += 1
            # check if we received less than the required limit and exit the loop
            if len(temp_data) < limit:
                # exit the while loop
                break

            # increment next call by our timeframe
            start_ts += timeframe

            # sleep after every 3rd call to be kind to the API
            if idx % 3 == 0:
                time.sleep(1)

        return output_data

    def get_historical_klines_generator(self, symbol, interval, start_str, end_str=None):
        """Get Historical Klines from Bitrue

        See dateparser docs for valid start and end string formats http://dateparser.readthedocs.io/en/latest/

        If using offset strings for dates add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"

        :param symbol: Name of symbol pair e.g XRPUSDT
        :type symbol: str
        :param interval: Bitrue Kline interval
        :type interval: str
        :param start_str: Start date string in UTC format or timestamp in milliseconds
        :type start_str: str|int
        :param end_str: optional - end date string in UTC format or timestamp in milliseconds (default will fetch everything up to now)
        :type end_str: str|int

        :return: generator of OHLCV values

        """

        # setup the max limit
        limit = 500

        # convert interval to useful value in seconds
        timeframe = interval_to_milliseconds(interval)

        # convert our date strings to milliseconds
        if type(start_str) == int:
            start_ts = start_str
        else:
            start_ts = date_to_milliseconds(start_str)

        # establish first available start timestamp
        first_valid_ts = self._get_earliest_valid_timestamp(symbol, interval)
        start_ts = max(start_ts, first_valid_ts)

        # if an end time was passed convert it
        end_ts = None
        if end_str:
            if type(end_str) == int:
                end_ts = end_str
            else:
                end_ts = date_to_milliseconds(end_str)

        idx = 0
        while True:
            # fetch the klines from start_ts up to max 500 entries or the end_ts if set
            output_data = self.get_klines(
                symbol=symbol,
                interval=interval,
                limit=limit,
                startTime=start_ts,
                endTime=end_ts
            )

            # handle the case where exactly the limit amount of data was returned last loop
            if not len(output_data):
                break

            # yield data
            for o in output_data:
                yield o

            # set our start timestamp using the last value in the array
            start_ts = output_data[-1][0]

            idx += 1
            # check if we received less than the required limit and exit the loop
            if len(output_data) < limit:
                # exit the while loop
                break

            # increment next call by our timeframe
            start_ts += timeframe

            # sleep after every 3rd call to be kind to the API
            if idx % 3 == 0:
                time.sleep(1)

    def get_ticker_24h(self, **params):  #PRODREADY
        """24 hour price change statistics.

        ref: https://github.com/Bitrue-exchange/bitrue-official-api-docs#24hr-ticker-price-change-statistics

        :param symbol:
        :type symbol: str

        :returns: API response

        .. code-block:: python

            {
              "symbol": "BNBBTC",
              "priceChange": "-94.99999800",
              "priceChangePercent": "-95.960",
              "weightedAvgPrice": "0.29628482",
              "prevClosePrice": "0.10002000",
              "lastPrice": "4.00000200",
              "lastQty": "200.00000000",
              "bidPrice": "4.00000000",
              "askPrice": "4.00000200",
              "openPrice": "99.00000000",
              "highPrice": "100.00000000",
              "lowPrice": "0.10000000",
              "volume": "8913.30000000",
              "quoteVolume": "15.30000000",
              "openTime": 1499783499040,
              "closeTime": 1499869899040,
              "firstId": 28385,   // First tradeId
              "lastId": 28460,    // Last tradeId
              "count": 76         // Trade count
            }

        OR

        .. code-block:: python

            [
              {
                "symbol": "BNBBTC",
                "priceChange": "-94.99999800",
                "priceChangePercent": "-95.960",
                "weightedAvgPrice": "0.29628482",
                "prevClosePrice": "0.10002000",
                "lastPrice": "4.00000200",
                "lastQty": "200.00000000",
                "bidPrice": "4.00000000",
                "askPrice": "4.00000200",
                "openPrice": "99.00000000",
                "highPrice": "100.00000000",
                "lowPrice": "0.10000000",
                "volume": "8913.30000000",
                "quoteVolume": "15.30000000",
                "openTime": 1499783499040,
                "closeTime": 1499869899040,
                "firstId": 28385,   // First tradeId
                "lastId": 28460,    // Last tradeId
                "count": 76         // Trade count
              }
            ]
        :raises: BitrueRequestException, BitrueAPIException

        """
        return self._get('ticker/24hr', data=params)

    def get_symbol_ticker(self, **params): #PRODREADY
        """Latest price for a symbol or symbols.

        ref: https://github.com/Bitrue-exchange/bitrue-official-api-docs#symbol-price-ticker

        :param symbol:
        :type symbol: str

        :returns: API response

        .. code-block:: python

            {
              "symbol": "LTCBTC",
              "price": "4.00000200"
            }

        :raises: BitrueRequestException, BitrueAPIException

        """
        return self._get('ticker/price', data=params, version=self.PRIVATE_API_VERSION)

    def get_orderbook_ticker(self, **params): #PRODREADY
        """Latest price for a symbol or symbols.

        ref: https://github.com/Bitrue-exchange/bitrue-official-api-docs#symbol-order-book-ticker

        :param symbol:
        :type symbol: str

        :returns: API response

        .. code-block:: python

            {
              "symbol": "LTCBTC",
              "bidPrice": "4.00000000",
              "bidQty": "431.00000000",
              "askPrice": "4.00000200",
              "askQty": "9.00000000"
            }


        :raises: BitrueRequestException, BitrueAPIException

        """
        return self._get('ticker/bookTicker', data=params, version=self.PRIVATE_API_VERSION)

    # Account Endpoints

    def create_order(self, **params):
        """Send in a new order

        Any order with an icebergQty MUST have timeInForce set to GTC.

        https://github.com/Bitrue-exchange/bitrue-official-api-docs#new-order--trade

        :param symbol: required
        :type symbol: str
        :param side: required
        :type side: str
        :param type: required
        :type type: str
        :param timeInForce: required if limit order
        :type timeInForce: str
        :param quantity: required
        :type quantity: decimal
        :param price: required
        :type price: str
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param icebergQty: Used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to create an iceberg order.
        :type icebergQty: decimal
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        Response ACK:

        .. code-block:: python

            {
              "symbol": "BTCUSDT",
              "orderId": 28,
              "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP", **Reserved**
              "transactTime": 1507725176595
            }

        Response RESULT:

        .. code-block:: python

            {
                "symbol": "BTCUSDT",
                "orderId": 28,
                "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
                "transactTime": 1507725176595,
                "price": "0.00000000",
                "origQty": "10.00000000",
                "executedQty": "10.00000000",
                "status": "FILLED",
                "timeInForce": "GTC",
                "type": "MARKET",
                "side": "SELL"
            }

        Response FULL:

        .. code-block:: python

            {
                "symbol": "BTCUSDT",
                "orderId": 28,
                "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
                "transactTime": 1507725176595,
                "price": "0.00000000",
                "origQty": "10.00000000",
                "executedQty": "10.00000000",
                "status": "FILLED",
                "timeInForce": "GTC",
                "type": "MARKET",
                "side": "SELL",
                "fills": [
                    {
                        "price": "4000.00000000",
                        "qty": "1.00000000",
                        "commission": "4.00000000",
                        "commissionAsset": "USDT"
                    },
                    {
                        "price": "3999.00000000",
                        "qty": "5.00000000",
                        "commission": "19.99500000",
                        "commissionAsset": "USDT"
                    },
                    {
                        "price": "3998.00000000",
                        "qty": "2.00000000",
                        "commission": "7.99600000",
                        "commissionAsset": "USDT"
                    },
                    {
                        "price": "3997.00000000",
                        "qty": "1.00000000",
                        "commission": "3.99700000",
                        "commissionAsset": "USDT"
                    },
                    {
                        "price": "3995.00000000",
                        "qty": "1.00000000",
                        "commission": "3.99500000",
                        "commissionAsset": "USDT"
                    }
                ]
            }

        :raises: BitrueRequestException, BitrueAPIException, BitrueOrderException, BitrueOrderMinAmountException, BitrueOrderMinPriceException, BitrueOrderMinTotalException, BitrueOrderUnknownSymbolException, BitrueOrderInactiveSymbolException

        """
        return self._post('order', True, data=params)

    def order_limit(self, timeInForce=TIME_IN_FORCE_GTC, **params):
        """Send in a new limit order
        https://github.com/Bitrue-exchange/bitrue-official-api-docs#new-order--trade
        Any order with an icebergQty MUST have timeInForce set to GTC.

        :param symbol: required
        :type symbol: str
        :param side: required
        :type side: str
        :param quantity: required
        :type quantity: decimal
        :param price: required
        :type price: str
        :param timeInForce: default Good till cancelled
        :type timeInForce: str
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param icebergQty: Used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to create an iceberg order.
        :type icebergQty: decimal
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        See order endpoint for full response options

        :raises: BitrueRequestException, BitrueAPIException, BitrueOrderException, BitrueOrderMinAmountException, BitrueOrderMinPriceException, BitrueOrderMinTotalException, BitrueOrderUnknownSymbolException, BitrueOrderInactiveSymbolException

        """
        params.update({
            'type': self.ORDER_TYPE_LIMIT,
            'timeInForce': timeInForce
        })
        return self.create_order(**params)

    def order_limit_buy(self, timeInForce=TIME_IN_FORCE_GTC, **params):
        """Send in a new limit buy order
        https://github.com/Bitrue-exchange/bitrue-official-api-docs#new-order--trade
        Any order with an icebergQty MUST have timeInForce set to GTC.

        :param symbol: required
        :type symbol: str
        :param quantity: required
        :type quantity: decimal
        :param price: required
        :type price: str
        :param timeInForce: default Good till cancelled
        :type timeInForce: str
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param stopPrice: Used with stop orders
        :type stopPrice: decimal
        :param icebergQty: Used with iceberg orders
        :type icebergQty: decimal
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        See order endpoint for full response options

        :raises: BitrueRequestException, BitrueAPIException, BitrueOrderException, BitrueOrderMinAmountException, BitrueOrderMinPriceException, BitrueOrderMinTotalException, BitrueOrderUnknownSymbolException, BitrueOrderInactiveSymbolException

        """
        params.update({
            'side': self.SIDE_BUY,
        })
        return self.order_limit(timeInForce=timeInForce, **params)

    def order_limit_sell(self, timeInForce=TIME_IN_FORCE_GTC, **params):
        """Send in a new limit sell order
        https://github.com/Bitrue-exchange/bitrue-official-api-docs#new-order--trade
        :param symbol: required
        :type symbol: str
        :param quantity: required
        :type quantity: decimal
        :param price: required
        :type price: str
        :param timeInForce: default Good till cancelled
        :type timeInForce: str
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param stopPrice: Used with stop orders
        :type stopPrice: decimal
        :param icebergQty: Used with iceberg orders
        :type icebergQty: decimal
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        See order endpoint for full response options

        :raises: BitrueRequestException, BitrueAPIException, BitrueOrderException, BitrueOrderMinAmountException, BitrueOrderMinPriceException, BitrueOrderMinTotalException, BitrueOrderUnknownSymbolException, BitrueOrderInactiveSymbolException

        """
        params.update({
            'side': self.SIDE_SELL
        })
        return self.order_limit(timeInForce=timeInForce, **params)

    def order_market(self, **params):
        """Send in a new market order
        https://github.com/Bitrue-exchange/bitrue-official-api-docs#new-order--trade
        :param symbol: required
        :type symbol: str
        :param side: required
        :type side: str
        :param quantity: required
        :type quantity: decimal
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        See order endpoint for full response options

        :raises: BitrueRequestException, BitrueAPIException, BitrueOrderException, BitrueOrderMinAmountException, BitrueOrderMinPriceException, BitrueOrderMinTotalException, BitrueOrderUnknownSymbolException, BitrueOrderInactiveSymbolException

        """
        params.update({
            'type': self.ORDER_TYPE_MARKET
        })
        return self.create_order(**params)

    def order_market_buy(self, **params):
        """Send in a new market buy order
        https://github.com/Bitrue-exchange/bitrue-official-api-docs#new-order--trade
        :param symbol: required
        :type symbol: str
        :param quantity: required
        :type quantity: decimal
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        See order endpoint for full response options

        :raises: BitrueRequestException, BitrueAPIException, BitrueOrderException, BitrueOrderMinAmountException, BitrueOrderMinPriceException, BitrueOrderMinTotalException, BitrueOrderUnknownSymbolException, BitrueOrderInactiveSymbolException

        """
        params.update({
            'side': self.SIDE_BUY
        })
        return self.order_market(**params)

    def order_market_sell(self, **params):
        """Send in a new market sell order
        https://github.com/Bitrue-exchange/bitrue-official-api-docs#new-order--trade
        :param symbol: required
        :type symbol: str
        :param quantity: required
        :type quantity: decimal
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        See order endpoint for full response options

        :raises: BitrueRequestException, BitrueAPIException, BitrueOrderException, BitrueOrderMinAmountException, BitrueOrderMinPriceException, BitrueOrderMinTotalException, BitrueOrderUnknownSymbolException, BitrueOrderInactiveSymbolException

        """
        params.update({
            'side': self.SIDE_SELL
        })
        return self.order_market(**params)

    # BITRUE DOES NOT CURRENTLY SUPPORT TEST TRADES.
    # def create_test_order(self, **params):
    #     """Test new order creation and signature/recvWindow long. Creates and validates a new order but does not send it into the matching engine.
    #     ref: https://github.com/Bitrue-exchange/bitrue-official-api-docs#new-order--trade
    #
    #     :param symbol: required
    #     :type symbol: str
    #     :param side: required
    #     :type side: str
    #     :param type: required
    #     :type type: str
    #     :param timeInForce: required if limit order
    #     :type timeInForce: str
    #     :param quantity: required
    #     :type quantity: decimal
    #     :param price: required
    #     :type price: str
    #     :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
    #     :type newClientOrderId: str
    #     :param icebergQty: Used with iceberg orders
    #     :type icebergQty: decimal
    #     :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
    #     :type newOrderRespType: str
    #     :param recvWindow: The number of milliseconds the request is valid for
    #     :type recvWindow: int
    #
    #     :returns: API response
    #
    #     .. code-block:: python
    #
    #         {}
    #
    #     :raises: BitrueRequestException, BitrueAPIException, BitrueOrderException, BitrueOrderMinAmountException, BitrueOrderMinPriceException, BitrueOrderMinTotalException, BitrueOrderUnknownSymbolException, BitrueOrderInactiveSymbolException
    #
    #
    #     """
    #     return self._post('order/test', True, data=params)

    def get_order(self, **params):
        """Check an order's status. Either orderId or origClientOrderId must be sent.

        https://github.com/Bitrue-exchange/bitrue-official-api-docs#new-order--trade
        :param symbol: required
        :type symbol: str
        :param orderId: The unique order id
        :type orderId: int
        :param origClientOrderId: optional
        :type origClientOrderId: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "symbol": "LTCBTC",
                "orderId": 1,
                "clientOrderId": "myOrder1",
                "price": "0.1",
                "origQty": "1.0",
                "executedQty": "0.0",
                "status": "NEW",
                "timeInForce": "GTC",
                "type": "LIMIT",
                "side": "BUY",
                "stopPrice": "0.0",
                "icebergQty": "0.0",
                "time": 1499827319559
            }

        :raises: BitrueRequestException, BitrueAPIException

        """
        return self._get('order', True, data=params)

    def get_all_orders(self, **params):
        """Get all account orders; active, canceled, or filled.

        ref: https://github.com/Bitrue-exchange/bitrue-official-api-docs#all-orders-user_data

        :param symbol: required
        :type symbol: str
        :param orderId: The unique order id
        :type orderId: int
        :param limit: Default 500; max 500.
        :type limit: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "symbol": "LTCBTC",
                    "orderId": 1,
                    "clientOrderId": "myOrder1",
                    "price": "0.1",
                    "origQty": "1.0",
                    "executedQty": "0.0",
                    "status": "NEW",
                    "timeInForce": "GTC",
                    "type": "LIMIT",
                    "side": "BUY",
                    "stopPrice": "0.0",
                    "icebergQty": "0.0",
                    "time": 1499827319559
                }
            ]

        :raises: BitrueRequestException, BitrueAPIException

        """
        return self._get('allOrders', True, data=params)

    def cancel_order(self, **params):
        """Cancel an active order. Either orderId or origClientOrderId must be sent.

        https://github.com/Bitrue-exchange/bitrue-official-api-docs#cancel-order-trade

        :param symbol: required
        :type symbol: str
        :param orderId: The unique order id
        :type orderId: int
        :param origClientOrderId: optional
        :type origClientOrderId: str
        :param newClientOrderId: Used to uniquely identify this cancel. Automatically generated by default.
        :type newClientOrderId: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "symbol": "LTCBTC",
                "origClientOrderId": "myOrder1",
                "orderId": 1,
                "clientOrderId": "cancelMyOrder1"
            }

        :raises: BitrueRequestException, BitrueAPIException

        """
        return self._delete('order', True, data=params)

    def get_open_orders(self, **params):
        """Get all open orders on a symbol.

        https://github.com/Bitrue-exchange/bitrue-official-api-docs#current-open-orders-user_data

        :param symbol: required
        :type symbol: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "symbol": "LTCBTC",
                    "orderId": 1,
                    "clientOrderId": "myOrder1",
                    "price": "0.1",
                    "origQty": "1.0",
                    "executedQty": "0.0",
                    "status": "NEW",
                    "timeInForce": "GTC",
                    "type": "LIMIT",
                    "side": "BUY",
                    "stopPrice": "0.0",
                    "icebergQty": "0.0",
                    "time": 1499827319559
                }
            ]

        :raises: BitrueRequestException, BitrueAPIException

        """
        return self._get('openOrders', True, data=params)

    # User Stream Endpoints
    def get_account(self, **params):
        """Get current account information.

        ref: https://github.com/Bitrue-exchange/bitrue-official-api-docs#account-information-user_data

        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "makerCommission": 15,
                "takerCommission": 15,
                "buyerCommission": 0,
                "sellerCommission": 0,
                "canTrade": true,
                "canWithdraw": true,
                "canDeposit": true,
                "balances": [
                    {
                        "asset": "BTC",
                        "free": "4723846.89208129",
                        "locked": "0.00000000"
                    },
                    {
                        "asset": "LTC",
                        "free": "4763368.68006011",
                        "locked": "0.00000000"
                    }
                ]
            }

        :raises: BitrueRequestException, BitrueAPIException

        """
        return self._get('account', True, data=params)

    def get_asset_balance(self, asset, **params):
        """Get current asset balance.

        ref: https://github.com/Bitrue-exchange/bitrue-official-api-docs#account-information-user_data

        :param asset: required
        :type asset: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: dictionary or None if not found

        .. code-block:: python

            {
                "asset": "BTC",
                "free": "4723846.89208129",
                "locked": "0.00000000"
            }

        :raises: BitrueRequestException, BitrueAPIException

        """
        res = self.get_account(**params)
        # find asset balance in list of balances
        if "balances" in res:
            for bal in res['balances']:
                if bal['asset'].lower() == asset.lower():
                    return bal
        return None

    def get_my_trades(self, **params):
        """Get trades for a specific symbol.

        ref: https://github.com/Bitrue-exchange/bitrue-official-api-docs#account-trade-list-user_data

        :param symbol: optional
        :type symbol: str
        :param limit: Default 500; max 500.
        :type limit: int
        :param fromId: TradeId to fetch from. Default gets most recent trades.
        :type fromId: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "id": 28457,
                    "price": "4.00000100",
                    "qty": "12.00000000",
                    "commission": "10.10000000",
                    "commissionAsset": "BNB",
                    "time": 1499865549590,
                    "isBuyer": true,
                    "isMaker": false,
                    "isBestMatch": true
                }
            ]

        :raises: BitrueRequestException, BitrueAPIException

        """
        return self._get('myTrades', True, data=params)
    # FUNCTIONS BELOW ARE NOT AVAILABLE ON BITRUE BUT LEFT HERE FOR FUTURE DEVELOPMENT
    # def get_system_status(self):
    #     """Get system status detail.
    #
    #
    #     :returns: API response
    #
    #     .. code-block:: python
    #
    #         {
    #             "status": 0,        # 0: normal，1：system maintenance
    #             "msg": "normal"     # normal or System maintenance.
    #         }
    #
    #     :raises: BitrueAPIException
    #
    #     """
    #     return self._request_withdraw_api('get', 'systemStatus.html')
    #
    # def get_account_status(self, **params):
    #     """Get account status detail.
    #
    #
    #     :param recvWindow: the number of milliseconds the request is valid for
    #     :type recvWindow: int
    #
    #     :returns: API response
    #
    #     .. code-block:: python
    #
    #         {
    #             "msg": "Order failed:Low Order fill rate! Will be reactivated after 5 minutes.",
    #             "success": true,
    #             "objs": [
    #                 "5"
    #             ]
    #         }
    #
    #     :raises: BitrueWithdrawException
    #
    #     """
    #     res = self._request_withdraw_api('get', 'accountStatus.html', True, data=params)
    #     if not res['success']:
    #         raise BitrueWithdrawException(res['msg'])
    #     return res
    #
    # def get_dust_log(self, **params):
    #     """Get log of small amounts exchanged for BNB.
    #
    #
    #     :param recvWindow: the number of milliseconds the request is valid for
    #     :type recvWindow: int
    #
    #     :returns: API response
    #
    #     .. code-block:: python
    #
    #         {
    #             "success": true,
    #             "results": {
    #                 "total": 2,   //Total counts of exchange
    #                 "rows": [
    #                     {
    #                         "transfered_total": "0.00132256", # Total transfered BNB amount for this exchange.
    #                         "service_charge_total": "0.00002699",   # Total service charge amount for this exchange.
    #                         "tran_id": 4359321,
    #                         "logs": [           # Details of  this exchange.
    #                             {
    #                                 "tranId": 4359321,
    #                                 "serviceChargeAmount": "0.000009",
    #                                 "uid": "10000015",
    #                                 "amount": "0.0009",
    #                                 "operateTime": "2018-05-03 17:07:04",
    #                                 "transferedAmount": "0.000441",
    #                                 "fromAsset": "USDT"
    #                             },
    #                             {
    #                                 "tranId": 4359321,
    #                                 "serviceChargeAmount": "0.00001799",
    #                                 "uid": "10000015",
    #                                 "amount": "0.0009",
    #                                 "operateTime": "2018-05-03 17:07:04",
    #                                 "transferedAmount": "0.00088156",
    #                                 "fromAsset": "ETH"
    #                             }
    #                         ],
    #                         "operate_time": "2018-05-03 17:07:04" //The time of this exchange.
    #                     },
    #                     {
    #                         "transfered_total": "0.00058795",
    #                         "service_charge_total": "0.000012",
    #                         "tran_id": 4357015,
    #                         "logs": [       // Details of  this exchange.
    #                             {
    #                                 "tranId": 4357015,
    #                                 "serviceChargeAmount": "0.00001",
    #                                 "uid": "10000015",
    #                                 "amount": "0.001",
    #                                 "operateTime": "2018-05-02 13:52:24",
    #                                 "transferedAmount": "0.00049",
    #                                 "fromAsset": "USDT"
    #                             },
    #                             {
    #                                 "tranId": 4357015,
    #                                 "serviceChargeAmount": "0.000002",
    #                                 "uid": "10000015",
    #                                 "amount": "0.0001",
    #                                 "operateTime": "2018-05-02 13:51:11",
    #                                 "transferedAmount": "0.00009795",
    #                                 "fromAsset": "ETH"
    #                             }
    #                         ],
    #                         "operate_time": "2018-05-02 13:51:11"
    #                     }
    #                 ]
    #             }
    #         }
    #
    #     :raises: BitrueWithdrawException
    #
    #     """
    #     res = self._request_withdraw_api('get', 'userAssetDribbletLog.html', True, data=params)
    #     if not res['success']:
    #         raise BitrueWithdrawException(res['msg'])
    #     return res
    #
    # def get_trade_fee(self, **params):
    #     """Get trade fee.
    #
    #
    #     :param symbol: optional
    #     :type symbol: str
    #     :param recvWindow: the number of milliseconds the request is valid for
    #     :type recvWindow: int
    #
    #     :returns: API response
    #
    #     .. code-block:: python
    #
    #         {
    #             "tradeFee": [
    #                 {
    #                     "symbol": "ADABNB",
    #                     "maker": 0.9000,
    #                     "taker": 1.0000
    #                 }, {
    #                     "symbol": "BNBBTC",
    #                     "maker": 0.3000,
    #                     "taker": 0.3000
    #                 }
    #             ],
    #             "success": true
    #         }
    #
    #     :raises: BitrueWithdrawException
    #
    #     """
    #     res = self._request_withdraw_api('get', 'tradeFee.html', True, data=params)
    #     if not res['success']:
    #         raise BitrueWithdrawException(res['msg'])
    #     return res
    #
    # def get_asset_details(self, **params):
    #     """Fetch details on assets.
    #
    #
    #     :param recvWindow: the number of milliseconds the request is valid for
    #     :type recvWindow: int
    #
    #     :returns: API response
    #
    #     .. code-block:: python
    #
    #         {
    #             "success": true,
    #             "assetDetail": {
    #                 "CTR": {
    #                     "minWithdrawAmount": "70.00000000", //min withdraw amount
    #                     "depositStatus": false,//deposit status
    #                     "withdrawFee": 35, // withdraw fee
    #                     "withdrawStatus": true, //withdraw status
    #                     "depositTip": "Delisted, Deposit Suspended" //reason
    #                 },
    #                 "SKY": {
    #                     "minWithdrawAmount": "0.02000000",
    #                     "depositStatus": true,
    #                     "withdrawFee": 0.01,
    #                     "withdrawStatus": true
    #                 }
    #             }
    #         }
    #
    #     :raises: BitrueWithdrawException
    #
    #     """
    #     res = self._request_withdraw_api('get', 'assetDetail.html', True, data=params)
    #     if not res['success']:
    #         raise BitrueWithdrawException(res['msg'])
    #     return res
    #
    # # Withdraw Endpoints
    #
    # def withdraw(self, **params):
    #     """Submit a withdraw request.
    #
    #
    #     Assumptions:
    #
    #     - You must have Withdraw permissions enabled on your API key
    #     - You must have withdrawn to the address specified through the website and approved the transaction via email
    #
    #     :param asset: required
    #     :type asset: str
    #     :type address: required
    #     :type address: str
    #     :type addressTag: optional - Secondary address identifier for coins like XRP,XMR etc.
    #     :type address: str
    #     :param amount: required
    #     :type amount: decimal
    #     :param name: optional - Description of the address, default asset value passed will be used
    #     :type name: str
    #     :param recvWindow: the number of milliseconds the request is valid for
    #     :type recvWindow: int
    #
    #     :returns: API response
    #
    #     .. code-block:: python
    #
    #         {
    #             "msg": "success",
    #             "success": true,
    #             "id":"7213fea8e94b4a5593d507237e5a555b"
    #         }
    #
    #     :raises: BitrueRequestException, BitrueAPIException, BitrueWithdrawException
    #
    #     """
    #     # force a name for the withdrawal if one not set
    #     if 'asset' in params and 'name' not in params:
    #         params['name'] = params['asset']
    #     res = self._request_withdraw_api('post', 'withdraw.html', True, data=params)
    #     if not res['success']:
    #         raise BitrueWithdrawException(res['msg'])
    #     return res
    #
    # def get_deposit_history(self, **params):
    #     """Fetch deposit history.
    #
    #
    #     :param asset: optional
    #     :type asset: str
    #     :type status: 0(0:pending,1:success) optional
    #     :type status: int
    #     :param startTime: optional
    #     :type startTime: long
    #     :param endTime: optional
    #     :type endTime: long
    #     :param recvWindow: the number of milliseconds the request is valid for
    #     :type recvWindow: int
    #
    #     :returns: API response
    #
    #     .. code-block:: python
    #
    #         {
    #             "depositList": [
    #                 {
    #                     "insertTime": 1508198532000,
    #                     "amount": 0.04670582,
    #                     "asset": "ETH",
    #                     "status": 1
    #                 }
    #             ],
    #             "success": true
    #         }
    #
    #     :raises: BitrueRequestException, BitrueAPIException
    #
    #     """
    #     return self._request_withdraw_api('get', 'depositHistory.html', True, data=params)
    #
    # def get_withdraw_history(self, **params):
    #     """Fetch withdraw history.
    #
    #
    #     :param asset: optional
    #     :type asset: str
    #     :type status: 0(0:Email Sent,1:Cancelled 2:Awaiting Approval 3:Rejected 4:Processing 5:Failure 6Completed) optional
    #     :type status: int
    #     :param startTime: optional
    #     :type startTime: long
    #     :param endTime: optional
    #     :type endTime: long
    #     :param recvWindow: the number of milliseconds the request is valid for
    #     :type recvWindow: int
    #
    #     :returns: API response
    #
    #     .. code-block:: python
    #
    #         {
    #             "withdrawList": [
    #                 {
    #                     "amount": 1,
    #                     "address": "0x6915f16f8791d0a1cc2bf47c13a6b2a92000504b",
    #                     "asset": "ETH",
    #                     "applyTime": 1508198532000
    #                     "status": 4
    #                 },
    #                 {
    #                     "amount": 0.005,
    #                     "address": "0x6915f16f8791d0a1cc2bf47c13a6b2a92000504b",
    #                     "txId": "0x80aaabed54bdab3f6de5868f89929a2371ad21d666f20f7393d1a3389fad95a1",
    #                     "asset": "ETH",
    #                     "applyTime": 1508198532000,
    #                     "status": 4
    #                 }
    #             ],
    #             "success": true
    #         }
    #
    #     :raises: BitrueRequestException, BitrueAPIException
    #
    #     """
    #     return self._request_withdraw_api('get', 'withdrawHistory.html', True, data=params)
    #
    # def get_deposit_address(self, **params):
    #     """Fetch a deposit address for a symbol
    #
    #
    #     :param asset: required
    #     :type asset: str
    #     :param recvWindow: the number of milliseconds the request is valid for
    #     :type recvWindow: int
    #
    #     :returns: API response
    #
    #     .. code-block:: python
    #
    #         {
    #             "address": "0x6915f16f8791d0a1cc2bf47c13a6b2a92000504b",
    #             "success": true,
    #             "addressTag": "1231212",
    #             "asset": "BNB"
    #         }
    #
    #     :raises: BitrueRequestException, BitrueAPIException
    #
    #     """
    #     return self._request_withdraw_api('get', 'depositAddress.html', True, data=params)
    #
    # def get_withdraw_fee(self, **params):
    #     """Fetch the withdrawal fee for an asset
    #
    #     :param asset: required
    #     :type asset: str
    #     :param recvWindow: the number of milliseconds the request is valid for
    #     :type recvWindow: int
    #
    #     :returns: API response
    #
    #     .. code-block:: python
    #
    #         {
    #             "withdrawFee": "0.0005",
    #             "success": true
    #         }
    #
    #     :raises: BitrueRequestException, BitrueAPIException
    #
    #     """
    #     return self._request_withdraw_api('get', 'withdrawFee.html', True, data=params)
    #
    # # User Stream Endpoints
    #
    # def stream_get_listen_key(self):
    #     """Start a new user data stream and return the listen key
    #     If a stream already exists it should return the same key.
    #     If the stream becomes invalid a new key is returned.
    #
    #     Can be used to keep the user stream alive.
    #
    #
    #     :returns: API response
    #
    #     .. code-block:: python
    #
    #         {
    #             "listenKey": "pqia91ma19a5s61cv6a81va65sdf19v8a65a1a5s61cv6a81va65sdf19v8a65a1"
    #         }
    #
    #     :raises: BitrueRequestException, BitrueAPIException
    #
    #     """
    #     res = self._post('userDataStream', False, data={})
    #     return res['listenKey']
    #
    # def stream_keepalive(self, listenKey):
    #     """PING a user data stream to prevent a time out.
    #
    #
    #     :param listenKey: required
    #     :type listenKey: str
    #
    #     :returns: API response
    #
    #     .. code-block:: python
    #
    #         {}
    #
    #     :raises: BitrueRequestException, BitrueAPIException
    #
    #     """
    #     params = {
    #         'listenKey': listenKey
    #     }
    #     return self._put('userDataStream', False, data=params)
    #
    # def stream_close(self, listenKey):
    #     """Close out a user data stream.
    #
    #
    #     :param listenKey: required
    #     :type listenKey: str
    #
    #     :returns: API response
    #
    #     .. code-block:: python
    #
    #         {}
    #
    #     :raises: BitrueRequestException, BitrueAPIException
    #
    #     """
    #     params = {
    #         'listenKey': listenKey
    #     }
    #     return self._delete('userDataStream', False, data=params)
