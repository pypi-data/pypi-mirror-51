###########################################
## System, File, Data Structure 관련 import
###########################################

import os
import glob
import shutil
from itertools import chain

###########################################
##         Math, 자료형 관련 import
###########################################

import json
import math
import random

###########################################
##         Data 받기
###########################################

import requests

###########################################
##         데이터분석 툴
###########################################

import pandas as pd
from pandas.io.json import json_normalize
import numpy as np
###########################################
##         Process, Thread
###########################################

from matplotlib import font_manager, rc, pyplot as plt
import seaborn as sns

###########################################
##         Process, Thread
###########################################

try:
    import thread
except ImportError:
    import _thread as thread

###########################################
##          날짜관련 import
###########################################

import time
from datetime import datetime, timedelta
import calendar
from dateutil.relativedelta import relativedelta
import pytz

###########################################
## Multiprocessing 관련
###########################################

from multiprocessing import Pool, Queue, Process, Pipe, freeze_support

###########################################
##              Asyncio 관련
###########################################

import concurrent.futures
import asyncio

###########################################
##          websocket 관련
###########################################

import websocket

###########################################
##              Zero MQ
###########################################

import zmq

###########################################
##            Protocol Buffers
###########################################

from hexpot.hexpot_pb import cpformat_pb2
from google.protobuf.json_format import MessageToJson
import stream


###########################################################################
##                          General Tools
###########################################################################


## 프로그램 작동 시간 측정 데코레이터
"""
opening_time = time.time()
closing_time = time.time()
print(closing_time-opening_time)
"""
# def runtime(f):
#     def wrapper(*args, **kwargs):
#         import time
#         start = time.time()
#         f
#         end = time.time()
#         print(end - start)
#         return f()
#     return wrapper

def timestamp_into_kst_time(ts):
    KST = pytz.timezone('Asia/Seoul')
    try:
        dt = datetime.utcfromtimestamp(ts)
        k_dt = pytz.utc.localize(dt).astimezone(KST)
        return k_dt
    except:
        return np.nan


## Date list generator

def generate_day_list(start_date,end_date=None):

    start_date = datetime.strptime(start_date,'%Y-%m-%d')

    if end_date == None :
        end_date = datetime.today()
    else :
        end_date = datetime.strptime(end_date,'%Y-%m-%d')

    delta = end_date - start_date
    date_list = []

    for i in range(delta.days + 1):
        d = start_date + timedelta(days=i)
        date_list = date_list + [d.strftime("%Y-%m-%d")]

    return date_list

def generate_day_index_df(start_date,end_date=None):

    start_date = datetime.strptime(start_date,'%Y-%m-%d')

    if end_date == None :
        end_date = datetime.today()
    else :
        end_date = datetime.strptime(end_date,'%Y-%m-%d')

    delta = end_date - start_date
    date_list = []

    for i in range(delta.days + 1):
        d = start_date + timedelta(days=i)
        date_list = date_list + [d.strftime("%Y-%m-%d")]

    df = pd.DataFrame(index=date_list)
    df.index = pd.to_datetime(df.index)

    return df


def check_dir(dir_path):
    if os.path.exists(dir_path):
        pass
    else:
        os.mkdir(dir_path)

def mk_new_dir(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(path=dir_path)
    os.mkdir(dir_path)

def get_coin_tick_price_df(market,coin,start_datetime,end_datetime,input_dir_path,pb_class=cpformat_pb2.CoinPrice):

    start_date = start_datetime.split('T')[0]
    end_date = end_datetime.split('T')[0]

    to_do_candidate_list = generate_day_list(start_date=start_date,end_date=end_date)

    file_list = glob.glob(input_dir_path+'\\{}_{}_****-**-**.gz'.format(market,coin))
    to_do_file_path_list = []
    to_do_date_list = []

    for fp in file_list:
        file_date = fp.split('{}_{}_'.format(market,coin))[-1][:-3]
        if file_date in to_do_candidate_list:
            to_do_date_list.append(file_date)
            to_do_file_path_list.append(fp)


    for i in range(len(to_do_date_list)):
        input_file_name = '{}_{}_{}.gz'.format(market, coin, to_do_date_list[i])
        input_file_path = '{}\\{}'.format(input_dir_path,input_file_name)

        input_stream_file = stream.parse(ifp=input_file_path, pb_cls=pb_class)
        k=0
        for x in input_stream_file:

            if (i==0)&(k==0):
                js_frag = MessageToJson(x)
                df_frag = json_normalize(json.loads(js_frag))
                result_df_columns = list(df_frag.columns)
                result_df = pd.DataFrame(columns=result_df_columns)

            js_frag = MessageToJson(x)
            df_frag = json_normalize(json.loads(js_frag))
            result_df = result_df.append(df_frag)

            k+=1

        input_stream_file.close()

    result_df['tms'] = result_df['tms'].map(lambda x:timestamp_into_kst_time(float(x)/1000).replace(tzinfo=None).strftime('%Y-%m-%dT%H:%M:%S'))
    result_df = result_df[(result_df['tms']>=start_datetime)&(result_df['tms']<end_datetime)]
    result_df = result_df.reset_index(drop=True)

    return result_df


def get_merged_coin_tick_price_data_file(market, coin, start_date, end_date, input_dir_path, output_dir_path, pb_cls=cpformat_pb2.CoinPrice):

    to_do_candidate_list = generate_day_list(start_date=start_date,end_date=end_date)

    file_list = glob.glob(input_dir_path+'\\{}_{}_****-**-**.gz'.format(market,coin))
    to_do_file_path_list = []
    to_do_date_list = []

    for fp in file_list:
        file_date = fp.split('{}_{}_'.format(market,coin))[-1][:-3]
        if file_date in to_do_candidate_list:
            to_do_date_list.append(file_date)
            to_do_file_path_list.append(fp)

    min_date = min(to_do_date_list)
    max_date = max(to_do_date_list)

    output_file_name = '{}_{}_{}_{}.gz'.format(market,coin,min_date.replace('-',''),max_date.replace('-',''))
    output_file_path = output_dir_path+'\\{}'.format(output_file_name)

    with stream.open(output_file_path,'a') as output_stream_file:

        for cur_date in to_do_date_list:
            input_file_name = '{}_{}_{}.gz'.format(market, coin, cur_date)
            input_file_path = '{}\\{}'.format(input_dir_path,input_file_name)

            input_stream_file = stream.parse(ifp=input_file_path, pb_cls=pb_cls)
            for x in input_stream_file:
                output_stream_file.write(x)

    print('Merging Files / Completed / File Name : {}'.format(output_file_name))


def load_coin_tick_price_data_on_the_date_generator(market, coin, date, file_dir_path, pb_cls=cpformat_pb2.CoinPrice):

    file_name = '{}_{}_{}.gz'.format(market, coin, date)
    data_file_path = '{}\\{}'.format(file_dir_path, file_name)
    f = stream.parse(ifp=data_file_path, pb_cls=pb_cls)

    return f


def load_coin_tick_price_data_generator(market, coin, start_dt_str, end_dt_str, file_dir_path, pb_cls=cpformat_pb2.CoinPrice):

    start_date = start_dt_str.split('T')[0]
    end_date = end_dt_str.split('T')[0]

    start_ts_str = str(int(datetime.strptime(start_dt_str,'%Y-%m-%dT%H:%M:%S').timestamp()*1000))
    end_ts_str = str(int(datetime.strptime(end_dt_str,'%Y-%m-%dT%H:%M:%S').timestamp()*1000))

    to_do_candidate_list = generate_day_list(start_date=start_date,end_date=end_date)

    file_name = '{}_{}_****-**-**.gz'.format(market,coin)
    file_path = '{}\\{}'.format(file_dir_path,file_name)
    file_list = glob.glob(file_path)
    to_do_file_path_list = []
    to_do_date_list = []

    for fp in file_list:
        file_date = fp.split('{}_{}_'.format(market,coin))[-1][:-3]
        if file_date in to_do_candidate_list:
            to_do_date_list.append(file_date)
            to_do_file_path_list.append(fp)

    to_do_file_path_list.sort(reverse=False)

    for fp_inx in range(len(to_do_file_path_list)):
        if fp_inx==0:
            fp = to_do_file_path_list[fp_inx]
            t = stream.parse(ifp=fp, pb_cls=pb_cls)
            continue
        fp = to_do_file_path_list[fp_inx]
        f = stream.parse(ifp=fp, pb_cls=pb_cls)
        t = chain(t,f)

    def filtered_gen_func():
        for x in t:
            if (x.tms < start_ts_str)|(x.tms >= end_ts_str):
                continue
            yield x

    return filtered_gen_func()

def get_ohlcv_df_from_tick_price_data_generator(generator,time_interval,start_dt_str,end_dt_str):

    k = 0

    for msg in generator:

        cur_datetime = timestamp_into_kst_time(float(msg.tms) / 1000).replace(tzinfo=None)
        cur_dt_str = cur_datetime.strftime('%Y-%m-%dT%H:%M:%S')

        ## Start Datetime 이후부터 시작 & End Datetime 이전까지만

        if (cur_dt_str<start_dt_str)|(cur_dt_str>=end_dt_str):
            continue

        js_frag = json.loads(MessageToJson(message=msg))
        df_frag = json_normalize(js_frag)
        df_frag.index = [cur_datetime]
        df_frag = df_frag.resample(rule=time_interval).first()
        cur_datetime = df_frag.index[0]

        ## 맨처음 루프시에는 리스트 생성

        if k == 0:
            prior_datetime = cur_datetime
            ohlc_result_list = list()
            ohlc_df_frag_list = list()
            k += 1

        ## 계속된 루프시 루틴

        if prior_datetime == cur_datetime:
            ohlc_df_frag_list.append(df_frag)
            continue
        else:
            ## ohlc 완성
            if len(ohlc_df_frag_list) == 0:
                continue
            elif len(ohlc_df_frag_list) == 1:
                row = ohlc_df_frag_list[0].iloc[0]
                ohlc_dict = {'datetime': row.name.strftime('%Y-%m-%dT%H:%M:%S'), 'open': row['price'], 'high': row['price'], 'low': row['price'], 'close': row['price'],'mean':row['price'],'median':row['price'], 'volume': row['volume']}
                ohlc_json = json.dumps(ohlc_dict)

            else:
                merged_ohlc_df_frag = pd.concat(ohlc_df_frag_list)
                o = merged_ohlc_df_frag['price'].iloc[0]
                h = merged_ohlc_df_frag['price'].max()
                l = merged_ohlc_df_frag['price'].min()
                c = merged_ohlc_df_frag['price'].iloc[-1]
                mn = merged_ohlc_df_frag['price'].mean()
                md = merged_ohlc_df_frag['price'].median()
                v = merged_ohlc_df_frag['volume'].sum()
                ohlc_dict = {'datetime': merged_ohlc_df_frag.iloc[0].name.strftime('%Y-%m-%dT%H:%M:%S'), 'open': o, 'high': h, 'low': l, 'close': c,'mean':mn,'median':md, 'volume': v}
                ohlc_json = json.dumps(ohlc_dict)

            ## 리셋

            ohlc_df_frag_list = list()
            ohlc_df_frag_list.append(df_frag)

            ## 데이터 처리 & 모니터링
            # print(ohlc_json)
            ohlc_result_list.append(ohlc_json)

        prior_datetime = cur_datetime
        k += 1

    ## ohlc 완성
    if len(ohlc_df_frag_list) == 0:
        pass
    elif len(ohlc_df_frag_list) == 1:
        row = ohlc_df_frag_list[0].iloc[0]
        ohlc_dict = {'datetime': row.name.strftime('%Y-%m-%dT%H:%M:%S'), 'open': row['price'], 'high': row['price'], 'low': row['price'], 'close': row['price'],'mean':row['price'],'median':row['price'], 'volume': row['volume']}
        ohlc_json = json.dumps(ohlc_dict)
        ohlc_result_list.append(ohlc_json)
    else:
        merged_ohlc_df_frag = pd.concat(ohlc_df_frag_list)
        o = merged_ohlc_df_frag['price'].iloc[0]
        h = merged_ohlc_df_frag['price'].max()
        l = merged_ohlc_df_frag['price'].min()
        c = merged_ohlc_df_frag['price'].iloc[-1]
        mn = merged_ohlc_df_frag['price'].mean()
        md = merged_ohlc_df_frag['price'].median()
        v = merged_ohlc_df_frag['volume'].sum()
        ohlc_dict = {'datetime': merged_ohlc_df_frag.iloc[0].name.strftime('%Y-%m-%dT%H:%M:%S'),'open': o, 'high': h, 'low': l, 'close': c,'mean':mn,'median':md, 'volume': v}
        ohlc_json = json.dumps(ohlc_dict)
        ohlc_result_list.append(ohlc_json)

    ohlc_result_df = pd.DataFrame([json.loads(x) for x in ohlc_result_list]).reset_index(drop=True)

    return ohlc_result_df



class hexpo_trader():
    def __init__(self,rcv_port,snd_port):
        self.rcv_port = rcv_port
        self.snd_port = snd_port

        self.rcv_settings()
        self.snd_settings()

    def rcv_settings(self):
        self.context = zmq.Context()
        self.data_receiver = self.context.socket(zmq.SUB)
        self.data_receiver.connect("tcp://127.0.0.1:{}".format(self.rcv_port))
        self.data_receiver.setsockopt_string(zmq.SUBSCRIBE,"")

    def snd_settings(self):
        self.context = zmq.Context()
        self.data_sender = self.context.socket(zmq.PUB)
        self.data_sender.bind("tcp://127.0.0.1:{}".format(self.snd_port))

    def default_settings(self):
        pass

    def main(self):
        pass



