import socks
import socket
import logging
import requests



logger = logging.getLogger(__name__)


class Scrapper(object):
    def __init__(self, skip_objects=None):
        self.skip_objects = skip_objects

    def scrap_process(self, url, storage = None):
        #for tor service
        socks.set_default_proxy(socks.SOCKS5, "localhost", 9050)
        socket.socket = socks.socksocket
        # You can iterate over ids, or get list of objects
        # from any API, or iterate throught pages of any site
        # Do not forget to skip already gathered data
        # Here is an example for you
        #url = 'https://otus.ru/'

        response = requests.get(url)

        if not response.ok:
            logger.error(response.text)
            # then continue process, or retry, or fix your code
            return None
        else:
            # Note: here json can be used as response.json
            #data = response.text
            # save scrapped objects here
            # you can save url to identify already scrapped objects
            #storage.write_data([url + '\t' + data.replace('\n', '')])

            #scrapped objects is very large

            return response
