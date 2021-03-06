#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import da
import json 
from datetime import *
import search


urls = (     
    "/new", "New",
    "/edit", "Edit",
    "/list","List",
    "/list3","List3",
    "/total","Total",
    "/android_page","AndroidPage",
    "/search","Search",
    "/profile","Profile",
    "/account_mobile_code","account_mobile_code",
    "/account_mobile_validate","account_mobile_validate",
    "/account_password_change","account_password_change", 
    "/account_password_find", "account_password_find",
    "/account_email_validate","account_email_validate")

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
        i = web.input(content='',local_id=0,creation_date=None,last_update=None)  

        content = web.websafe(i.content)
        pk_id = da.subject.insert2(self.token.user_id,i.content,
            self.token.device_type,self.token.device_no,i.local_id,
            i.creation_date,i.last_update) 

        task = da.subject.load_by_id(pk_id)

        try:
            search.make_index(task)
        except:
            pass  

        task.local_id = i.local_id  #local_id必须是本次请求的id
        #cron.update_term_count(task) #remove to eda?
        r = {"code":1,"data":task}
        return json.dumps(r,cls=CJsonEncoder) 

class Edit:
    @validate_token
    def POST(self):
        i = web.input(remote_id=0,local_id=0,content='',is_todo=0,is_remind=0,parent_id=0,
            local_version=0,is_del=0,plan_start_date=None,task_status=0,
            remind_datetime=None,remind_next=None,remind_frequency=0,closed_date=None)  
        content = web.websafe(i.content)
        da.subject.update(i.remote_id,self.token.user_id,
            body=i.content,is_todo=i.is_todo,is_remind=i.is_remind,
            parent_id=i.parent_id,version=i.local_version,is_delete=i.is_del,
            plan_start_date = i.plan_start_date,task_status=i.task_status,
            remind_datetime=i.remind_datetime,remind_next=i.remind_next,remind_frequency=i.remind_frequency,
            closed_date=i.closed_date)         
        task = da.subject.load_by_id(i.remote_id) 
        try:
            search.make_index(task)
        except:
            pass  

        task.local_id = i.local_id        
        r = {"code":1,"data":task}
        return json.dumps(r,cls=CJsonEncoder) 

class Total:
    @validate_token
    def GET(self): 
        count = da.subject.load_count(self.token.user_id)
        r = {'code':1,'total':count,'user_id':self.token.user_id}
        return json.dumps(r)

class List:
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

import search
class Search:
    @validate_token
    def GET(self):
        i = web.input(query="",offset=0,size=100)         
        rows = search.search(self.token.user_id,i.query,i.offset,i.size)
        r = {'code':1,'list':rows,'user_id':self.token.user_id}
        return  json.dumps(r,cls=CJsonEncoder)

class Profile:
    @validate_token
    def GET(self): 
        profile = da.user.load_user(self.token.user_id)
        r = {'code':1,'data':profile}
        return  json.dumps(r,cls=CJsonEncoder)

#@validate_token
class AndroidPage:   
    def GET(self):
        web.header('Content-Type', 'text/html; charset=utf-8')
        i = web.input(module="",item="")
        render = web.template.frender('templates/android/' + i.module + '.html')
        profile = da.user.load_user(1)
        return render(profile) 

############################################
class account_mobile_code:   
    def GET(self):
        i = web.input(user_id=0,mobile="") #无需验证token等
        r = {'code':1,"user_id":i.user_id,"mobile":i.mobile,'data':None}
        return  json.dumps(r,cls=CJsonEncoder)

class account_mobile_validate:       
    def POST(self):
        i = web.input(user_id=0,mobile="",sms_code="") #无需验证token等
        r = {'code':1,"user_id":i.user_id,"mobile":i.mobile,'data':None}
        return  json.dumps(r,cls=CJsonEncoder)

class account_password_change:      
    def POST(self):
        i = web.input(user_id=0,oldpwd="",newpwd="") #无需验证token等 
        r = {'code':1,"user_id":i.user_id,'data':None}
        return  json.dumps(r,cls=CJsonEncoder)

class account_password_find:       
    def GET(self):
        i = web.input(mobile="",code="") #无需验证token等
        r = {'code':1,'data':None}
        return  json.dumps(r,cls=CJsonEncoder)

class account_email_validate:   
    def POST(self):
        i = web.input(user_id=0,email="",password="") #无需验证token等?
        r = {'code':1, "user_id":i.user_id,"email":i.email,'data':None}
        return  json.dumps(r,cls=CJsonEncoder)


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