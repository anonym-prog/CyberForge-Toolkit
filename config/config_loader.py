#!/usr/bin/env python3
import configparser
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'settings.conf')

def load_config():
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_PATH):
        print("[!] Config file not found, using defaults")
        return {}
    config.read(CONFIG_PATH)
    return config

def get_setting(section, key, fallback=None):
    config = load_config()
    try:
        return config.get(section, key)
    except:
        return fallback
