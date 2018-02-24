import os

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options

from tornado.options import define, options, parse_command_line
define('port', default=8888, type=int, help="run on the port")

from url import urls

if __name__ == "__main__":
    PORT = 8888
    SETTINGS = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        login_url="/login",
        cookie_secret="235lksjfASKJFlks=jdfGLKS=JDFLKSsfjlk234dsjflksdjffj/=sf"
    )
    application = tornado.web.Application(
        handlers=urls,
        **SETTINGS
    )
    parse_command_line()
    print('serve listen port %s' % options.port)
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()