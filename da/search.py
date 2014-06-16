#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
from config import dbr,dbw





def term_insert(term):
    tname = 'terms'
    result = list(dbr.select(tname,where="term=$term",vars=locals()))
    if not result:
        return dbw.insert(tname,term=term,term_len=len(term),last_update=web.SQLLiteral('now()'))
    return result[0].term_id

    #return dbw.query("replace into public_terms(term)values('%s')" %( term )  )
    #term_id ?


def term_doc_insert(user_id,term_id,doc_id,term_count):
    dbw.query("replace into term_doc(term_id,doc_id,term_count)values(%s,%s,%s)" % (term_id,doc_id,term_count)) 


def compute_tf_idf():
    #数据量非常小的情况下可以这样用，数据量大就需要编写hadoop脚本
    dbw.query("""update terms as t, (SELECT term_id, count(*) as count FROM term_doc group by term_id) as tmp
        set t.count_domain = tmp.count
        where t.term_id=tmp.term_id;""")
    #update term's idf
    r = dbw.select('subjects',what="count(*) as count")  #select count(*) as count from subjects;
    doc_total_count = r[0].count    
    dbw.query("update terms set idf_domain=LOG(%s/(count_domain+1))" % doc_total_count )
    #update term's tf
    dbw.query("""update term_doc as t,
    (SELECT doc_id, sum(term_count) as doc_term_count FROM term_doc group by doc_id) as tmp
    set t.tf = t.term_count/tmp.doc_term_count
    where t.doc_id = tmp.doc_id""")
    #update term's tf-idf
    dbw.query("""update term_doc as td,
    terms as t
    set td.tf_idf = td.tf*t.idf_domain
    where td.term_id = t.term_id """)

def load_terms(terms):
    rows = list(dbr.select('terms',what="term_id,term",where="term in $terms",vars=locals()))
    d={}
    for r in rows:
        d[r.term] = r
    return d


def load_subjects(user_id,terms):
    result = load_terms(terms)
    term_ids = [str(k.term_id) for k in result.values()]
    rows = list(dbr.select('term_doc',what="doc_id",where="user_id=$user_id and term_id in $term_ids",vars=locals()))
    
    r = dbr.query("""select s.pk_id,user_id,s.body,s.created_date,s.last_update,s.local_id from 
        (SELECT doc_id,sum(tf_idf) as tf_idf FROM term_doc  where user_id=%s and  term_id in (%s) group by doc_id) as t
        left join subjects s on t.doc_id = s.pk_id
        order by t.tf_idf desc""" %(str(user_id),','.join(term_ids)) )
    return list(r)

    #compute 匹配度
    doc_ids = [r.doc_id for r in rows]
    subjects = list(dbr.select('subjects',
        what="pk_id,user_id,body,created_date,last_update,local_id", 
        where="user_id=$user_id and pk_id in $doc_ids",vars=locals()))
    return subjects
