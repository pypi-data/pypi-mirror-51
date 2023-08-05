import time 
from lmf.dbv2 import db_command,db_query
import traceback
from lmf.bigdata import pg2pg 
from sqlalchemy.dialects.postgresql import  TEXT,BIGINT,TIMESTAMP,NUMERIC

def est_gg_zhongbiao():
    sql="""
    CREATE TABLE "public"."gg_zhongbiao" (
    "html_key" int8,
    "href" text COLLATE "default",
    "ggtype" text COLLATE "default",
    "quyu" text COLLATE "default",
    "zhongbiaoren" text COLLATE "default",
    "zhaobiaoren" text COLLATE "default",
    "zbdl" text COLLATE "default",
    "zhongbiaojia" numeric,
    "kzj" numeric,
    "xmmc" text COLLATE "default",
    "xmjl" text COLLATE "default",
    "xmdz" text COLLATE "default",
    "zbfs" text COLLATE "default",
    "xmbh" text COLLATE "default",
    "gg_name" text COLLATE "default",
    "fabu_time" timestamp(6),
    "xzqh" text COLLATE "default",
    "ts_title" tsvector,
    "ent_key" int8
    )
    distributed by (html_key)"""

    conp=['gpadmin','since2015','192.168.4.206','biaost','public']

    db_command(sql,dbtype="postgresql",conp=['gpadmin','since2015','192.168.4.206','biaost','public'])

def update_gg_zhongbiao():
    sql="""
         insert into public.gg_zhongbiao( html_key,  href ,   ggtype , quyu ,   zhongbiaoren,    zhaobiaoren ,zbdl  ,  zhongbiaojia  ,  kzj, xmmc,    xmjl ,   xmdz ,
           zbfs  ,  xmbh ,   gg_name, fabu_time ,  xzqh ,   ts_title,ent_key)
        select a.html_key,  a.href ,   a.ggtype , a.quyu ,   a.zhongbiaoren, a.zhaobiaoren ,a.zbdl  ,a.zhongbiaojia  
    ,  a.kzj, a.xmmc,  a.xmjl ,   a.xmdz ,
           a.zbfs  ,  a.xmbh ,   a.gg_name, a.fabu_time ,  a.xzqh ,   a.ts_title::tsvector ts_title 
            ,b.ent_key  

            from public.et_gg_meta as a  left join "public".qy_base as b  on a.zhongbiaoren=b.jgmc  and  zhongbiaoren is not null  
    and  not exists(select 1 from gg_zhongbiao as c where a.html_key=c.html_key )
    """
    print(sql)
    conp=['gpadmin','since2015','192.168.4.206','biaost','public']

    db_command(sql,dbtype="postgresql",conp=['gpadmin','since2015','192.168.4.206','biaost','public'])