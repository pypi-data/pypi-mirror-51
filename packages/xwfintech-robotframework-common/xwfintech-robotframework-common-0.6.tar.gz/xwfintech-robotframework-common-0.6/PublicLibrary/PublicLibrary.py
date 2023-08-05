#!usr/bin/env python
# coding=utf-8
from robot.api import logger
from robot.api.deco import keyword
import hashlib
import time
import json
import hashlib
import random
import pymysql
import jwt
from datetime import datetime,timedelta
from .version import VERSION


__author__ = 'bryan hou'
__email__ = 'bryanhou@gmail.com'
__version__ = VERSION

class PublicLibrary(object):

    def __int__(self):
        pass




    SECRET_KEY = "83717cf6a2ba11e8be7c787b8ad1ae43"


    @keyword('Generate BUser Token')
    def generate_bUser_token(code):

        utc_timestamp = datetime.now().timestamp()
        token = jwt.encode({"code": code, "time": utc_timestamp}, SECRET_KEY).decode()
        # utc_timestamp = datetime.now().timestamp()
        # key = "support:jwt:{}".format(code)
        # ex = 60000
        # data = {"exp_time": utc_timestamp + ex, "token": token}
        # redis.set(key, value=json.dumps(data), ex=ex)
        return token

    
    @keyword('Generate CUser Token')
    def generate_cUser_token(phone,password,uin):
        token = jwt.encode({"phone": phone, "pwd": password,
                            "exp": int((datetime.now() + timedelta(days=7)).timestamp()), "uin": uin},
                           key="",
                           ).decode()
        return token


    @keyword('getCoding')
    def getCoding(self, strInput):
        u"""
        获取编码格式
        """
        if isinstance(strInput, unicode):
            return "unicode"
        try:
            strInput.decode("utf8")
            return 'utf8'
        except:
            pass
        try:
            strInput.decode("gbk")
            return 'gbk'
        except:
            pass


    @keyword('tran2UTF8')
    def tran2UTF8(self, strInput):
        """
        转化为utf8格式
        """
        strCodingFmt = self.getCoding(strInput)
        if strCodingFmt == "utf8":
            return strInput
        elif strCodingFmt == "unicode":
            return strInput.encode("utf8")
        elif strCodingFmt == "gbk":
            return strInput.decode("gbk").encode("utf8")


    @keyword('tran2GBK')
    def tran2GBK(self, strInput):
        """
        转化为gbk格式
        """
        strCodingFmt = self.getCoding(strInput)
        if strCodingFmt == "gbk":
            return strInput
        elif strCodingFmt == "unicode":
            return strInput.encode("gbk")
        elif strCodingFmt == "utf8":
            return strInput.decode("utf8").encode("gbk")


    def md5(self, init_str):
            """
            md5加密
            """
            m = hashlib.md5()
            m.update(init_str)

            return m.hexdigest()


    @keyword('Eval Dict')
    def eval_dict(self, strInput):
        u"""接收字符串直接转成需要类型,例
         | eval dict                   | str                |
        """
        strInput = eval(strInput)

        return strInput


    @keyword('Random Num')
    def random_num(self, num):
        """
        随机出给出数字位数的数字
        """
        number = ''
        for i in random.sample(range(10), int(num)):
            number += ''.join(str(i))

        return number

    @keyword('CON DB')
    def con_db(self, sql):
        db = pymysql.connect(
            host="1.1.5.2",
            user="xxx",
            passwd="xxx",
            db="xxx",
            charset='utf8')

        cursor = db.cursor()
        cursor.execute(sql)
        data = cursor.fetchone()
        db.close()
        return data


    @keyword('Located User')
    def located_user(self,value):
        """落库地址查询"""
        relation_dict = {(1,251):"1", (251,501):"1", (501,751):"1", (751,1001):"1"}
        
        digest = int(hashlib.md5(str(value).encode()).hexdigest(), 16)
        mod = digest % 1000 + 1
        for k, v in relation_dict.items():
            if k[0]<=mod<k[1]:
                returns = str(digest % 32 + 1).zfill(2)
                return returns
    
    @keyword('Get Current Time')                
    def get_current_time(self):
        """获取当前时间"""
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time

    @keyword('Unicode To Dict')                
    def uinicode_to_dict(self,input):
        """获取当前时间"""
        inputStr = str(input)
        inputDict = json.loads(inputStr)
        return inputDict

    @keyword('GBK To Unicode')                
    def convert_gbk_2_unicode(self,input):
        """获取当前时间"""
        output = str(input).encode('unicode_escape')
        return output

    @keyword('Unicode To GBK')                
    def convert_unicode_2_gbk(self,input):
        # """Linux"""
        output = str(input).encode('utf-8').decode('unicode_escape')
        # """Windows"""
        # output = str(input).encode('unicode_escape').decode('unicode_escape')
        return output

    def str_fill(self,origin,n):
        return origin.zfill(n)

