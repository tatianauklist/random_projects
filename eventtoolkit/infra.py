import os
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging
from google.oauth2 import service_account
from typing import Union, List, Any, Dict
import yaml

def _load_config():
    try:
        with open("config.yaml.example", 'r') as configFile:
                config = yaml.safe_load(configFile)
                return config
    except FileNotFoundError:
        logging.error("config.yaml not found")
        raise FileNotFoundError("config.yaml not found")

def _validateConfig(config):
    if "services" in config and "credentials" in config:
        return True
    else:
        logging.error("Missing required keys in config file")
        raise ValueError("Missing required keys in config file")

def _getValidCredentials(scopes: list[str],config:dict) -> Credentials:
    credentials = config["credentials"]
    file = credentials["file"]
    try:
        creds = service_account.Credentials.from_service_account_file(file, scopes=scopes)

    except FileNotFoundError:
        logging.error("Credentials not found")
        raise FileNotFoundError("Credentials not found")

    return creds

def _resolveScope(serviceName: str, scopes: list[str],config: dict):
    if serviceName in config['services']:
        serviceConfig = config["services"][serviceName]
        scopesDict = serviceConfig["scopes"]
        urls = []
        for permission in scopes:
            url = serviceConfig["scopes"][permission]
            urls.append(url)
        return urls

def getAuthenticatedService(serviceName: str, access: list=None, config: str="config.yaml"):
    config = _load_config()
    validConfig = _validateConfig(config)
    resolvedScope = _resolveScope(serviceName, access, config)
    credentials = _getValidCredentials(resolvedScope, config)
    try:
        logging.info("Authenticating with Google API")
        service = build(serviceName, config["services"][serviceName]["version"], credentials=credentials)
        return service

    except HttpError as err:
        logging.error(f"Failed to connect to Google Sheets API: {err}")












