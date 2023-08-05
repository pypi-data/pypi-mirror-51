from zlsrc.zlsys.src import src_update,src_update_dates
from zlsrc.zlsys.t_gg import t_gg_update,est_func
from datetime import datetime,timedelta
from lmf.dbv2 import db_command
import json 

conp_=['postgres','since2015','192.168.4.201','zlsys']

settings={
    "zlsys_yunnan_qujingshi":[['曲靖市','zfcg','yunnan_qujingshi','云南曲靖市','2019-06-27'],
            ['曲靖市','gcjs','yunnan_qujingshi','云南曲靖市','2019-06-27']]
    ,
    "zlsys_yunnan_dalizhou":[['大理州','zfcg','yunnan_dalizhou','云南大理州','2019-07-03'],
            ['大理州','gcjs','yunnan_dalizhou','云南大理州','2019-07-03']]
    ,

    "zlsys_yunnan_lincangshi":[['临沧市','zfcg','yunnan_lincangshi','云南临沧市','2019-07-03'],
            ['临沧市','gcjs','yunnan_lincangshi','云南临沧市','2019-07-03']]
    ,

    "zlsys_yunnan_wenshanzhou":[['文山州','zfcg','yunnan_wenshanzhou','云南文山州','2019-07-03'],
            ['文山州','gcjs','yunnan_wenshanzhou','云南文山州','2019-07-03']]
    ,
    "zlsys_yunnan_yuxishi":[['玉溪市','zfcg','yunnan_yuxishi','云南玉溪市','2019-07-03'],
            ['玉溪市','gcjs','yunnan_yuxishi','云南玉溪市','2019-07-03']]
    ,
    "zlsys_yunnan_xishuangbanna":[['西双版纳州','zfcg','yunnan_xishuangbanna','云南西双版纳州','2019-07-03'],
            ['西双版纳州','gcjs','yunnan_xishuangbanna','云南西双版纳州','2019-07-03']]
    ,
    "zlsys_yunnan_zhaotongshi":[['昭通市','zfcg','yunnan_zhaotongshi','云南昭通市','2019-07-03'],
            ['昭通市','gcjs','yunnan_zhaotongshi','云南昭通市','2019-07-03']]

    ,
    "zlsys_yunnan_dehongzhou":[['德宏州','zfcg','yunnan_dehongzhou','云南德宏州','2019-07-03'],
            ['德宏州','gcjs','yunnan_dehongzhou','云南德宏州','2019-07-03']]
    ,
    "zlsys_yunnan_diqingzhou":[['迪庆州','zfcg','yunnan_diqingzhou','云南迪庆州','2019-07-03'],
            ['迪庆州','gcjs','yunnan_diqingzhou','云南迪庆州','2019-07-03']]

    ,
    "zlsys_yunnan_puershi":[['普洱市','zfcg','yunnan_puershi','云南普洱市','2019-07-03'],
            ['普洱市','gcjs','yunnan_puershi','云南普洱市','2019-07-03']]

    ,
    "zlsys_yunnan_baoshanshi":[['保山市','zfcg','yunnan_baoshanshi','云南保山市','2019-07-03'],
            ['保山市','gcjs','yunnan_baoshanshi','云南保山市','2019-07-03']]

    ,
    "zlsys_yunnan_lijiangshi":[['丽江市','zfcg','yunnan_lijiangshi','云南丽江市','2019-07-03'],
            ['丽江市','gcjs','yunnan_lijiangshi','云南丽江市','2019-07-03']],

    "zlsys_yunnan_yunnansheng":[['云南省','zfcg','yunnan_yunnansheng','云南省本级','2019-07-03'],
            ['云南省','gcjs','yunnan_yunnansheng','云南省本级','2019-07-03']],



    "zlsys_yunnan_chuxiongzhou":[['楚雄州','zfcg','yunnan_chuxiongzhou','云南省楚雄州','2019-07-03'],
            ['楚雄州','gcjs','yunnan_chuxiongzhou','云南省楚雄州','2019-07-03']],



    "zlsys_yunnan_honghezhou":[['红河州','zfcg','yunnan_honghezhou','云南省红河州','2019-07-03'],
            ['红河州','gcjs','yunnan_honghezhou','云南省红河州','2019-07-03']],


    "zlsys_yunnan_nujiangzhou":[['深圳市','zfcg','yunnan_nujiangzhou','云南省怒江州','2019-07-03'],
            ['云南省','gcjs','yunnan_nujiangzhou','云南省本级','2019-07-03']],



    "zlsys_yunnan_tengchongshi":[['腾冲市','zfcg','yunnan_tengchongshi','云南腾冲市','2019-07-02'],
            ['腾冲市','gcjs','yunnan_tengchongshi','云南腾冲市','2019-07-02']],

    "zlsys_yunnan_kunmingshi":[['昆明市','zfcg','yunnan_kunmingshi','云南省昆明市','2019-07-02'],
            ['昆明市','gcjs','yunnan_kunmingshi','云南省昆明市','2019-07-02']],

    "zlsys_guangdongsheng_shenzhenshi":[
            ['深圳市','gcjs','guangdongsheng_shenzhenshi','广东省深圳市','2019-06-21']],







    "zlsys_sichuan_yaanshi":[['雅安市','zfcg','sichuan_yaanshi','四川雅安市','2019-06-28'],
            ['雅安市','gcjs','sichuan_yaanshi','四川雅安市','2019-06-28']],


    "zlsys_sichuan_suiningshi":[['遂宁市','zfcg','sichuan_suiningshi','四川遂宁市','2019-06-28'],
            ['遂宁市','gcjs','sichuan_suiningshi','四川遂宁市','2019-06-28']],


    "zlsys_sichuan_yibinshi":[['宜宾市','zfcg','sichuan_yibinshi','四川宜宾市','2019-06-30'],
            ['宜宾市','gcjs','sichuan_yibinshi','四川宜宾市','2019-06-30']],



}



def task(quyu,conp,tag=None):
    sts=settings[quyu]
    for st in sts:
        conp=[*conp_,st[2]]

        if tag is None:
            bdate=st[4]
        else:
            bdate=datetime.strftime(datetime.now()+timedelta(days=-2),'%Y-%m-%d')

        src_update_dates(st[0],st[1],conp,bdate)
        print("t_gg_update")
        t_gg_update(conp,'zlsys_%s'%st[2],st[3])

def restart_quyu(quyu,conp):
    db,schema=quyu.split("_")[0],'_'.join(quyu.split("_")[1:])
    conp=[*conp_,schema]
    sql="drop schema if exists %s cascade;create schema if not exists %s"%(schema,schema)

    db_command(sql,dbtype="postgresql",conp=[*conp_,'public'])
    task(quyu)

def create_func():
    est_func(conp_)


def restart_all():
    arr=settings.keys()
    arr.sort()
    for quyu in arr:

        restart_quyu(quyu)
# restart_quyu('zlsys_yunnan_diqingzhou')



def work(conpx,**krg):
    para={"info":None}
    para.update(krg)

    info=para['info']
    schema=conpx[4]
    quyu=schema
    sts=settings[quyu]
    for st in sts:
        conp=conpx

        if info is None:
            bdate=st[4]
        else:
            bdate=datetime.strftime(datetime.now()+timedelta(days=-2),'%Y-%m-%d')

        src_update_dates(st[0],st[1],conp,bdate)
        print("t_gg_update")
        t_gg_update(conp,st[2],st[3])



def task_conp_cfg(quyu,cfg,conpx,tag=None):
    cfg=json.loads(cfg)
    sts=cfg[quyu]
    for st in sts:
        conp=[*conpx,st[2]]

        if tag is None:
            bdate=st[4]
        else:
            bdate=datetime.strftime(datetime.now()+timedelta(days=-2),'%Y-%m-%d')

        src_update_dates(st[0],st[1],conp,bdate)
        print("t_gg_update")
        t_gg_update(conp,'zlsys_%s'%st[2],st[3])