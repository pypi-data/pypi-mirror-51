# coding=utf-8
import base64
import json
from functools import wraps

import requests

from ._win_func import RegFunc


def _add_local_params(func):
    @wraps(func)
    def wras(self):
        version = RegFunc(sub_key=r'Software\Glodon\GDraw\1.0').get_value('Version')
        GetBoxParams.params['oldversion'] = version
        devid = RegFunc().get_guid()
        GetBoxParams.params['devid'] = devid
        func(self, devid, version)
    
    return wras


def read_last_line(rfile, n):
    with open(rfile, 'r') as f:
        txt = f.readlines()
    keys = [k for k in range(0, len(txt))]
    result = {k: v for k, v in zip(keys, txt[::-1])}
    for i in range(n):
        if 'return code' in result[i]:
            return result[i]



class GetBoxParams(object):
    params = dict()
    env = 'cs'
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    base_url = 'http://gsup-test.glodon.com/'
    product = '153'
    
    def _products_gdraw_params(self):
        url = self.base_url + 'api/v2/products?secret=false'
        resp = requests.get(url)
        
        products = resp.json()['info']['products']
        for item in products:
            if item['clientid'] == 'GDraw':
                GetBoxParams.params['exe'] = item['exe']
                GetBoxParams.params['logo'] = item['logo']
                GetBoxParams.params['showname'] = item['showname']
                GetBoxParams.params['optional'] = item['optional']
                GetBoxParams.params['clientid'] = item['clientid']
                GetBoxParams.params['path'] = item['path']
                break
    
    @_add_local_params
    def _record_gdraw_params(self, devid, ver):
        
        url = GetBoxParams.base_url + 'api/v2/record?secret=false'
        
        data = {
            "product": GetBoxParams.product,
            "deviceid": devid,
            "version": ver,
            "bits": "64",
            "os": 'Win7',
            "sysbits": "64",
            "updateid": "74001"
        }
        resp = requests.post(url, params=data)
        
        assert resp.json()['status'] != 5000, "没有要查询升级的产品的信息！"
        infos = resp.json()['info']
        for k, v in infos.items():
            if k == 'product_id':
                GetBoxParams.params['pid'] = infos[k]
                del infos[k]
            if k == 'name':
                GetBoxParams.params['fname'] = r'C:\ProgramData\Glodon\GSUP\download\%s' % infos[k]
                del infos[k]
            if k == 'full_update':
                GetBoxParams.params['diff'] = infos[k]
                del infos[k]
            if k == 'utype':
                if infos[k] == 1 or infos[k] == 0:
                    GetBoxParams.params['force'] = '0'
                elif infos[k] == 2:
                    GetBoxParams.params['force'] = '1'
                del infos[k]
            if k in ('can_update', 'ntype', 'args', 'message'):
                del infos[k]
        GetBoxParams.params['span'] = 'false'
        GetBoxParams.params.update(infos)
    
    def get_box_params(self, ischeck='false'):
        """
        
        :param ischeck: 是否为检查升级，有两种类型true和false，默认值为false。
        :return:
        """
        if ischeck == 'false':
            GetBoxParams.params['check'] = 'false'
        elif ischeck == 'true':
            GetBoxParams.params['check'] = 'true'
        else:
            raise ValueError('params wrong!')
        self._products_gdraw_params()
        self._record_gdraw_params()
        return GetBoxParams.params


if __name__ == '__main__':
    # import subprocess,time
    # import os
    s = GetBoxParams().get_box_params()
    p = base64.b64encode(json.dumps(s))
