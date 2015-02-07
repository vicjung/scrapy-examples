from scrapy import log
from scrapy.dupefilter import RFPDupeFilter
from scrapy.utils.request import request_fingerprint
from proxy import PROXIES
from agents import AGENTS

import os
import random






class CustomHttpProxyMiddleware(object):

    def process_request(self, request, spider):
        # TODO implement complex proxy providing algorithm
        if self.use_proxy(request):
            p = random.choice(PROXIES)
            try:
                request.meta['proxy'] = "http://%s" % p['ip_port']
            except Exception, e:
                log.msg("Exception %s" % e, _level=log.CRITICAL)

    def use_proxy(self, request):
        """
        using direct download for depth <= 2
        using proxy with probability 0.3
        """
        if "depth" in request.meta and int(request.meta['depth']) <= 2:
            return False
        i = random.randint(1, 10)
        return i <= 2


class CustomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(AGENTS)
        request.headers['User-Agent'] = agent


class CustomSqliteDupeFilter(RFPDupeFilter):
"""A dupe filter that considers specific ids in the url"""

    def __getid(self, url):
        mm = url.split("&refer")[0] #or something like that
        return mm

    def request_seen(self, request):
        fp = self.__getid(request.url)
        if fp in self.fingerprints:
            return True
        self.fingerprints.add(fp)
        if self.file:
            self.file.write(fp + os.linesep)