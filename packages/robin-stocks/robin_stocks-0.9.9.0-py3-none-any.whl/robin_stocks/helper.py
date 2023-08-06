from robin_stocks.constants import Session
from functools import wraps
import requests

__is_logged_in__ = False
DEVICE_TOKEN = None

def get_device_token():
    """Gets the device token"""
    global DEVICE_TOKEN
    token = DEVICE_TOKEN
    return (token)

def set_device_token(token):
    """Sets the device token"""
    global DEVICE_TOKEN
    DEVICE_TOKEN = token

def set_login_state(logged_in):
    """Sets the login state"""
    global __is_logged_in__
    __is_logged_in__ = logged_in

def login_required(func):
    """A decorator for indicating which methods require the user to be logged
       in."""
    @wraps(func)
    def login_wrapper(*args, **kwargs):
      global __is_logged_in__
      if not __is_logged_in__:
          raise Exception('{} can only be called when logged in'.format(
              func.__name__))
      return func(*args, **kwargs)
    return login_wrapper

def id_for_stock(symbol):
    """Takes a stock ticker and returns the instrument id associated with the stock.

    :param symbol: The symbol to get the id for.
    :type symbol: str
    :returns:  A string that represents the stocks instrument id.

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message)
        return None

    url = 'https://api.robinhood.com/instruments/'
    payload = { 'symbol' : symbol}
    data = request_get(url,'indexzero',payload)

    return(filter(data,'id'))

def id_for_chain(symbol):
    """Takes a stock ticker and returns the chain id associated with a stocks option.

    :param symbol: The symbol to get the id for.
    :type symbol: str
    :returns:  A string that represents the stocks options chain id.

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message)
        return None

    url = 'https://api.robinhood.com/instruments/'

    payload = { 'symbol' : symbol}
    data = request_get(url,'indexzero',payload)

    return(data['tradable_chain_id'])

def id_for_group(symbol):
    """Takes a stock ticker and returns the id associated with the group.

    :param symbol: The symbol to get the id for.
    :type symbol: str
    :returns:  A string that represents the stocks group id.

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message)
        return None

    url = 'https://api.robinhood.com/options/chains/'+id_for_chain(symbol)+'/'
    data = request_get(url)
    return(data['underlying_instruments'][0]['id'])

def id_for_option(symbol,expirationDate,strike,optionType='both'):
    """Returns the id associated with a specific option order.

    :param symbol: The symbol to get the id for.
    :type symbol: str
    :param expirationData: The expiration date as YYYY-MM-DD
    :type expirationData: str
    :param strike: The strike price.
    :type strike: str
    :param optionType: Either call or put.
    :type optionType: str
    :returns:  A string that represents the stocks option id.

    """
    symbol = symbol.upper()
    payload = { 'chain_id' : id_for_chain(symbol),
                'state' : 'active',
                'tradability' : 'tradable',
                'type' : optionType}
    url = 'https://api.robinhood.com/options/instruments/'
    data = request_get(url,'pagination',payload)

    listOfOptions = [item for item in data if item["expiration_date"] == expirationDate and float(item["strike_price"])== float(strike)]
    if (len(listOfOptions) == 0):
        print('Getting the option ID failed. Perhaps the expiration date is wrong format, or the strike price is wrong.')
        return None

    return(listOfOptions[0]['id'])


def filter(data,info):
    """Takes the data and extracts the value for the keyword that matches info.

    :param data: The data returned by request_get.
    :type data: dict or list
    :param info: The keyword to filter from the data.
    :type info: str
    :returns:  A list or string with the values that correspond to the info keyword.

    """
    if (data == None or data == [None]):
        return data
    elif (type(data) == list):
        if (len(data) == 0):
            return([None])
        compareDict = data[0]
        noneType = [None]
    elif (type(data) == dict):
        compareDict = data
        noneType = None

    if info is not None:
        if info in compareDict and type(data) == list:
            return([x[info] for x in data])
        elif info in compareDict and type(data) == dict:
            return(data[info])
        else:
            print(error_argument_not_key_in_dictionary(info))
            return(noneType)
    else:
        return(data)

def inputs_to_set(inputSymbols):
    """Takes in the parameters passed to *args and puts them in a set and a list.
    The set will make sure there are no duplicates, and then the list will keep
    the original order of the input.

    :param inputSymbols: A list, dict, or tuple of stock tickers.
    :type inputSymbols: list or dict or tuple or str
    :returns:  A list of strings that have been capitalized and stripped of white space.

    """

    symbols_list = []
    symbols_set = set()

    def add_symbol(symbol):
        symbol = symbol.upper().strip()
        if symbol not in symbols_set:
            symbols_set.add(symbol)
            symbols_list.append(symbol)

    if type(inputSymbols) is str:
        add_symbol(inputSymbols)
    elif type(inputSymbols) is list or type(inputSymbols) is tuple or type(inputSymbols) is set:
        inputSymbols = [comp for comp in inputSymbols if type(comp) is str]
        for item in inputSymbols:
            add_symbol(item)

    return symbols_list

def request_document(url,payload=None):
    """Using a document url, makes a get request and returnes the session data.

    :param url: The url to send a get request to.
    :type url: str
    :returns: Returns the session.get() data as opppose to session.get().json() data.

    """
    try:
        res = Session.get(url,params=payload)
        res.raise_for_status()
    except requests.exceptions.HTTPError as message:
        print(message)
        return None

    return res

def request_get(url,dataType='regular',payload=None):
    """For a given url and payload, makes a get request and returns the data.

    :param url: The url to send a get request to.
    :type url: str
    :param dataType: Determines how far to drill down into the data. 'regular' returns the unfiltered data. \
    'results' will return data['results']. 'pagination' will return data['results'] and append it with any \
    data that is in data['next']. 'indexzero' will return data['results'][0].
    :type dataType: Optional[str]
    :param payload: Dictionary of parameters to pass to the url as url/?key1=value1&key2=value2.
    :type payload: Optional[dict]
    :returns: Returns the data from the get request.

    """
    try:
        res = Session.get(url,params=payload)
        res.raise_for_status()
        data = res.json()
    except (requests.exceptions.HTTPError,AttributeError) as message:
        print(message)
        if (dataType == 'results' or dataType == 'pagination'):
            return [None]
        else:
            return None

    if (dataType == 'results'):
        try:
            data = data['results']
        except KeyError as message:
            print("{} is not a key in the dictionary".format(message))
            return [None]
    elif (dataType == 'pagination'):
        counter = 2
        nextData = data
        try:
            data = data['results']
        except KeyError as message:
            print("{} is not a key in the dictionary".format(message))
            return [None]

        if nextData['next']:
            print('Found Additional pages.')
        while nextData['next']:
            try:
                res = Session.get(nextData['next'])
                res.raise_for_status()
                nextData = res.json()
            except:
                print('Additional pages exist but could not be loaded.')
                return(data)
            print('Loading page '+str(counter)+' ...')
            counter += 1
            for item in nextData['results']:
                data.append(item)
    elif (dataType == 'indexzero'):
        try:
            data = data['results'][0]
        except KeyError as message:
            print("{} is not a key in the dictionary".format(message))
            return None
        except IndexError as message:
            return None

    return data

def request_post(url,payload=None,timeout=16,json=False):
    """For a given url and payload, makes a post request and returns the response.

    :param url: The url to send a post request to.
    :type url: str
    :param payload: Dictionary of parameters to pass to the url as url/?key1=value1&key2=value2.
    :type payload: Optional[dict]
    :param timeout: The time for the post to wait for a response. Should be slightly greater than multiples of 3.
    :type timeout: Optional[int]
    :param json: This is used for buying and selling options.
    :type json: bool
    :returns: Returns the data from the post request.

    """
    try:
        if json:
            update_session('Content-Type', 'application/json')
            res = Session.post(url, json=payload, timeout=timeout)
            update_session('Content-Type', 'application/x-www-form-urlencoded; charset=utf-8')
        else:
            res = Session.post(url, data=payload, timeout=timeout)
        data = res.json()
        if 'challenge' in data:
            return data
        res.raise_for_status()
        if 'mfa_required' in data:
            mfa_token = input("Please Type In The MFA Code: ")
            payload['mfa_code'] = mfa_token
            res = Session.post(url, data=payload, timeout=timeout)
            while (res.status_code != 200):
                mfa_token = input("That MFA code was not correct. Please Type In Another MFA Code: ")
                payload['mfa_code'] = mfa_token
                res = Session.post(url, data=payload, timeout=timeout)
            data = res.json()
    except (requests.exceptions.HTTPError,AttributeError) as message:
        data = None
        print(message)

    return data

def request_delete(url):
    """For a given url and payload, makes a delete request and returns the response.

    :param url: The url to send a delete request to.
    :type url: str
    :returns: Returns the data from the delete request.

    """
    try:
        res = Session.delete(url)
        res.raise_for_status()
    except:
        data = None
        print("Cound not process delete request.")

    return data

def update_session(key,value):
    """Updates the session header used by the requests library.

    :param key: The key value to update or add to session header.
    :type key: str
    :param value: The value that corresponds to the key.
    :type value: str
    :returns: None. Updates the session header with a value.

    """
    Session.headers[key] = value

def error_argument_not_key_in_dictionary(keyword):
    return('Error: The keyword "{}" is not a key in the dictionary.'.format(keyword))

def error_ticker_does_not_exist(ticker):
    return('Warning: "{}" is not a valid stock ticker. It is being ignored'.format(ticker))

def error_must_be_nonzero(keyword):
    return('Error: The input parameter "{}" must be an integer larger than zero and non-negative'.format(keyword))
