
import tornado
import json
import store
from sqlalchemy import *
from sqlalchemy.orm import relationship, sessionmaker
from tornado.ioloop import IOLoop, PeriodicCallback

from tornado import gen

from tornado.websocket import websocket_connect

from ast import literal_eval


class Client(object):

    def __init__(self, urlb, urlg, timeout):

        self.urlb = urlb

        self.urlg = urlg

        self.timeout = timeout

        self.ioloop = IOLoop.instance()

        self.wsb = None

        self.wsg = None

        self.connect()

        PeriodicCallback(self.keep_alive, 20000).start()

        self.ioloop.start()



    @gen.coroutine

    def connect(self):

        print ("trying to connect")

        try:

            self.wsb = yield websocket_connect(self.urlb)

            self.wsg = yield websocket_connect(self.urlg)

            datab = {
                "event": "subscribe",
                "channel": "book",
                "pair": "BTCUSD",
                "prec": "P0",
                "freq": "F1"
            }

            datag = {
                "type": "subscribe",
                "channels": [{"name": "level2", "product_ids": ["BTC-USD"]}]

            }

            self.wsb.write_message(tornado.escape.utf8(json.dumps(datab)))

            self.wsg.write_message(tornado.escape.utf8(json.dumps(datag)))


            engine = create_engine('mysql://root:12345@localhost:3306/test')
            connection = engine.connect()
            Session = sessionmaker(bind=engine)
            session = Session()

        except (Exception):

            print ("connection error")
            print(Exception.__getattribute__())

        else:

            print ("connected")

            self.run(session,connection)



    @gen.coroutine

    def run(self,session,connection):

        while True:
            msgB = yield self.wsb.read_message()
            print("msgB:: " + msgB)
            if(msgB.startswith('[') and msgB.endswith(']')):
                msglist = literal_eval(msgB)
                if(len(msglist)==2 and type(msglist)=='list'):
                    for index in range(1,len(msglist[1])):
                        f = msglist[1]
                        if f[index][1] != 0:
                            if f[index][2] < 0:
                                f[index].insert(0, "Ask")
                            else:
                                f[index].insert(0, "Bid")
                            f[index].append("Bitfinex")
                            store.Main.run(session, f[index])

                if len(msglist) == 4 and msglist[2] != 0:
                    f = msglist
                    if f[3] < 0:
                        f.insert(1, "Ask")
                    else:
                        f.insert(1, "Bid")
                    f[index].append("Bitfinex")
                    store.Main.run(session, f[1:5])
            #connection.close()



            msgG = yield self.wsg.read_message()
            print("msgG:: " + msgG)
            msgdax = literal_eval(msgG)
            if msgdax["type"] == "snapshot":
                blist = msgdax["bids"]
                for index in range(1, len(blist)):
                    blist[index].insert(1, 1)
                    blist[index].insert(0, "Bid")
                    blist[index].append("GDAX")
                    store.Main.run(session, blist[index])
                alist = msgdax["asks"]
                for index in range(1, len(alist)):
                    alist[index].insert(1, 1)
                    alist[index].insert(0, "Ask")
                    alist[index].append("GDAX")
                    store.Main.run(session, alist[index])
            if msgdax["type"] == "l2update":
                mlist = msgdax["changes"][0]
                if mlist[0] == "sell":
                    mlist[0] = "Ask"
                if mlist[0] == "buy":
                    mlist[0] = "Bid"
                mlist.insert(2, 1)
                mlist.append("GDAX")
                store.Main.run(session, mlist)


            if msgB is None:

                print ("Bitfinex connection closed")

                self.wsb = None

                break

            if msgG is None:

                print("Gdax connection closed")

                self.wsb = None

                break



    def keep_alive(self):

        if self.wsb or self.wsg is None:

            self.connect()

        else:

            print("*still connected*")



if __name__ == "__main__":

    client = Client("wss://api.bitfinex.com/ws", "wss://ws-feed.gdax.com", 5)
