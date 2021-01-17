#!/usr/local/bin/python3

from pathlib import Path
import datetime
from logging import getLogger
from typing import Union

import asyncio
import pyppeteer
import requests

from .ExportData import ExportData


logger = getLogger(__name__)


class HealthPlanetExport:
    MaxPeriod = 28 * 3
    RedirectURL = 'https://www.healthplanet.jp/success.html'
    AuthBaseURL = 'https://www.healthplanet.jp/oauth/auth'
    TokenURL = 'https://www.healthplanet.jp/oauth/token'
    StatusBaseURL = 'https://www.healthplanet.jp/status'

    def __init__(self, client_id: str, client_secret: str, login_id: str, login_pass: str):
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.login_id: str = login_id
        self.login_pass: str = login_pass

        self.scope: str ='innerscan'

        self.code: str = None
        self.access_token: str = None
        self.export_data: ExportData = None

    def _get_url_with_params(self, url_org: str, params: dict):
        return '{}?{}'.format(
            url_org,
            '&'.join([f'{k}={v}' for k, v in params.items()])
        )

    async def _get_auth(self):
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.RedirectURL,
            'scope': self.scope,
            'response_type': 'code'
        }

        browser = await pyppeteer.launch(headless=True)
        page = await browser.newPage()
        await page.goto(self._get_url_with_params(self.AuthBaseURL, params))
        await page.type('input[name=loginId]', self.login_id)
        await page.type('input[name=passwd]', self.login_pass)
        await asyncio.wait([
            page.click('input.mt15'), page.waitForNavigation()
        ])
        await asyncio.wait([
            page.click('li.ml20 img'), page.waitForNavigation()
        ])
        code = await page.querySelectorEval('textarea#code', 'e => e.value')
        await browser.close()
        self.code = code

    def get_auth(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._get_auth())
        logger.debug(f'code: {self.code}')

    def get_token(self):
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.RedirectURL,
            'code': self.code,
            'grant_type': 'authorization_code'
        }

        resp = requests.post(self.TokenURL, data=data)
        self.access_token = resp.json()['access_token']
        logger.debug(f'access token: {self.access_token}')

    def _get_data_json(self, from_date: datetime.datetime, to_date: datetime.datetime = None):
        if from_date is None:
            from_date = (to_date - datetime.timedelta(days=self.MaxPeriod))
        data = {
            'access_token': self.access_token,
            'date': 1,
            'from': from_date.strftime("%Y%m%d%H%M%S"),
            'to': to_date.strftime("%Y%m%d%H%M%S"),
            'tag': '6021,6022',
            'scope': self.scope
        }

        url = f'{self.StatusBaseURL}/{self.scope}.json'
        request = requests.Request('GET', url)
        prepared = request.prepare()
        prepared.url += self._get_url_with_params('', data)
        logger.debug(f'prepared.url: {prepared.url}')

        session = requests.Session()
        resp = session.send(prepared)
        logger.debug(f'status code: {resp.status_code}')
        return resp.text

    @classmethod
    def _convert_str2datetime(cls, s: str):
        if s == 'today':
            return datetime.datetime.now()
        elif s == 'minimum':
            return datetime.datetime.now() - datetime.timedelta(days=cls.MaxPeriod)
        else:
            return datetime.datetime.strptime(s, '%Y%m%d')

    def _add_data_dict(self, data: dict):
        if self.export_data is None:
            self.export_data = ExportData.from_json(data)
        else:
            assert isinstance(self.export_data, ExportData)
            export_data = ExportData.from_json(data)
            self.export_data.data.extend(export_data.data)

    def get_data(self, from_date: str, to_date: str):
        fd = self._convert_str2datetime(from_date)
        td = self._convert_str2datetime(to_date)

        begin_date = td - datetime.timedelta(days=self.MaxPeriod)
        end_date = td
        while end_date > fd:
            logger.debug(f'begin date: {begin_date}, end date: {end_date}')
            self._add_data_dict(self._get_data_json(begin_date, end_date))
            end_date = begin_date
            begin_date -= datetime.timedelta(days=self.MaxPeriod)
            if begin_date < fd:
                begin_date = fd

    def save(self, out_file_path: Union[str, Path]):
        if isinstance(out_file_path, str):
            out_file_path = Path(out_file_path)
        with out_file_path.open('w') as f:
            print(self.export_data.to_json(indent=4), file=f)
