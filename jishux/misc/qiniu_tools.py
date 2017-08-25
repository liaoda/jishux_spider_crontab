# 七牛云存储配置项

import time
from .all_secret_set import qiniu_config
from qiniu import Auth, put_file, etag
access_key = qiniu_config['access_key']
secret_key = qiniu_config['secret_key']
bucket_name = qiniu_config['bucket_name']
image_domain = qiniu_config['image_domain']
suffix = qiniu_config['suffix']


def upload_file(self, file_path, file_name):
    # print(file_path)
    # print(file_name)
    date = time.strftime('%Y/%m/%d', time.localtime(time.time()))
    file_name = 'jishux/' + date + file_name
    q = Auth(access_key,secret_key)
    token = q.upload_token(bucket_name, file_name, 3600)
    ret, info = put_file(token, file_name, file_path)
    assert ret['key'] == file_name
    assert ret['hash'] == etag(file_path)
    # os.remove(file_path)
    return image_domain + file_name + suffix