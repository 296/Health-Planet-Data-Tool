#!/usr/local/bin/python3

from pathlib import Path
from logging import basicConfig, getLogger, DEBUG, INFO, StreamHandler, Filter
from bullet import Password

from HealthPlanetDataTool import HealthPlanetExport


def main(args):
    logger = getLogger(__name__)
    sh = StreamHandler()
    sh.addFilter(Filter('HealthPlanetDataTool'))
    basicConfig(handlers=[sh])
    if args.verbose:
        getLogger('HealthPlanetDataTool').setLevel(DEBUG)
    else:
        getLogger('HealthPlanetDataTool').setLevel(INFO)

    passwd_client = Password(prompt='Please enter your password: ')
    passwd = passwd_client.launch()

    client = HealthPlanetExport(
        client_id=args.client_id,
        client_secret=args.client_secret,
        login_id=args.login_id,
        login_pass=passwd
    )
    client.get_auth()
    client.get_token()
    client.get_data(args.from_date, args.to_date)
    client.save(args.out_file)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--login_id', type=str, required=True, help='your login id')
    parser.add_argument('-c', '--client_id', type=str, required=True, help='client id')
    parser.add_argument('-s', '--client_secret', type=str, required=True, help='client secret')
    parser.add_argument('-t', '--to', dest='to_date', type=str, default='today', help='end of the period [YYYYmmdd]')
    parser.add_argument('-f', '--from', dest='from_date', type=str, default='minimum', help='begging of the period [YYYYmmdd]')
    parser.add_argument('-o', '--out', dest='out_file', type=Path, default='out.json')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()
    main(args)
