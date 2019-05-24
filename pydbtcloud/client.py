import requests
from dataclasses import dataclass
from dataclasses import field
from typing import Dict


@dataclass
class DbtCloud:
    account_id: int
    api_token: str = field(repr=False)
    api_base: str = 'https://cloud.getdbt.com/api/v2'

    def _construct_headers(self) -> Dict:
        return {'Authorization': 'Token %s' % self.api_token}

    def _get(self, url_suffix: str, params: Dict = None) -> Dict:
        url = self.api_base + url_suffix
        headers = self._construct_headers()
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def _post(self, url_suffix: str, params: Dict = None, data: Dict = None) -> Dict:
        url = self.api_base + url_suffix
        headers = self._construct_headers()
        response = requests.post(url, headers=headers, params=params, data=data)
        response.raise_for_status()
        return response.json()

    def list_connections(self, params: Dict = None):
        url_suffix = f"/accounts/{self.account_id}/connections/"
        response = self._get(url_suffix, params)
        return DbtCloudResponse(self, url_suffix, params, response)

    def list_environments(self, params: Dict = None):
        url_suffix = f"/accounts/{self.account_id}/environments/"
        response = self._get(url_suffix, params)
        return DbtCloudResponse(self, url_suffix, params, response)

    def list_repositories(self, params: Dict = None):
        url_suffix = f"/accounts/{self.account_id}/repositories/"
        response = self._get(url_suffix, params)
        return DbtCloudResponse(self, url_suffix, params, response)

    def list_jobs(self, params: Dict = None):
        url_suffix = f"/accounts/{self.account_id}/jobs/"
        response = self._get(url_suffix, params)
        return DbtCloudResponse(self, url_suffix, params, response)

    def list_runs(self, params: Dict = None):
        url_suffix = f"/accounts/{self.account_id}/runs/"
        response = self._get(url_suffix, params)
        return DbtCloudResponse(self, url_suffix, params, response)

    def get_run(self, run_id: int, params: Dict = None):
        url_suffix = f"/accounts/{self.account_id}/runs/{run_id}/"
        response = self._get(url_suffix, params)
        return DbtCloudResponse(self, url_suffix, params, response)

    def get_repository(self, repository_id: int, params: Dict = None):
        url_suffix = f"/accounts/{self.account_id}/repositories/{repository_id}/"
        response = self._get(url_suffix, params)
        return DbtCloudResponse(self, url_suffix, params, response)

    def get_job(self, job_id: int, params: Dict = None):
        url_suffix = f"/accounts/{self.account_id}/jobs/{job_id}/"
        response = self._get(url_suffix, params)
        return DbtCloudResponse(self, url_suffix, params, response)

    def get_environment(self, environment_id: int, params: Dict = None):
        url_suffix = f"/accounts/{self.account_id}/environments/{environment_id}/"
        response = self._get(url_suffix, params)
        return DbtCloudResponse(self, url_suffix, params, response)

    def get_connection(self, connection_id: int, params: Dict = None):
        url_suffix = f"/accounts/{self.account_id}/connections/{connection_id}/"
        response = self._get(url_suffix, params)
        return DbtCloudResponse(self, url_suffix, params, response)

    def run_job(self, job_id: int, params: Dict = None, data: Dict = {'cause': 'Kicked off via pydbtcloud SDK'}):
        url_suffix = f"/accounts/{self.account_id}/jobs/{job_id}/run/"
        response = self._post(url_suffix, params, data)
        return DbtCloudResponse(self, url_suffix, params, response)

    def cancel_run(self, run_id: int, params: Dict = None, data: Dict = None):
        url_suffix = f"/accounts/{self.account_id}/runs/{run_id}/cancel/"
        response = self._post(url_suffix, params, data)
        return DbtCloudResponse(self, url_suffix, params, response)


@dataclass
class DbtCloudResponse:
    client: DbtCloud
    url_suffix: str
    params: Dict = None
    response: Dict = None

    def __iter__(self):
        self._iteration = 0
        return self

    def __next__(self):
        self._iteration += 1
        if self._iteration == 1:
            return self

        if self.response.get('status').get('is_success') is False:
            raise RuntimeError('Error while requesting data.')

        if self.response.get('extra') is None:
            raise StopIteration

        self.total_count: int = self.response.get('extra').get('pagination').get('total_count')
        self.count: int = self.response.get('extra').get('pagination').get('count')
        self.offset: int = self.response.get('extra').get('filters').get('offset')

        if self.total_count > self.offset:
            self.offset += self.response.get('extra').get('pagination').get('count')
            self.params = {"offset": self.offset}
            self.response = self.client._get(url_suffix=self.url_suffix, params=self.params)
            self.count += self.response.get('extra').get('pagination').get('count')
            return self
        else:
            raise StopIteration

    def get(self, key, default=None):
        return self.response.get(key, default)
