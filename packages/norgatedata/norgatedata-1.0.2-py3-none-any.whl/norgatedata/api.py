"""This is the Norgate Data Python interface
"""

__version__ = '1.0.2'
__author__ = 'NorgateData Pty Ltd'

from .norgatehelper import *
import csv
from enum import Enum

__all__ = ['StockPriceAdjustmentType','PaddingType',
           'assetid','symbol','base_type','domicile','currency','exchange_name','exchange_name_full','security_name','subtype1','subtype2','subtype3','financial_summary',
           'business_summary','last_quoted_date','second_last_quoted_date',
           'lowest_ever_tick_size','margin','point_value','tick_size','first_notice_date','base_symbol','futures_market_name',
           'price_timeseries','capital_event_timeseries','dividend_yield_timeseries','index_constituent_timeseries','major_exchange_listed_timeseries',
           'padding_status_timeseries',
           'last_database_update_time','last_price_update_time',
           'watchlist_symbols','watchlist','watchlists',
           'fundamental',
           'classification','classification_at_level','corresponding_industry_index',
           '__version__','__author__'] 



class StockPriceAdjustmentType(Enum):
    NONE = 0
    CAPITAL = 1
    CAPITALSPECIAL = 2
    TOTALRETURN = 3

class PaddingType(Enum):
    NONE = 0
    ALLMARKETDAYS = 3
    ALLWEEKDAYS = 4
    ALLCALENDARDAYS = 5

version_checker(__version__,'norgatedata')



# Type Hints
# TODO
#assetid = TypeVar('assetid',int)
#symbol = TypeVar('symbol',str,int)
#field = TypeVar('field',str)
#databasename = TypeVar('databasename',str)
#level = TypeVar('level',int)
#schemename = TypeVar('schemename',str)
#indexfamilycode = TypeVar('indexfamilycode',str)
#indexreturntype = TypeVar('indexreturntype',str) # Might change to an enum
#classificationresulttype = TypeVar('classificationresulttype',str) # Might change to an enum

#######################################################################################################
#                           SYMBOL METADATA
#######################################################################################################


def assetid(symbol):
    r = get_api_data('security',symbol + '/assetid',None)
    validate_api_response(r,symbol)
    return bytes.decode(r.data)

def symbol(assetid):
    r = get_api_data('security',assetid + '/symbol',None)
    validate_api_response(r,symbol)
    return bytes.decode(r.data)

def base_type(symbol):
    r = get_api_data('security',symbol + '/basetype',None)
    return bytes.decode(r.data)

def domicile(symbol):
    r = get_api_data('security',symbol + '/domicile',None)
    validate_api_response(r,symbol)
    return bytes.decode(r.data)

def exchange_name(symbol):
    r = get_api_data('security',symbol + '/exchange',None)
    validate_api_response(r,symbol)
    return bytes.decode(r.data)

def exchange_name_full(symbol):
    r = get_api_data('security',symbol + '/exchangenamefull',None)
    validate_api_response(r,symbol)
    return bytes.decode(r.data)

def currency(symbol):
    r = get_api_data('security',symbol + '/currency',None)
    validate_api_response(r,symbol)
    return bytes.decode(r.data)

def security_name(symbol):
    r = get_api_data('security',symbol + '/name',None)
    validate_api_response(r,symbol)
    return bytes.decode(r.data)

def futures_market_name(symbol):
    r = get_api_data('security',symbol + '/futuresmarketname',None)
    validate_api_response(r,symbol)
    return bytes.decode(r.data)

def subtype1(symbol):
    r = get_api_data('security',symbol + '/subtype1',None)
    validate_api_response(r,symbol)
    return bytes.decode(r.data)

def subtype2(symbol):
    r = get_api_data('security',symbol + '/subtype2',None)
    validate_api_response(r,symbol)
    return bytes.decode(r.data)

def subtype3(symbol):
    r = get_api_data('security',symbol + '/subtype3',None)
    validate_api_response(r,symbol)
    return bytes.decode(r.data)

def financial_summary(symbol):
    # TODO: Output date at the same time ?
    r = get_api_data('security',symbol + '/financialsummary',None)
    validate_api_response(r,symbol)
    return bytes.decode(r.data)


def business_summary(symbol):
    # TODO: Output date at the same time ?
    r = get_api_data('security',symbol + '/businesssummary',None)
    validate_api_response(r,symbol)
    return bytes.decode(r.data)


def last_quoted_date(symbol):
    r = get_api_data('security',symbol + '/lastquoteddate',None)
    validate_api_response(r,symbol)
    return bytes.decode(r.data)

def second_last_quoted_date(symbol):
    r = get_api_data('security',symbol + '/secondlastquoteddate',None)
    validate_api_response(r,symbol)
    return bytes.decode(r.data)



#######################################################################################################
#                           FUTURES METADATA
#######################################################################################################
def lowest_ever_tick_size(symbol):
    r = get_api_data('security',symbol + '/lowesteverticksize',None)
    validate_api_response(r,symbol)
    return float(r.data)

def margin(symbol):
    r = get_api_data('security',symbol + '/margin',None)
    validate_api_response(r,symbol)
    return float(r.data)

def point_value(symbol):
    r = get_api_data('security',symbol + '/pointvalue',None)
    validate_api_response(r,symbol)
    return float(r.data)

def tick_size(symbol):
    r = get_api_data('security',symbol + '/ticksize',None)
    validate_api_response(r,symbol)
    return float(r.data)

def first_notice_date(symbol):
    r = get_api_data('security',symbol + '/firstnoticedate',None)
    validate_api_response(r,symbol)
    return bytes.decode(r.data)

def base_symbol(symbol):
    r = get_api_data('security',symbol + '/basesymbol',None)
    validate_api_response(r,symbol)
    return bytes.decode(r.data)


#######################################################################################################
#                           TIMESERIES
#######################################################################################################
def price_timeseries(symbol,
                          stock_price_adjustment_setting=StockPriceAdjustmentType.CAPITALSPECIAL,
                          padding_setting=PaddingType.NONE,
                          start_date="1800-01-01",
                          end_date="2999-01-01",
                          limit=-1,
                          format='numpy-recarray'):
    lowercase_columns = False
    if (format == 'pandas-dataframe-zipline'):
        format = 'pandas-dataframe'
        lowercase_columns = True
    parameters = { 'start_date': start_date,
                    'end_date': end_date,
                    'limit':str(limit),
                    'stock_price_adjustment_setting':stock_price_adjustment_setting.name,
                    'padding_setting':padding_setting.name,
                    'format':format }
    r = get_api_data('prices',symbol,parameters)
    validate_api_response(r,symbol)
    if (format == 'numpy-recarray'):
        return create_numpy_recarray(r,None)
    if (format == "pandas-dataframe"):
        return create_pandas_dataframe(r,None,lowercase_columns)
    if (format == 'numpy-ndarray'):
        return create_numpy_ndarray(r,None)


###############
def capital_event_timeseries(symbol,
                          padding_setting=PaddingType.NONE,
                          start_date="1800-01-01",
                          end_date="2999-01-01",
                          limit=-1,
                          format="numpy-recarray",
                          pandas_dataframe=None,
                          numpy_ndarray=None,
                          numpy_recarray=None,):
    if pandas_dataframe is not None or numpy_ndarray is not None or numpy_recarray is not None:
        start_date,end_date,limit = validate_existing_array(pandas_dataframe,numpy_ndarray,numpy_recarray,format)
    parameters = { 'start_date': start_date,
                    'end_date': end_date,
                    'limit':str(limit),
                    'padding_setting':padding_setting.name,
                    'format':format }
    r = get_api_data('capitalevent',symbol,parameters)
    validate_api_response(r,symbol)
    if (format == 'numpy-recarray'):
        return create_numpy_recarray(r,numpy_recarray)
    if (format == "pandas-dataframe"):
        return create_pandas_dataframe(r,pandas_dataframe)
    if (format == 'numpy-ndarray'):
        return create_numpy_ndarray(r,numpy_ndarray)

###############


def dividend_yield_timeseries(symbol,
                          padding_setting=PaddingType.NONE,
                          start_date="1800-01-01",
                          end_date="2999-01-01",
                          limit=-1,
                          format="numpy-recarray",
                          pandas_dataframe=None,
                          numpy_ndarray=None,
                          numpy_recarray=None,):
    if pandas_dataframe is not None or numpy_ndarray is not None or numpy_recarray is not None:
        start_date,end_date,limit = validate_existing_array(pandas_dataframe,numpy_ndarray,numpy_recarray,format)
    parameters = { 'start_date': start_date,
                    'end_date': end_date,
                    'limit':str(limit),
                    'padding_setting':padding_setting.name,
                    'format':format }
    r = get_api_data('dividendyield',symbol,parameters)
    validate_api_response(r,symbol)
    if (format == 'numpy-recarray'):
        return create_numpy_recarray(r,numpy_recarray)
    if (format == "pandas-dataframe"):
        return create_pandas_dataframe(r,pandas_dataframe)
    if (format == 'numpy-ndarray'):
        return create_numpy_ndarray(r,numpy_ndarray)


###############



def index_constituent_timeseries(symbol,
                          indexname,
                          padding_setting=PaddingType.NONE,
                          start_date="1800-01-01",
                          end_date="2999-01-01",
                          limit=-1,
                          format="numpy-recarray",
                          pandas_dataframe=None,
                          numpy_ndarray=None,
                          numpy_recarray=None,):
    if pandas_dataframe is not None or numpy_ndarray is not None or numpy_recarray is not None:
        start_date,end_date,limit = validate_existing_array(pandas_dataframe,numpy_ndarray,numpy_recarray,format)

    parameters = { 'start_date': start_date,
                    'end_date': end_date,
                    'indexname' : indexname,
                    'limit':str(limit),
                    'padding_setting':padding_setting.name,
                    'format':format }
    r = get_api_data('indexconstituent',symbol,parameters)
    validate_api_response(r,symbol)
    if (format == 'numpy-recarray'):
        return create_numpy_recarray(r,numpy_recarray)
    if (format == "pandas-dataframe"):
        return create_pandas_dataframe(r,pandas_dataframe)
    if (format == 'numpy-ndarray'):
        return create_numpy_ndarray(r,numpy_ndarray)



###############
def major_exchange_listed_timeseries(symbol,
                             padding_setting=PaddingType.NONE,
                          start_date="1800-01-01",
                          end_date="2999-01-01",
                          limit=-1,
                          format="numpy-recarray",
                          pandas_dataframe=None,
                          numpy_ndarray=None,
                          numpy_recarray=None):
    if pandas_dataframe is not None or numpy_ndarray is not None or numpy_recarray is not None:
        start_date,end_date,limit = validate_existing_array(pandas_dataframe,numpy_ndarray,numpy_recarray,format)

    parameters = { 'start_date': start_date,
                    'end_date': end_date,
                    'limit':str(limit),
                    'padding_setting':padding_setting.name,
                    'format':format }
    r = get_api_data('majorexchangelisted',symbol,parameters)
    validate_api_response(r,symbol)
    if (format == 'numpy-recarray'):
        return create_numpy_recarray(r,numpy_recarray)
    if (format == "pandas-dataframe"):
        return create_pandas_dataframe(r,pandas_dataframe)
    if (format == 'numpy-ndarray'):
        return create_numpy_ndarray(r,numpy_ndarray)

###############
def padding_status_timeseries(symbol,
                             padding_setting=PaddingType.NONE,
                          start_date="1800-01-01",
                          end_date="2999-01-01",
                          limit=-1,
                          format="numpy-recarray",
                          pandas_dataframe=None,
                          numpy_ndarray=None,
                          numpy_recarray=None,):
    if pandas_dataframe is not None or numpy_ndarray is not None or numpy_recarray is not None:
        start_date,end_date,limit = validate_existing_array(pandas_dataframe,numpy_ndarray,numpy_recarray,format)
    parameters = { 'start_date': start_date,
                    'end_date': end_date,
                    'limit':str(limit),
                    'padding_setting':padding_setting.name,
                    'format':format }
    r = get_api_data('paddingstatus',symbol,parameters)
    validate_api_response(r,symbol)
    if (format == 'numpy-recarray'):
        return create_numpy_recarray(r,numpy_recarray)
    if (format == "pandas-dataframe"):
        return create_pandas_dataframe(r,pandas_dataframe)
    if (format == 'numpy-ndarray'):
        return create_numpy_ndarray(r,numpy_ndarray)

#######################################################################################################
#                           INFORMATIONAL - UPDATE RELATED
#######################################################################################################

def last_database_update_time(databasename):
    r = get_api_data('database',databasename + '/lastupdatetime',None)
    validate_api_response(r,databasename)
    result = str(r.data)
    return result

def last_price_update_time(symbol):
    r = get_api_data('security',symbol + '/lastupdatetime',None)
    validate_api_response(r,symbol)
    result = str(r.data)
    return result


#######################################################################################################
#                           WATCHLIST
#######################################################################################################

def watchlist(watchlistname):
    parameters = { 'format':'csv' }
    r = get_api_data('watchlist',watchlistname,parameters)
    validate_api_response(r,watchlistname)
    txtlines = r.data.decode().splitlines()
    lines = csv.reader(txtlines, delimiter=',')
    symbols = []
    for line in lines:
        if (line[0] == 'Symbol'):
            continue
        symbols.append({ 'symbol':line[0], 'assetid':int(line[1]), 'securityname':line[2] })
    return symbols

def watchlist_symbols(watchlistname):
    parameters = { 'format':'symbolsonly' }
    r = get_api_data('watchlist',watchlistname,parameters)
    validate_api_response(r,watchlistname)
    symbols = r.data.decode().splitlines()
    return symbols

def watchlists():
    r = get_api_data('watchlists',None,None)
    validate_api_response(r,'watchlists')
    symbols = r.data.decode().splitlines()
    return symbols




#######################################################################################################
#                           FUNDAMENTALS
#######################################################################################################
def fundamental(symbol,field):  
    # Returns both the field value and date
    r = get_api_data('fundamental',symbol,None)
    validate_api_response(r,symbol)
    # result = bytes.decode(r.data);

    fundamentalresult,fundadate = r.data.decode().split(',')
    return fundamentalresult,fundadate 


#######################################################################################################
#                           CLASSIFICATION RELATED
#######################################################################################################
def classification(symbol,schemename,classificationresulttype):
    # TODO: Return array with all types
    parameters = { 'schemename': schemename,
                    'classificationresulttype': classificationresulttype }
    r = get_api_data('security',symbol + '/classification',parameters)
    validate_api_response(r,symbol)
    result = bytes.decode(r.data)
    return result

def classification_at_level(symbol,schemename,classificationresulttype,level):
    # TODO: Return array with all types
    parameters = { 'schemename': schemename,
                    'classificationresulttype': classificationresulttype,
                    'level': level }
    r = get_api_data('security',symbol + '/classification',parameters)
    validate_api_response(r,symbol)
    result = bytes.decode(r.data)
    return result

def corresponding_industry_index(symbol,indexfamilycode,level,indexreturntype):
    # TODO: Return array with all types
    parameters = { 'schemename': schemename,
                    'classificationresulttype': classificationresulttype,
                    'level': level,
                    'indexreturntype' : indexreturntype }
    r = get_api_data('security',symbol + '/industryindex',parameters)
    validate_api_response(r,symbol)
    result = bytes.decode(r.data)
    return result

print ('NorgateData package v' + __version__ + ': Init complete')
