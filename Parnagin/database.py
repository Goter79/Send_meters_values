# import psycopg2
# from psycopg2 import sql
# from psycopg2._psycopg import AsIs

import sqlite3 as sl

class Database:
    def __init__(self):
        # self.conn = psycopg2.connect(database='MyDataBase', user='MyUser',
        #                              password='SECRET', host='MeServ', port=5432)
        # self.cursor = self.conn.cursor()
        self.con = sl.connect('reports.db',check_same_thread=False)
        self.cursor = self.con.cursor()


    def listColledjeForPage(self, tables='Meter_Measure', Page=1, id_meter='', wheres=''):
        if id_meter=='' :
            sql="SELECT 0 r, 1 rn, id_meter, LS, Service, Number, value, value_old, LastUpdate, id_user" \
                "   FROM "+tables+" "+wheres+" order by LS, Service, id_meter limit 2"
        else:
            # self.cursor.execute(sql)
            #sql="select * from "+tables+" "+wheres
            sql="""with t as (Select  ROW_NUMBER() over (order by LS, Service, id_meter) rn, * 
                                from """+tables+""" """+wheres+""" )
                    SELECT ts.rn-t1.rn as r, ts.rn, ts.id_meter, ts.LS, ts.Service, ts.Number, ts.value, ts.value_old, ts.LastUpdate, ts.id_user
                        from t ts 
                        cross join t t1 on t1.id_meter="""+id_meter+"""
                       Where ts.rn-t1.rn BETWEEN -1 and 1 """
        # print(sql)
      
        self.cursor.execute(sql)
        res = self.cursor.fetchall()

        sql="select count(*) from "+tables+" "+wheres
        self.cursor.execute(sql)
        count = self.cursor.fetchone()[0]
        
        return res, len(res), count