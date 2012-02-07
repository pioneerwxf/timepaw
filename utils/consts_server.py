import hashlib

# The ROOT URL config

BASE_URL = "http://www.timepaw.com"

# Sina Weibo related consts

WEIBO_KEY    = '2247177954' #'602940159'
WEIBO_SECRET = '9d3d0383018ee9af1182fd0b75cf750b' #'53dea87025dee532822a774fe2b76bac'

# Renren related consts

RENREN_KEY    = '74584b4e87af47c599515de99655bebb'
RENREN_SECRET = '656724e3c6264f31b8a6cc0d1d147058'

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

TAOBAO_KEY    = "12459617"
TAOBAO_SECRET = "6c6d654780e339754c33304320018d93"

# Common functions

def calc_md5(str):
    hasher = hashlib.md5()
    hasher.update(str)
    return hasher.hexdigest()