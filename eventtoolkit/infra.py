import os
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging
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
    token = credentials["token"]
    creds = None

    if os.path.exists(token):
        creds = Credentials.from_authorized_user_file(token, scopes)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(file, scopes)
            creds = flow.run_local_server(port=0)

        # save creds for next run
    with open(token, "w") as token_file:
         token_file.write(creds.to_json())

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












