import concurrent.futures
import requests
import threading
import sys
import time
import urllib3
from colorama import Fore, Style
urllib3.disable_warnings()
inputfile=sys.argv[1]
outputfile=sys.argv[2]
output=open(outputfile, "a")
with open(inputfile, "r") as f:
	inputurl = [line.rstrip() for line in f]
threadLocal = threading.local()
count = len(inputurl)
print("number of urls = " + str(count))
def get_session():
    if not hasattr(threadLocal, "session"):
        threadLocal.session = requests.Session()
    return threadLocal.session
def check_allowed_methods(url):
	try :
		session=get_session()
		res=session.options(url, timeout=1, allow_redirects=False)
		if res.headers:
			methods=url + " : " + res.headers['allow']
			print(Style.BRIGHT + Fore.WHITE + (url)+ " : " + Fore.YELLOW + (res.headers['allow']))
			output.write(methods +"\n")
		else :
			print(Style.BRIGHT + Fore.WHITE + (url)+ " : " + Fore.RED + str(res.status_code))
	except:
		pass
def itterate_url(inputurl):
	url=inputurl
	check_allowed_methods(url)
	
if __name__ == "__main__":
	start_time = time.time()
	with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
       		executor.map(itterate_url, inputurl)
	duration = time.time() - start_time
	print("finished in : " + str(duration) + "  sec")





