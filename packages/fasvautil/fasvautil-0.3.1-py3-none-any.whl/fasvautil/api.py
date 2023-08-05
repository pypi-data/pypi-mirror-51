# -*- coding: utf-8 -*-
# Copyright (c) 2019 by Lars Klitzke, Lars.Klitzke@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from concurrent.futures import ThreadPoolExecutor

import requests
from fasvaorm.schema import SignalSchema
from requests.auth import HTTPBasicAuth

from fasvautil.io import to_epoch

import pandas as pd


def query_api(api, entry, user, password):
    """
    Query the FASva RESTful-API

    Args:
        api (str):                  The URL of the API.
        entry (str):                The query statement
        user (str):                 The name of the user
        password (str):             The password

    Returns:
        str:                        The result as JSON encoded string
    """
    result = requests.get('{api}/{entry}'.format(
            api=api,
            entry=entry),
            auth=HTTPBasicAuth(user, password)).text

    try:
        return pd.read_json(result)
    except ValueError:
        return pd.read_json(result, typ='series')


def query_scenes(api, drive, idsignals, user, password, start=None, end=None):
    """
    Get scenes from the FASva RESTFul-API.

    Args:
        api (str):                  The URL of the API.
        drive (Drive):              The drive to get the scenes from.
        idsignals (list[int]|int):  The id's of the signals
        user (str):                 The name of the user
        password (str):             The password
        start (datetime.datetime):  The start of the interval
        end (datetime.datetime):    The end of the interval

    Returns:
        pd.DataFrame: The result of the request as `DataFrame`
    """

    if not isinstance(idsignals, (tuple, list)):
        idsignals = str(idsignals)
    else:
        idsignals = ",".join([str(v) for v in idsignals])

    if start is None and end is None:
        start = drive.start
        end = drive.end

    drive_scenes = query_api(api,
                             'scene/start/{start_time}/end/{end_time}/drive/{iddrive}?idsignal={ids}'.format(
                                 start_time=to_epoch(start),
                                 end_time=to_epoch(end),
                                 iddrive=drive.iddrive,
                                 ids=idsignals),
                             user, password)

    drive_scenes.timestamp = pd.to_datetime(drive_scenes.timestamp)

    return drive_scenes


def query_signals(api, signals, user, password):
    """
    Get the signals with the given names.

    Args:
        api (str):                  The URL of the API.
        signals (list[str]|str):    The name(s) of the signal(s) to query
        user (str):                 The name of the user
        password (str):             The password

    Returns:
        pd.Series|pd.DataFrame:     The signal entries as a pandas Series or as rows in a pandas DataFrame
    """

    if not isinstance(signals, (list, tuple)):
        return query_api(api, 'signal/{name}'.format(name=signals), user, password)

    with ThreadPoolExecutor() as pool:
        futures = [pool.submit(query_api, api, 'signal/{name}'.format(name=name), user, password) for name in signals]

    r = [f.result() for f in futures]

    return pd.DataFrame(r)
