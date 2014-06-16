#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import da
import json 
from datetime import *


urls = (     
    "/new", "New",
    "/list2","List2",
    "/list3","List3",
    "/total","Total",
    "/dashboard","Dashboard",
    "/search","Search")

#register, mobile + sms_validate_code
#login, mobile + password_encryption
#

def validate_token(func): #python decorator函数
    def new_func(arg1):
        i = web.input(user_id=0,access_token="")
        result = da.user.validate_token(i.user_id,i.access_token)
        if not result:
            web.ctx.status = '401 Unauthorized'
            return '{"code":-1,"data":"access_token is not validate"}' 
        arg1.token = result[0]    
        return func(arg1)
    return new_func 

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj) 

class New:
    @validate_token
    def POST(self):
        i = web.input(content='',local_id=0,creation_date=0,last_update=0)  

        content = web.websafe(i.content)
        pk_id = da.subject.insert2(self.token.user_id,i.content,
            self.token.device_type,self.token.device_no,i.local_id,
            i.creation_date,i.last_update) 

        task = da.subject.load_by_id(pk_id)
        task.local_id = i.local_id  #local_id必须是本次请求的id
        #cron.update_term_count(task) #remove to eda?
        r = {"code":1,"data":task}
        return json.dumps(r,cls=CJsonEncoder) 

class Total:
    @validate_token
    def GET(self): 
        count = da.subject.load_count(self.token.user_id)
        r = {'code':1,'total':count,'user_id':self.token.user_id}
        return json.dumps(r)

class List2:
    @validate_token
    def GET(self):
        i = web.input(offset=0,size=100)
        rows = da.subject.load_page2(self.token.user_id,i.offset,i.size)   
        #total_count = da.subject.load_count(i.user_id)

        r = {'code':1,'list':rows,'user_id':self.token.user_id,'offset':i.offset}
        return json.dumps(r,cls=CJsonEncoder)

class List3:
    @validate_token
    def GET(self):
        i = web.input(min_pk_id=1,size=50)

        rows = da.subject.load_page3(self.token.user_id,i.min_pk_id,int(i.size))
        total_count = da.subject.load_count(self.token.user_id)

        r = {'code':1,'list':rows,'total':total_count,'user_id':self.token.user_id}
        return json.dumps(r,cls=CJsonEncoder)

class Dashboard:
    def GET(self):
        #self.token.user_id
        return  "<h1>hello,world</h1>"

import search
class Search:
    @validate_token
    def GET(self):
        i = web.input(keywords="")         
        rows = search.search(self.token.user_id,i.keywords)
        return  json.dumps(rows,cls=CJsonEncoder)

def api_loadhook():
    # 如果把login剔除api，所有资源访问都可以加上user_id+device_no+access_token?
    web.header('Content-Type', 'application/json; charset=utf-8')
    # i = web.input(user_id=0,access_token="")
    # valdate_result = False # validate_access_token(i.user_id,i.device_no,i.access_token)
    # if not valdate_result:
    #     return '{"code":-1,"data":"access_token is not validate"}' 
    

def api_unloadhook():
    pass 

def init_app():
    app = web.application(urls, globals())
    #app.notfound = api_notfound
    #app.internalerror = api_internalerror
    app.add_processor(web.loadhook(api_loadhook))
    app.add_processor(web.unloadhook(api_unloadhook))    
    return app

app = init_app()