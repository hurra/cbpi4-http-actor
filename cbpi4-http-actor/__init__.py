
# -*- coding: utf-8 -*-
import os
from aiohttp import web
import logging
from unittest.mock import MagicMock, patch
import asyncio
import random
from cbpi.api import *

import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


logger = logging.getLogger(__name__)

@parameters([
    Property.Select(label="Http Method", options=['GET','POST'], description="asdc"),
    Property.Select(label="Check Certificate", options=['YES','NO'], description="asdc"),
    Property.Number(label="Request Timeout", configurable=True, description="asd", default_value=5),
    Property.Text(label="Target URL On", configurable=True, description="anc"),
    Property.Text(label="Request Body On", configurable=True, description="asdc"),
    Property.Text(label="Target URL Off", configurable=True, description="anc"),
    Property.Text(label="Request Body Off", configurable=True, description="asdc"),
    Property.Select(label="Continous Mode", options=['YES','NO'], description="asdc"),
    Property.Number(label="Continous Interval", configurable=True, description="asd")
    ])
class HTTPActor(CBPiActor):

    @action("action test lorenz", parameters={})
    async def action(self, **kwargs):
        logger.info("Action triggered %s los" % kwargs)
        self.on()
        self.off()
        logger.info("Action triggered %s ende" % kwargs)
        pass
    
    def __init__(self, cbpi, id, props):
        super().__init__(cbpi, id, props)
        self.state = False

        self.s = requests.Session()

        if self.props.get("Check Certificate", "YES") == "YES":
            self.cert = True
        else:
            self.cert = False

        if self.props.get("Http Method", "GET") == "GET":
            self.httpmethod_get = True
        else:
            self.httpmethod_get = False

        self.timeout = float(self.props.get("Request Timeout", 5))

        pass

    def start_request(self, onoff):
        if onoff:
            url=self.props.get("Target URL On")
        else:
            url=self.props.get("Target URL Off")

        if self.httpmethod_get:
            self.s.get(url, verify=self.cert, timeout=self.timeout)
        else:
            self.s.post(url, verify=self.cert, timeout=self.timeout)


    async def on(self, power=0):
        logger.info("ACTOR 1111 %s ON" % self.id)
        logger.info("ACTOR 1111 %s ON" % self.props)
        self.start_request(True)
        self.state = True

    async def off(self):
        logger.info("ACTOR %s OFF " % self.id)
        logger.info("ACTOR %s OFF" % self.props)
        start_request(False)
        self.state = False

    def get_state(self):
        return self.state
    
    async def run(self):
        pass


def setup(cbpi):
    cbpi.plugin.register("HTTP Actor", HTTPActor)
    pass
