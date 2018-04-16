import logging
import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.options
import simplejson
import sqlalchemy
import collections

from tornado.options import define, options

define("port", default=3000, help="run on the given port", type=int)
engine = sqlalchemy.create_engine('mysql://root:12345@localhost:3306/test')


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET,PUT,POST")
        self.set_header("Access-Control-Allow-Headers",
                        "Content-Type, Depth, User-Agent, X-File-Size, X-Requested-With, X-Requested-By,If-Modified-Since, X-File-Name,Cache-Control")

class queryHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self, *args):
        snapshotHandler()

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", RealtimeHandler),
                    (r"/snapshot", snapshotHandler),
                    (r"/", queryHandler)]
        settings = dict(debug=True)
        tornado.web.Application.__init__(self, handlers, **settings)

# MainHandler to handle realtime orders
class RealtimeHandler(BaseHandler):
    num = 0;
    @tornado.web.asynchronous
    def get(self, *args):
        connection = engine.connect()
        bid = connection.execute("SELECT * FROM orderbook WHERE typ = 'Bid' ORDER BY id DESC LIMIT 20")
        ask = connection.execute("SELECT * FROM orderbook WHERE typ = 'Ask' ORDER BY id DESC LIMIT 20")

        bid_msg = []
        ask_msg = []
        msg = []
        msg.append(createDict(bid,bid_msg,"Ask"))
        msg.append(createDict(ask,ask_msg, "Bid"))
        print(msg)

        self.write(simplejson.dumps(msg))
        self.flush()
        self.finish()
        connection.close()

class snapshotHandler(BaseHandler):

    @tornado.web.asynchronous
    def get(self, *args):
        connection = engine.connect()
        condition = ""
        price = "0"
        try:
            price = self.get_argument("price")
        except:
            print("No price value")

        try:
            exchange = self.get_argument("exchange")

            if (exchange == "Both"):
                condition = ""
            else:
                condition = "AND xchange = '" + exchange + "'"

        except:
            print("No exchange value")


        ask = connection.execute(
            "SELECT * FROM orderbook WHERE typ = 'Ask' AND price > " + price + " " + condition + " ORDER BY id DESC LIMIT 20 ")
        bid = connection.execute(
            "SELECT * FROM orderbook WHERE typ = 'Bid' AND price > " + price + " " + condition + " ORDER BY id DESC LIMIT 20 ")

        bid_msg = []
        ask_msg = []
        msg = []
        msg.append(createDict(bid,bid_msg,"Ask"))
        msg.append(createDict(ask,ask_msg, "Bid"))
        print(msg)

        self.write(simplejson.dumps(msg))
        self.flush()
        self.finish()
        connection.close()


def createDict(rows, list, str):
    for element in rows:
        d = {
            'type' : str,
            'price' : element.price,
            'amount' : element.amount,
            'count' : element.count,
            'exchange' : element.xchange
        }
        list.append(d)

    return list



def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()



if __name__ == "__main__":
    main()