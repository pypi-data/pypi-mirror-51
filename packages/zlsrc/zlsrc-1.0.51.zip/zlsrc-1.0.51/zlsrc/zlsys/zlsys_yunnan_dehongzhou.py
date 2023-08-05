from zlsrc.zlsys.src import src_update,src_update_dates
from zlsrc.zlsys.t_gg import t_gg_update,est_func
from datetime import datetime,timedelta
from lmf.dbv2 import db_command,db_query
import json 

data=[['德宏州','zfcg','zlsys_yunnan_dehongzhou','云南德宏州','2019-08-20'],
            ['德宏州','gcjs','zlsys_yunnan_dehongzhou','云南德宏州','2019-08-20']]



def work(conp,**krg):
    info=krg['info']
    para={
    "zfcg_bdate":None,"gcjs_bdate":None
    }
    if info is not None:
        info=json.loads(info)
        para.update(info)

    zfcg_bdate=para['zfcg_bdate']
    gcjs_bdate=para['gcjs_bdate']

    quyu=conp[4]
    schemas=db_query(""" SELECT nspname FROM  pg_namespace """,dbtype="postgresql",conp=conp)['nspname'].values.tolist()
    if  quyu not in schemas:  db_command("""create schema if not exists %s """%quyu,dbtype="postgresql",conp=conp)


    tables=db_query("""SELECT tablename FROM  pg_tables where schemaname='%s' """%quyu,dbtype="postgresql",conp=conp)['tablename'].values.tolist()

    if 't_gg' not in tables:tag=None
    else:tag='cdc'

    for st in data:
        if tag is None:
            jytype=st[1]
            if jytype=='zfcg':
                bdate=st[4] if zfcg_bdate is  None else zfcg_bdate
            else:
                bdate=st[4] if gcjs_bdate is  None else gcjs_bdate
            print(bdate)
        else:
            bdate=datetime.strftime(datetime.now()+timedelta(days=-2),'%Y-%m-%d')

        src_update_dates(st[0],st[1],conp,bdate)
        print("t_gg_update")
        t_gg_update(conp,st[2],st[3])

# conp=['postgres','since2015','192.168.4.201','zlsys','zlsys_yunnan_dalizhou']

# work(conp,info=None)