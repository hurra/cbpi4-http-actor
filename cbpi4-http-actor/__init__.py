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
    Property.Select(label="Continous Mode", options=['YES','NO'], description="asdc"),
    Property.Number(label="Continous Interval", configurable=True, description="asd")
    ])
class HTTPActor(CBPiActor):

    @action("Toggle on off once with 5 second pause", parameters={})
    async def action(self, **kwargs):
        logger.info("Action triggered %s los" % kwargs)
        self.on()
        await asyncio.sleep(5)
        self.off()
        logger.info("Action triggered %s ende" % kwargs)
        pass
    
    def __init__(self, cbpi, id, props):
        super().__init__(cbpi, id, props)
        self.state = False

        self.request_session = requests.Session()

        if self.props.get("Check Certificate", "YES") == "YES":
            self.request_session.verify = True
        else:
            self.request_session.verify = False

        if self.props.get("Http Method", "GET") == "GET":
            self.httpmethod_get = True
        else:
            self.httpmethod_get = False
    
        if self.props.get("Continous Mode", "NO") == "YES":
            self.continous_mode = True
        else:
            self.continous_mode = False
            
        self.url_on = self.props.get("Target URL On")
        self.url_off = self.props.get("Target URL Off")

        self.payload_on = self.props.get("Request Body On")
        self.payload_off = self.props.get("Request Body Off")

        self.continous_interval = float(self.props.get("Continous Interval", 5))


        self.request_session.timeout = float(self.props.get("Request Timeout", 5))


        if self.continous_mode:
            self.continous_task = asyncio.create_task(self.set_continous_state())
        else:
            #TODO: irgendwie checkt er nicht, dass schon ein task exisitert
            self.continous_task.cancel()


        logger.info("Continous Mode: %s" % self.continous_mode)

        pass


    async def set_continous_state(self):
        logger.info('Starting continous state setter background task')
        while True:
            start_time = int(time.time())
            try:
                self.start_request(self.state)
            except Exception as e:
                logger.error("Unknown exception: %s" % e)
            
            wait_time = start_time + self.continous_interval - int(time.time())
            if wait_time < 0:
                logger.warn("Continous interval kann nicht gehalten werden, da zu klein und requests brauchen zu lange")
            else:
                await asyncio.sleep(wait_time)

        pass

    def start_request(self, onoff):
        if onoff:
            url = self.url_on
            payload = self.payload_on
        else:
            url = self.url_off
            payload = self.payload_off

        logger.info("HTTPActor type=request_start onoff=%s url=\"%s\" payload=\"%s\"" % (onoff, url, payload))
        if self.httpmethod_get:
            repsonse = self.request_session.get(url)
        else:
            response = self.request_session.post(url, data=payload)

        logger.info("HTTPActor type=request_done onoff=%s url=\"%s\" http_statuscode=%s response_text=\"%s\"" % (onoff, url, response.status_code, response.text))


    async def on(self, power=0):
        logger.debug("Actor %s ON" % self.id)
        self.state = True
        self.start_request(True)

    async def off(self):
        logger.debug("Actor %s OFF" % self.id)
        self.state = False
        self.start_request(False)

    def get_state(self):
        return self.state
    
    async def run(self):
        pass


def setup(cbpi):
    cbpi.plugin.register("HTTP Actor", HTTPActor)
    pass
