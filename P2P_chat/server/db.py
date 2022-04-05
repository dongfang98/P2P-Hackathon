from pymysql import *
from config import *
#python connect to db
class DB(object):
    def __init__(self):
        print('DB connected')
        self.conn=connect(host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASS,database=DB_NAME)
    #get cursor

        self.cursor = self.conn.cursor()
    def close(self):

        #release the resource

        self.cursor.close()
        self.conn.close()

    def get_one(self,sql):
        #use sql to query the information

        print(sql)
        self.cursor.execute(sql)
        print('cursor obtained')
        #get the result
        #We can get the result of each columu but cannot get the header

        query_result=self.cursor.fetchone()
        print(query_result,'query')

        #Check whether we find it successfully

        if not query_result:
            print('none')
            return None
        #get header
        #use self.cursor.description to return a list, each element in the list is another list
        #get each elemnet in junior list and build a new list ['user_id','user_name','user_nickname']

        fileds =[filed[0] for filed in self.cursor.description]
        return_data={}
        #wrappe the result and list to a dictionary

        for filed, value in zip(fileds, query_result):
            return_data[filed] = value
        print(return_data,'return_data')
        return return_data
if __name__ =='__main__':
    db=DB()
    data=db.get_one("select * from users WHERE user_name='user2'")
    print(data)
    db.close()