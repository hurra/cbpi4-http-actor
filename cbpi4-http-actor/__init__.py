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
    Property.Select(label="Http Method", options=['GET','POST'], description="HTTP method to use"),
    Property.Select(label="Check Certificate", options=['YES','NO'], description="Enable or disable TLS certificate checking. This setting has no influence for unencrypted connections"),
    Property.Number(label="Request Timeout", configurable=True, description="http request timeout in seconds (default 5)", default_value=5),
    Property.Text(label="Target URL On", configurable=True, description="target url for state on. Must include a uri scheme (https://...)"),
    Property.Text(label="Request Body On", configurable=True, description="This request body is passed in the corresponding on request"),
    Property.Text(label="Target URL Off", configurable=True, description="target url for state off. Must include a uri scheme (https://...)"),
    Property.Text(label="Request Body Off", configurable=True, description="This request body is passed in the corresponding off request"),
    Property.Select(label="Continous Mode", options=['YES','NO'], description="Enable this if the remote url should be refreshed periodically even if our local actor state hasn't changed"),
    Property.Number(label="Continous Interval", configurable=True, description="Refresh interval in seconds used in continous mode")
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
        self.continous_task = None

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

        pass


    async def set_continous_state(self):
        logger.info('Starting continous state setter background task interval=%s'% (self.continous_interval))
        while True:
            start_time = int(time.time())
            try:
                await self.start_request(self.state)
            except Exception as e:
                logger.error("Unknown exception: %s" % e)
            
            wait_time = start_time + self.continous_interval - int(time.time())
            if wait_time < 0:
                logger.warn("Continous interval kann nicht gehalten werden, da zu klein und requests brauchen zu lange")
            else:
                await asyncio.sleep(wait_time)

        pass

    async def start_request(self, onoff):
        if onoff:
            url = self.url_on
            payload = self.payload_on
        else:
            url = self.url_off
            payload = self.payload_off

        if payload is not None:
            payload_logtext=payload.replace('"', '\\"')
        else:
            payload_logtext="[not_set]"

        logger.info("HTTPActor type=request_start onoff=%s url=\"%s\" payload=\"%s\" method_getpost=%s" % (onoff, url, payload_logtext, self.httpmethod_get))
        if self.httpmethod_get:
            response = self.request_session.get(url, data=payload)
        else:
            response = self.request_session.post(url, data=payload)

        logger.info("HTTPActor type=request_done onoff=%s url=\"%s\" http_statuscode=%s response_text=\"%s\"" % (onoff, url, response.status_code, response.text.replace('"', '\\"')))


    async def on(self, power=0):
        logger.debug("Actor %s ON" % self.id)
        self.state = True
        await self.start_request(True)

    async def off(self):
        logger.debug("Actor %s OFF" % self.id)
        self.state = False
        await self.start_request(False)

    def get_state(self):
        return self.state

    async def start(self):
        pass

    async def stop(self):
        if self.continous_task is not None:
            self.continous_task.cancel()

        pass

    async def on_start(self):
        pass

    async def on_stop(self):
        pass

    
    async def run(self):
        if self.continous_mode:
            self.continous_task = asyncio.create_task(self.set_continous_state())
        pass


def setup(cbpi):
    cbpi.plugin.register("HTTP Actor", HTTPActor)
    pass
