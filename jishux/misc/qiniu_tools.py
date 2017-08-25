# 七牛云存储配置项

import time
from qiniu import Auth, put_file, etag
access_key = 'xgt-TDgBWe5e2rjotJnL6e0UbuIK253uL0IF6pvv'
secret_key = '9okIxkQuSU8s1QU0zTrRr7vlIa3PxHPuGYKOFIFg'
bucket_name = 'xapp'
image_domain = 'http://7xw8xm.com2.z0.glb.qiniucdn.com/'
suffix = '?imageMogr2/interlace/1' #图片后缀参数


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