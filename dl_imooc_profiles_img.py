#coding: utf-8
#批量下载慕课网系统随机头像
from urllib import request
import json
import os

cookie = ''#登陆后的cookie
req = request.Request('http://www.imooc.com/user/randimage/?type=1')
req.add_header('Cookie', cookie)

def get_img(num=100, save_dir='profiles'):
	save_dir = os.path.join('.', save_dir)
	if not os.path.isdir(save_dir):
		os.mkdir(save_dir)
	imgs = set()
	while len(imgs)<num:
		with request.urlopen(req) as result:
			img_url = json.loads(result.read().decode('utf-8'))['imgpath']
			img_name = os.path.split(img_url)[1]
		with open(os.path.join(save_dir, img_name), 'wb') as tmp_img, request.urlopen(img_url) as dl_img:
			tmp_img.write(dl_img.read())
			imgs.add(img_name)

if __name__ == '__main__':
	get_img()
	print('done')