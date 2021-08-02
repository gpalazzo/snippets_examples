"""
    Download files from Google Drive if executed inside Google Colab
"""

import requests
import warnings
from sys import stdout
from os import makedirs
from os.path import dirname, exists

class GoogleDriveDownloader:

    CHUNK_SIZE = 32768
    DOWNLOAD_URL = "https://docs.google.com/uc?export=download"

    @staticmethod
    def download_file_from_google_drive(file_id, dest_path, overwrite=False, unzip=False):

        destination_directory = dirname(dest_path)
        if not exists(destination_directory):
            makedirs(destination_directory)

        if not exists(dest_path) or overwrite:

            session = requests.Session()

            print('Downloading id {} to {}... '.format(file_id, dest_path), end='')
            stdout.flush()

            response = session.get(GoogleDriveDownloader.DOWNLOAD_URL, params={'id': file_id}, stream=True)

            token = GoogleDriveDownloader._get_confirm_token(response)
            if token:
                params = {'id': file_id, 'confirm': token}
                response = session.get(GoogleDriveDownloader.DOWNLOAD_URL, params=params, stream=True)

            GoogleDriveDownloader._save_response_content(response, dest_path)
            print('Success.')

    @staticmethod
    def _get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None

    @staticmethod
    def _save_response_content(response, destination):
        with open(destination, "wb") as f:
            for chunk in response.iter_content(GoogleDriveDownloader.CHUNK_SIZE):
                if chunk:
                    f.write(chunk)


_dir = "/path/to/output"
file_id = ["file_id_1", "file_id_2", "file_id_N"]
file_name = ["name_file_1", "name_file_2", "name_file_N"]

for idx, id in enumerate(file_id):
    GoogleDriveDownloader.download_file_from_google_drive(id, _dir + file_name[idx])