
# -*- coding: utf-8 -*-
import os
from aiohttp import web
import logging
from unittest.mock import MagicMock, patch
import asyncio
import random
from cbpi.api import *

import requests
import time


logger = logging.getLogger(__name__)

@parameters([
    Property.Select(label="Http Method", options=['GET','POST'], description="asdc"),
    Property.Select(label="Check Certificate", options=['YES','NO'], description="asdc"),
    Property.Number(label="Request Timeout", configurable=True, description="asd", default_value=5),
    Property.Text(label="Target URL On", configurable=True, description="anc"),
    Property.Text(label="Request Body On", configurable=True, description="asdc"),
    Property.Text(label="Target URL Off", configurable=True, description="anc"),
    Property.Text(label="Request Body Off", configurable=True, description="asdc"),
    Property.Select(label="Check Return Status Code", options=['YES','NO'], description="asdc"),
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
            self.s.verify = True
        else:
            self.s.verify = False

        if self.props.get("Http Method", "GET") == "GET":
            self.httpmethod_get = True
        else:
            self.httpmethod_get = False

        if self.props.get("Check Return Status Code", "NO") == "YES":
            self.check_statuscode = True
        else:
            self.check_statuscode = False            

        if self.props.get("Continous Mode", "NO") == "YES":
            self.continous_mode = True
        else:
            self.continous_mode = False

        self.continous_interval = float(self.props.get("Continous Interval", 5))


        self.s.timeout = float(self.props.get("Request Timeout", 5))


        if self.continous_mode:
            self._task = asyncio.create_task(self.set_continous_state())

        pass

    async def set_continous_state(self):
        logger.info('Starting Continous State Setter background task')
        while True:
            start_time = int(time.time())
            try:
                self.start_request(self.state)
            except Exception as e:
                logger.error("Irgendeine Exception is aufgetreten: %s" % e)
            
            wait_time = start_time + self.continous_interval - int(time.time())
            logger.info("Warte %s Zeit" % wait_time)
            if wait_time < 0:
                logger.warn("Continous Interval kann nicht gehalten werden, da zu klein und requests brauchen zu lange")
            else:
                await asyncio.sleep(wait_time)

        pass

    def start_request(self, onoff):
        logger.info("HTTPActor request onoff=%s start" % onoff)
        if onoff:
            url=self.props.get("Target URL On")
        else:
            url=self.props.get("Target URL Off")

        if self.httpmethod_get:
            repsonse = self.s.get(url)
        else:
            response = self.s.post(url)

        if self.check_statuscode:
            if response.status_code != 200:
                raise Exception("Received Statuscode %s is not 200" % (response.status_code))

        logger.info("HTTPActor request onoff=%s end" % onoff)


    async def on(self, power=0):
        logger.info("Actor %s ON" % self.id)
        self.state = True
        self.start_request(True)

    async def off(self):
        logger.info("Actor %s OFF" % self.id)
        self.state = False
        self.start_request(False)

    def get_state(self):
        return self.state
    
    async def run(self):
        pass


def setup(cbpi):
    cbpi.plugin.register("HTTP Actor", HTTPActor)
    pass
