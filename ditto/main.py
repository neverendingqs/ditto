from ditto import app, clone
import argparse
import sys
from gevent.wsgi import WSGIServer


class Ditto(object):

    def __init__(self):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest='command')

        transform = subparsers.add_parser('clone')
        transform.add_argument('--source', type=str, default='http://localhost/')
        transform.add_argument('--destination', type=str, default='./data')

        serve = subparsers.add_parser('serve')
        serve.add_argument('--port', type=int, default=80)
        serve.add_argument('--source', type=str, default='./data')

        args = parser.parse_args(sys.argv[1:])
        if args.command is None:
            parser.print_help()
            exit(1)
        getattr(self, args.command)(args)

    @staticmethod
    def clone(args):
        clone.do_clone(args.source, args.destination)

    @staticmethod
    def serve(args):
        print('serving on port %d from source %s' % (args.port, args.source))
        WSGIServer(('', args.port), app.build(args.source)).serve_forever()
