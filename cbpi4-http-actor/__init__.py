
# -*- coding: utf-8 -*-
import os
from aiohttp import web
import logging
from unittest.mock import MagicMock, patch
import asyncio
import random
from cbpi.api import *

logger = logging.getLogger(__name__)



             
class CustomActor(CBPiActor):

    eins = Property.Text(label="Target URL", configurable=True, description="anc")
    zwei = Property.Select(label="Http Method", options=['GET','POST'], description="asdc")
    drei = Property.Number(label="Timeout", configurable=True, description="asd")
   

    @action("action test lorenz", parameters={})
    async def action(self, **kwargs):
        print("Action Triggered", kwargs)
        logger.info("Action triggered %s" % kwargs)
        pass
    
    def init(self):        
        self.state = False
        logging.info("eins: %s",eins)
        logging.info("zwei: %s",zwei)
        logging.info("drei: %s",drei)
        pass

    async def on(self, power=0):
        logger.info("ACTOR 1111 %s ON" % self.id)
        self.state = True

    async def off(self):
        logger.info("ACTOR %s OFF " % self.id)
        self.state = False

    def get_state(self):
        return self.state
    
    async def run(self):
        pass


def setup(cbpi):
    cbpi.plugin.register("HTTP Actor", CustomActor)
    pass
