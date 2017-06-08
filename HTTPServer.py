'''
	简易多线程HTTP服务器，实现了处理GET/POST请求、COOKIE管理等简单功能
'''
import socket as S
import threading

class HTTPServer(object):
	def __init__(self, conf):
		self.conf = conf
		self.servSock = S.socket(S.AF_INET, S.SOCK_STREAM)
		addr = (conf['host'], conf['port'])
		self.servSock.bind(addr)

	def start(self):
		self.servSock.listen(self.conf['backlog'])
		while True:
			cliSock, addr = self.servSock.accept()
			t = threading.Thread(target=self._request, args=(cliSock,))
			t.start()

	def _request(self, s):
		req = []
		while True:
			bf = s.recv(self.conf['bfsz'])
			if not bf:
				break
			req.append(bf)
			if bf.find(b'\r\n\r\n') != -1:
				break
		try:
			req = b''.join(req)
			header, data = req.split(b'\r\n\r\n', 1)
			header = header.decode('ASCII')
			header = header.split('\r\n')
			method, url, version = header[0].strip().split(' ')
			del header[0]
			method = method.upper()
			if not method in ['GET', 'POST']:
				return
			headers = {}
			for i in header:
				k, v = i.split(':', 1)
				headers[k.upper()] = v
		except:
			return
		if method == 'POST':
			try:
				contLength = int(headers['CONTENT-LENGTH'])
				if contLength > 0:
					while len(data) < contLength:
						bf = s.recv(self.conf['bfsz'])
						data += bf
			except:
				pass
		cookie = {}
		try:
			tmp = headers['COOKIE'].split(';')
			for i in tmp:
				i = i.strip()
				k, v = i.split('=', 1)
				cookie[k] = v
		except:
			pass
		s.send(self._reponse(method, url, cookie, data, headers))
		s.close()

	def _reponse(self, method, url, cookie, data, headers):
		d = b'HTTP/1.1 200 OK\r\nContent-Type: text/html;charset=utf-8\r\n\r\n'
		d += b'<html><head><title>test</title></head><body>'
		d += b'<div>Method: %s</div>' % method.encode('ASCII')
		d += b'<div>Url: %s</div>' % url.encode('ASCII')
		d += b'<div>Cookie: %s</div>' % str(cookie).encode('ASCII')
		d += b'<div>Data: %s</div>' % data
		d += b'<div>Headers: %s</div>' % str(headers).encode('ASCII')
		d += b'</body></html>'
		return d

if __name__ == '__main__':
        conf = {
            'host': '',
            'port': 1919,
            'bfsz': 1024,
            'backlog': 10
        }
        hs = HTTPServer(conf)
        hs.start()
