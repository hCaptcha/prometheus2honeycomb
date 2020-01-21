#!/usr/bin/env python
"""
This tool sends prometheus metrics to honeycomb given a certain prometheus URL to pull metrics from

If requested, it will send the data to honeycomb given a honeycomb write key.  Alternately, it can be
run locally and the output printed to screen instead of shipped to honeycomb.

See the CLI arguments for more details:

python3 prometheus2honeycomb.py --help

"""

import logging
import os
import sys
import beeline
import math
import subprocess
import json

from collections import defaultdict

LOG = logging.getLogger('redismetrics')

DATASET_NAME = os.getenv("DATASET_NAME", "redis")
HONEY_WRITEKEY = os.getenv("HONEYCOMB_WRITEKEY")
HONEY_DEBUG_ENABLED = 'true' in os.getenv("HONEY_DEBUG_ENABLED",
                                          'false').lower()

# assumes this binary is on the system path
PROM2JSON_BINARY = 'prom2json'


def parse_prometheus_content(lines_list):
    """
    expects to be fed prometheus metrics in a list of lines, a sample per line.

    Given the way that honeycomb and prometheus handles data differently, we break
    apart and group all metrics by their labels, and then append the labels into
    the collection of metric name/value entries
    """
    # pipe results to prom2json and parse the json result data
    proc = subprocess.Popen(PROM2JSON_BINARY,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)

    proc.stdin.write(bytes('\n'.join(lines_list), 'utf-8'))
    proc.stdin.flush()
    try:
        outs, errs = proc.communicate(timeout=.5)
        results = json.loads(outs)
    except TimeoutError:
        proc.kill()
        _, errs = proc.communicate()
        raise TimeoutError(f'prom2json failed: {errs}')

    # group by on labels to get metrics in a consumable format (each label collection collects related entries)
    ret = defaultdict(dict)
    labels_key = defaultdict(list)

    for entry in results:
        for metric in entry.get('metrics', []):
            labels = metric.get('labels', {})
            hsh = hash(frozenset(labels.items()))
            labels_key[hsh] = labels

            if entry.get('type') == 'GAUGE':
                ret[hsh].update({
                    entry['name']: metric['value'],
                    'type': entry['type']
                })
            # TODO: need to handle other types: 'SUMMARY'

    # add the label key/values back into each entry we'll send to honeycomb
    for hsh in ret.keys():
        ret[hsh].update(labels_key[hsh])

    return list(ret.values())


def honeycomb_send(data):
    """
    ships a list or a dict of data to honeycomb
    """
    beeline.init(writekey=HONEY_WRITEKEY,
                 dataset=DATASET_NAME,
                 debug=HONEY_DEBUG_ENABLED,
                 block_on_send=True)

    LOG.debug(f'sending to honeycomb: {data}')

    client = beeline.get_beeline().client
    if not isinstance(data, list):
        data = [data]

    for eventdata in data:
        ev = client.new_event()
        ev.add(eventdata)
        ev.send()

    client.flush()

    LOG.info(f'{len(data)} events shipped to honeycomb ..')


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(
        description=
        "Take data from a prometheus file or URL and ship off to honeycomb")

    parser.add_argument("-u",
                        "--url",
                        type=str,
                        help="URL to pull metrics from")
    parser.add_argument("-f",
                        "--file",
                        type=str,
                        help="Local file to pull metrics from")
    parser.add_argument(
        "-s",
        "--ship",
        action='store_true',
        help=
        "If selected, will send data to honeycomb, otherwise will print to screen"
    )
    parser.add_argument(
        "-e",
        "--extra-args",
        type=str,
        nargs='+',
        help=
        "Key=value value pair separated by space of extra args to add to payload"
    )

    parsed = parser.parse_args()

    return vars(parsed)


def get_url(url):
    """ pulls down a url and returns string of content """
    import urllib.request

    LOG.debug(f'getting url {url} ..')
    req = urllib.request.Request(url)
    return urllib.request.urlopen(req).read().decode()


if __name__ == "__main__":
    level = logging.getLevelName(os.getenv('LOG_LEVEL', 'INFO').upper())
    logging.basicConfig(
        level=level,
        format='%(asctime)s:%(levelname)s:%(module)s: %(message)s')

    args = parse_args()

    if args.get('url'):
        content = get_url(args.get('url')).split('\n')
    elif args.get('file'):
        with open(args.get('file')) as fd:
            content = fd.read().split('\n')
    else:
        LOG.info('reading from stdin ..')
        content = sys.stdin.readlines()

    parsed = parse_prometheus_content(content)

    if args.get('extra_args'):
        for entry in parsed:
            entry.update(dict([x.split('=') for x in args.get('extra_args')]))

    if args.get('ship'):
        honeycomb_send(parsed)
    else:
        LOG.info('not sending to honeycomb:')
        print(json.dumps(parsed, indent=2))
