import hashlib

# The ROOT URL config

BASE_URL = "http://127.0.0.1:8000"

# Sina Weibo related consts

WEIBO_KEY    = '1036427558'
WEIBO_SECRET = '35b26b1a0cf9782b78b64b5d566ac0b0'

# Renren related consts

RENREN_KEY    = 'da463374f6ce469ab8b0b7a8d64d6a4e'
RENREN_SECRET = '2c0933bac49a4ff7819e56575c09b0d8'

# Douban related consts

DOUBAN_KEY    = "0c672e7e31aa9b5025358b7a94ffd1f0"
DOUBAN_SECRET = "cadbe6a3746e7f4e"

# GitHub related consts

GITHUB_KEY    = "9fbb508f251c22cecdb0"
GITHUB_SECRET = "53cee8d01b08c216b6b652ae935d95b2961980bc"

# QQ related consts

QQ_KEY    = "801074414"
QQ_SECRET = "6cf49c0e8ad7e05f644c6d71fe2ff2d8"

# Taobao related consts

TAOBAO_KEY    = "12456540"
TAOBAO_SECRET = "87b4d10bd4a5737be09c96f7a889452e"

# Common functions

def calc_md5(str):
    hasher = hashlib.md5()
    hasher.update(str)
    return hasher.hexdigest()    