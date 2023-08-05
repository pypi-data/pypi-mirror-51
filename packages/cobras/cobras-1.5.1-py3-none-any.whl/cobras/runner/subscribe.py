'''Subscribe to a channel

Copyright (c) 2018-2019 Machine Zone, Inc. All rights reserved.
'''

import logging
import asyncio
import json
from typing import Dict

import click
import uvloop

from cobras.client.client import subscribeClient
from cobras.client.credentials import (createCredentials, getDefaultRoleForApp,
                                       getDefaultSecretForApp)
from cobras.common.apps_config import PUBSUB_APPKEY
from cobras.common.superuser import preventRootUsage
from cobras.common.throttle import Throttle

DEFAULT_URL = f'ws://127.0.0.1:8765/v2?appkey={PUBSUB_APPKEY}'


class MessageHandlerClass:
    def __init__(self, websockets, args):
        self.cnt = 0
        self.cntPerSec = 0
        self.throttle = Throttle(seconds=1)

    async def on_init(self):
        pass

    async def handleMsg(self, message: Dict, position: str) -> bool:
        self.cnt += 1
        self.cntPerSec += 1

        logging.info(f'{message} at position {position}')

        if self.throttle.exceedRate():
            return True

        print(f"#messages {self.cnt} msg/s {self.cntPerSec}")
        self.cntPerSec = 0

        return True


@click.command()
@click.option('--url', default=DEFAULT_URL)
@click.option('--role', default=getDefaultRoleForApp('pubsub'))
@click.option('--secret', default=getDefaultSecretForApp('pubsub'))
@click.option('--channel', default='sms_republished_v1_neo')
@click.option('--position')
@click.option('--stream_sql')
def subscribe(url, role, secret, channel, position, stream_sql):
    '''Subscribe to a channel
    '''

    preventRootUsage()
    uvloop.install()

    credentials = createCredentials(role, secret)

    asyncio.get_event_loop().run_until_complete(
        subscribeClient(url, credentials, channel, position, stream_sql,
                        MessageHandlerClass, {}))
