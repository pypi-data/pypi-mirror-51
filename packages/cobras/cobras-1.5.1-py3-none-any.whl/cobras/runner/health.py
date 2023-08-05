'''Health check.

Copyright (c) 2018-2019 Machine Zone, Inc. All rights reserved.

Subscribe to a channel, publish and make sure a message is received
'''
import sys
import urllib.request

import click
import uvloop

from cobras.client.credentials import (getDefaultRoleForApp,
                                       getDefaultSecretForApp)
from cobras.client.health_check import (getDefaultHealthCheckChannel,
                                        getDefaultHealthCheckHttpUrl,
                                        getDefaultHealthCheckUrl, healthCheck)
from cobras.common.superuser import preventRootUsage


@click.option('--url', default=getDefaultHealthCheckUrl())
@click.option('--http_url', default=getDefaultHealthCheckHttpUrl)
@click.option('--http', is_flag=True)
@click.option('--role', default=getDefaultRoleForApp('health'))
@click.option('--secret', default=getDefaultSecretForApp('health'))
@click.option('--channel', default=getDefaultHealthCheckChannel())
@click.option('--retry', is_flag=True)
@click.command()
def health(url, http_url, http, role, secret, channel, retry):
    '''Health check

    \b
    cobra health --http
    \b
    cobra health --http --http_url 'http://127.0.0.1:8765/health/'
    \b
    '''
    preventRootUsage()
    uvloop.install()

    if http:
        print('url:', http_url)
        with urllib.request.urlopen(http_url) as response:
            html = response.read()
            print(html.decode('utf8'), end='')
    else:
        try:
            healthCheck(url, role, secret, channel, retry)
        except ValueError as e:
            click.secho(f'System is unhealthy !!: {e}', fg='red')
            sys.exit(1)

    click.secho('System is healthy', fg='green')
