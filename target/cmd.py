import tornado.ioloop
import tornado.httpserver
import tornado.web
import argparse
import numpy as np
import gc


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class CpuHandler(tornado.web.RequestHandler):
    def get(self):
        x, y = np.ogrid[-2:1:100j, -1.5:1.5:100j]

        # Increase this to improve the shape of the fractal
        iterations = 3

        c = x + 1j*y

        z = reduce(lambda x, y: x**2 + c, [1] * iterations, c)
        self.write(",".join(str(num) for num in np.angle(z)))


class MemoryHandler(tornado.web.RequestHandler):
    data = []

    def get(self):
        self.data.append(1)


class DiskHandler(tornado.web.RequestHandler):
    data = []

    def get(self):
        with open("test.tmp", "w") as f:
            f.write("Hello world!\n")


class SleepHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        yield tornado.gen.sleep(np.random.lognormal(mean=-1.63, sigma=0.7))


class SleepyHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        if np.random.rand() < 0.99:
            yield tornado.gen.sleep(
                np.random.lognormal(mean=-1.63, sigma=0.7))
        else:
            yield tornado.gen.sleep(
                np.random.lognormal(mean=1, sigma=0.25))


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/cpu", CpuHandler),
        (r"/mem", MemoryHandler),
        (r"/disk", DiskHandler),
        (r"/sleep", SleepHandler),
        (r"/1", MainHandler),
        (r"/2", CpuHandler),
        (r"/3", MemoryHandler),
        (r"/4", DiskHandler),
        (r"/5", SleepHandler),
        (r"/5star", SleepyHandler),
    ])


def main():
    parser = argparse.ArgumentParser(description='Target stub.')
    parser.add_argument('--port', dest='port', type=int, default=8888, help='target port')
    parser.add_argument('--workers', dest='workers', type=int, default=1, help='number of workers')
    parser.add_argument('--loggc', dest='loggc', action='store_true', help='log gc stats')
    args = parser.parse_args()
    if args.loggc:
        gc.set_debug(gc.DEBUG_STATS | gc.DEBUG_COLLECTABLE)
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.bind(args.port)

    server.start(args.workers)

    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
