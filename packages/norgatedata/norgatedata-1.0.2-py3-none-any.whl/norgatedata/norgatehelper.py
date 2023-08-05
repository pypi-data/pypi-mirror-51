import urllib3
import urllib
import sys
import pandas as pd
import numpy as np
import numpy.lib.recfunctions as rfn
import inspect
import csv
from enum import Enum
import requests
import json
import os
from os.path import exists, expanduser, join
import inspect
from time import time
import warnings
from errno import EEXIST

try:
    from packaging.version import parse
except ImportError:
    from pip._vendor.packaging.version import parse

# Global vars
httppool = urllib3.PoolManager()
norgate_web_api_base_url = 'http://localhost:38889/api/v1/'

#######################################################################################################
# Internal helper functions
#######################################################################################################
def build_api_url(dataitem,item,parameters=None):
    url = norgate_web_api_base_url + dataitem
    if (item is not None):
        item = str(item)
        url += '/' + urllib.parse.quote(item)
    #parameters["pyfile"] = __file__ # for diagnosis
    #parameters["pymain"] = '__main__' # for diagnosis
    #parameters["pyargv0"] = sys.argv[0] # for diagnosis
    if (parameters is not None):
        url += '?' + urllib.parse.urlencode(parameters)
    return url

def get_api_data(dataitem,item,parameters=None):
    url = build_api_url(dataitem,item,parameters)
    try:
        apiresponse = httppool.request('GET', url)
    except Exception:
        raise ValueError("Unable to obtain Norgate Data - perhaps NDU is not running?")
    return apiresponse

def validate_existing_array(pandas_dataframe,numpy_ndarray,numpy_recarray,format):
    if pandas_dataframe is not None:
        start_date,end_date,limit = validate_dataframe(pandas_dataframe,format)
    if numpy_ndarray is not None:
        start_date,end_date,limit = validate_ndarray(numpy_ndarray,format)
    if numpy_recarray is not None:
        start_date,end_date,limit = validate_recarray(numpy_recarray,format)
    return start_date,end_date,limit

def validate_dataframe(pandas_dataframe,format):
    if (format != 'pandas-dataframe'):
        raise ValueError("Format specified is " + format + " but the parameter pandas_dataframe was provided.  You need to pass in an array of the same type as the format you require.  Perhaps you didn't explicitly specify the format?")
    if (not(isinstance(pandas_dataframe,pd.core.frame.DataFrame))):
        raise ValueError(inspect.currentframe().f_back.f_code.co_name + ": pandas_dataframe passed was not a Pandas DataFrame - it is actually " + str(type(pandas_dataframe)))
    if (pandas_dataframe.index.name != 'Date'):
        raise ValueError(inspect.currentframe().f_back.f_code.co_name + ": Expected dataframe to have index of Date but found " + pandas_dataframe.index.name)
    start_date = pandas_dataframe.first_valid_index()
    end_date = pandas_dataframe.last_valid_index()
    limit = -1
    return start_date,end_date,limit

def validate_recarray(numpy_recarray,format):
    if (format != 'numpy-recarray'):
        raise ValueError("Format specified is " + format + " but the parameter numpy_recarray was specified. You need to pass in an array of the same type as the format you require.  Perhaps you didn't explicitly specify the format?")
    if (not(isinstance(numpy_recarray,np.recarray))):
        raise ValueError(inspect.currentframe().f_back.f_code.co_name + ": numpy_recarray was not a Numpy recarray - it is actually " + str(type(numpy_recarray)))
    if (numpy_recarray.dtype.names[0] != 'Date'):
        raise ValueError(inspect.currentframe().f_back.f_code.co_name + ": Expected recarray to have first field of Date but found " + numpy_recarray.dtype.names[0])
    start_date = numpy_recarray[0][0]
    end_date = numpy_recarray[-1][0]
    limit = -1
    return start_date,end_date,limit

def validate_ndarray(numpy_ndarray,format):
    if (format != 'numpy-ndarray'):
        raise ValueError("Format specified is " + format + " but the parameter numpy_ndarray was specified.  You need to pass in an array of the same type as the format you require.  Perhaps you didn't explicitly specify the format?")
    if (not(isinstance(numpy_ndarray,np.ndarray))):
        raise ValueError(inspect.currentframe().f_back.f_code.co_name + ": numpy_ndarray was not a Numpy ndarray array - it is actually " + str(type(numpy_ndarray)))
    if (numpy_ndarray.dtype.names[0] != 'Date'):
        raise ValueError(inspect.currentframe().f_back.f_code.co_name + ": Expected recarray to have first field of Date but found " + numpy_ndarray.dtype.names[0])
    start_date = numpy_ndarray[0][0]
    end_date = numpy_ndarray[-1][0]
    limit = -1
    return start_date,end_date,limit


def validate_api_response(r,symbol):
    if (r.status == 404):
        raise ValueError(inspect.currentframe().f_back.f_code.co_name + ': ' + str(symbol) + " was not found")
    if (not (r.status == 200 or r.status == 204)) :
        raise ValueError(inspect.currentframe().f_back.f_code.co_name + ": Error in receiving Norgate Data - check paramters are correctly formatted.  Status code is: " + str(r.status))

def create_pandas_dataframe(r,pandas_dataframe=None,lowercase_columns=False):
    recordcount = int(r.headers['X-Norgate-Data-Record-Count'])
    if (lowercase_columns):
        fields = r.headers['X-Norgate-Data-Field-Names'].lower().split(',')
    else:
        fields = r.headers['X-Norgate-Data-Field-Names'].split(',')
    formats = r.headers['X-Norgate-Data-Field-Formats'].split(',')
    fieldcount = int(r.headers['X-Norgate-Data-Field-Count'])
    npdates = np.frombuffer(r.data,formats[0],recordcount)  # 'datetime64[D]'
    npdates = npdates.copy()
    indicatorType = []
    for i in range(1,fieldcount):
        indicatorType.append((fields[i],formats[i]))
    npdata = np.frombuffer(r.data,indicatorType,-1,recordcount * 8)
    npdata = npdata.copy()
    pdf = pd.DataFrame(data=npdata,index=npdates)
    pdf.index.name = fields[0]
    if pandas_dataframe is None:
        return pdf
    pandas_dataframe = pd.merge(pandas_dataframe,pdf, how='left', left_index=True, right_index=True)
    return pandas_dataframe

def create_numpy_ndarray(r,np_ndarray=None):
    recordcount = int(r.headers['X-Norgate-Data-Record-Count'])
    fields = r.headers['X-Norgate-Data-Field-Names'].split(',')
    formats = r.headers['X-Norgate-Data-Field-Formats'].split(',')
    fieldcount = int(r.headers['X-Norgate-Data-Field-Count'])
    indicatorType = []
    for i in range(0,fieldcount):
        indicatorType.append((fields[i],formats[i]))
    npdata = np.frombuffer(r.data,indicatorType,recordcount)
    if np_ndarray is not None:
        np_ndarray = rfn.join_by("Date",np_ndarray,npdata)
        return np_ndarray
    return npdata


def create_numpy_recarray(r,np_recarray=None):
    npdata = create_numpy_ndarray(r)
    npdata2 = npdata.view(np.recarray)
    if np_recarray is not None:
        np_recarray = rfn.join_by("Date",np_recarray,npdata2)
        return np_recarray
    return npdata2


def version_checker(currentversion, package):
    ensure_norgatedata_root()
    jsonfile = norgatedata_root() + "\\" + package + "_release_version.json" # this file is part of the package distribution
    newversion = '0'
    if (os.path.isfile(jsonfile)):
        file1 = open(jsonfile,"r")
        newversion = json.load(file1)
        file1.close()
    if (not (os.path.isfile(jsonfile)) or (os.path.isfile(jsonfile) and (time() - os.path.getmtime(jsonfile) > 60 * 60))): # Check once an hour
        newversion = get_latest_pypi_version(package)
        file1 = open(jsonfile,"w")
        file1.write('"' + newversion + '"')
        file1.close()
    if (newversion > currentversion):
        print("**PACKAGE VERSION WARNING*** You have version (" + currentversion + ") of the " + package + " package installed.  A newer version " + newversion + " is available and is a recommended upgraded.")

def get_latest_pypi_version(package):
    """Return version of package on pypi.python.org using json."""
    url_pattern = 'https://pypi.python.org/pypi/{package}/json'
    version = parse('0')
    try:
        req = requests.get(url_pattern.format(package=package))
        if req.status_code == requests.codes.ok:
            j = json.loads(req.text) # .encode(req.encoding))
            releases = j.get('releases', [])
            for release in releases:
                ver = parse(release)
                if not ver.is_prerelease:
                    version = max(version, ver)
    except:
        print ('Warning: Unable to obtain version data of ' + package + ' from pypi - perhaps you are offline?')
    return version.public

def norgatedata_root():
    """
    Get the root directory for all Norgate Data managed files.
    These files are primarily used for version checking/warning that a new version is available

    Returns
    -------
    root : string
        Path to the zipline root dir.
    """
    environ = os.environ
    root = environ.get('NORGATEDATA_ROOT', None)
    if root is None:
        root = expanduser('~/.norgatedata')
    return root


def ensure_norgatedata_root():
    """
    Ensure that the Norgate Data root directory exists for config files
    """
    ensure_directory(norgatedata_root())

def ensure_directory(path):
    """
    Ensure that a directory named "path" exists.
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == EEXIST and os.path.isdir(path):
            return
        raise

