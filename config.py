
from redis_mock import RedisMock
r = RedisMock()

token = '8564243133:AAEx8UTZKQOxtAr2jMRDkFCsjivv-aiLuiQ'
Dev_Zaid = token.split(':')[0]
sudo_id = 8087077168
botUsername = 'DarkTepbot'
from kvsqlite.sync import Client as DB
ytdb = DB('ytdb.sqlite')
sounddb = DB('sounddb.sqlite')
wsdb = DB('wsdb.sqlite')