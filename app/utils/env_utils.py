import os
from os.path import exists

from dotenv import dotenv_values


def load_config(env_file=".env"):
    if exists(env_file):
        return load_from_file(env_file)

    return load_from_env()


def load_from_file(env_file):
    return dotenv_values(env_file)


def load_from_env():
    return os.environ
