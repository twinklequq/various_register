# -*- coding: utf-8 -*-


import mitmproxy.http
from mitmproxy import ctx


num = 0


class Counter:
    def __init__(self):
        self.num = 0

    def request(self, flow: mitmproxy.http.HTTPFlow):
        self.num = self.num + 1
        ctx.log.info("We've seen %d flows" % self.num)


class Joker:
    def request(self, flow: mitmproxy.http.HTTPFlow):
        if flow.request.host != "www.baidu.com" or not flow.request.path.startswith('/s'):
            return
        if "wd" not in flow.request.query.keys():
            ctx.log.warn("can not get search word from %s" % flow.request.pretty_url)
            return
        ctx.log.info("cannot get search word from %s" % flow.request.query.get('wd'))
        flow.request.query.set_all("wd", ["可爱"])

    # def response(self, flow: mitmproxy.http.HTTPFlow):

addons = [
    # Counter(),
    Joker(),
]