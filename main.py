from download_links import*
import multiprocessing as mp
from bs4 import BeautifulSoup
from multiprocessing import Process
from multiprocessing import Pool as process_pool
from multiprocessing.dummy import Pool as thread_pool
import requests, time, os, sys, weasyprint, argparse, fnmatch, shutil

def tutorialspoint():
	pass

def tutorialspoint_all():
	pass

def get_page(url):
	while True:
		try:
			page_response = requests.get(url, timeout=5)
			soup = BeautifulSoup(page_response.content, "html.parser")
			str_soup = str(soup)
		except:
			print("    >>  Could not connect to "+url.split("/")[-1]+", retrying")
			time.sleep(1)
			continue
		else:
			print("    >>  Downloaded " + url.split("/")[-1])
			break
	page = str_soup[str_soup.find("<h1"):]
	if "Prerequisite" in page:
		page = page.split("Prerequisite")[0][:page.rfind("<hr")]
	elif "nexttopicdiv" in page:
		page = page.split("nexttopicdiv")[0][:page.rfind("<hr")]
	elif "bottomnext" in page:
		page = page.split("nexttopicdiv")[0][:page.rfind("<br")]
	else:
		print("Couldn't find delimiter")

	# str_soup.find("<hr")
	return page

def save_pdf(tutorial):
	tutorial = str(tutorial.split(".")[0])
	if not os.path.exists('..'+os.sep+'Javatpoint_Downloads'+os.sep+tutorial):
		os.makedirs('..'+os.sep+'Javatpoint_Downloads'+os.sep+tutorial)
	print("Converting "+tutorial+" in pdf,\nplease wait, it may take a while...")
	try:
		html = weasyprint.HTML('..'+os.sep+'temp'+os.sep+tutorial+".html")
		main_doc = html.render()
		pdf = main_doc.write_pdf()
		with open('..'+os.sep+'Javatpoint_Downloads'+os.sep+tutorial+os.sep+tutorial+".pdf", 'wb') as f:
			f.write(pdf)
		print(tutorial + " pdf saved")
		os.remove('..'+os.sep+'temp'+os.sep+tutorial+".html")
	except:
		pass
	return

def html_to_pdf():
	completed_tutorials = []
	while not os.listdir('..'+os.sep+'temp'):
		time.sleep(2)

	while os.listdir('..'+os.sep+'temp'):
		tutorials = fnmatch.filter(os.listdir('..'+os.sep+'temp'), '*.html')
		for tutorial in tutorials:
			if tutorial not in completed_tutorials:
				save_pdf_runner = Process(target=save_pdf, args=(tutorial,))
				save_pdf_runner.start()
				completed_tutorials.append(tutorial)

	save_pdf_runner.join()
	try:
		os.rmdir('..'+os.sep+'temp')
	except:
		print("cannot delete '../temp' as it is not empty")
	return

def javatpoint(url, tutorial=None):
	if tutorial is None:
		tutorial = url.split("/")[-1]
	print("Downloading " + tutorial)
	tryAgain=0
	while tryAgain<5:
		try:
			page_response = requests.get(url, timeout=5)
			soup = BeautifulSoup(page_response.content, "html.parser")
			str_soup = str(soup)
		except:
			# raise
			print("Could not connect, trying again in 1 seconds!")
			time.sleep(1)
			continue
		tryAgain+=1
	links = []

	for div in soup.find_all("div", attrs={"class":"leftmenu"}):
		for a in div.find_all("a"):
			links.append(url[:url.rfind("/")+1] + a["href"])

	pages = []
	with thread_pool(processes = 2*mp.cpu_count()) as pool:
		pages = pool.map(get_page, links)

	page = str_soup[:str_soup.find("<body")] + "\n<body>\n" + "".join(pages)+ "\n</body>\n</html>"

	with open ('..'+os.sep+'temp'+os.sep+tutorial+".html","w") as f:
		f.write(page)
	# os.system('xdg-open page.html')
	# os.system('xdg-open page.pdf')
	print(tutorial + " download completed")
	return

def javatpoint_all():
	url = "https://www.javatpoint.com/"

	tryAgain=0
	print("Connecting to Javatpoint")
	while tryAgain<5:
		try:
			page_response = requests.get(url, timeout=5)
			soup = BeautifulSoup(page_response.content, "html.parser")
			str_soup = str(soup)
		except:
			# raise
			print("Could not connect, trying again in 1 seconds!")
			time.sleep(1)
			continue
		tryAgain+=1

	tutorials = []
	links = []
	break_condition = False
	for div in soup.find_all("div", attrs={"class":"firsthomecontent"}):
		if break_condition:
			break
		for a in div.find_all("a"):
			if "forum" in a["href"]:
				break_condition = True
				break
			if "http" in a["href"]:
				links.append(a["href"])
			else:
				links.append("https://www.javatpoint.com/" + a["href"])
			for tutorial_name in a.find_all("p"):
				tutorials.append(tutorial_name.contents[0])

	with thread_pool(processes = 3) as pool:
		pool.starmap(javatpoint, zip(links, tutorials))
	return


def download_list_all():
	javatpoint_list = []
	tutorialspoint_list = []
	for link in download_list:
		if "https://www.javatpoint.com/" in link:
			javatpoint_list.append(link)
		elif "https://www.tutorialspoint.com/" in link:
			turorialspoint_list.append(link)
		else:
			print(link + " is not a valid link!")

	def javatpoint_start():
		with thread_pool(processes = 3) as pool:
			pool.map(javatpoint, javatpoint_list)
		return
	def tutorialspoint_start():
		with thread_pool(processes = 3) as pool:
			pool.map(tutorialspoint, tutorialspoint_list)
		return
	javatpoint_runner = Process(target=javatpoint_start)
	tutorialspoint_runner = Process(target=tutorialspoint_start)
	javatpoint_runner.start()
	tutorialspoint_runner.start()
	return

def main():

	parser = argparse.ArgumentParser(description="download pdf of any tutorial on javatpoint")
	parser.add_argument("-a", "--all", action="store_true", help="download all tutorials from javatpoint and tutorialspoint")
	parser.add_argument("-j", "--javatpoint", action="store_true", help="download all tutorials from javatpoint")
	parser.add_argument("-t", "--tutorialspoint", action="store_true", help="download all tutorials from tutorialspoint")
	parser.add_argument("-u", "--url", action="store_true", help="download all tutorials mentioned in 'download_links.txt'")
	if len(sys.argv) < 2:
		parser.print_usage()
		sys.exit(1)
	args = parser.parse_args()

	if not os.path.exists('..'+os.sep+'Javatpoint_Downloads'):
		os.makedirs('..'+os.sep+'Javatpoint_Downloads')
	if os.path.exists('..'+os.sep+'temp'):
		shutil.rmtree('..'+os.sep+'temp')
	os.makedirs('..'+os.sep+'temp')

	pdf_conversion = Process(target=html_to_pdf)
	pdf_conversion.start()

	if args.all:
		javatpoint_all()
		tutorialspoint_all()

	if args.javatpoint:
		javatpoint_all()

	if args.tutorialspoint:
		tutorialspoint_all()

	elif args.url:
		download_list_all()

	return

if __name__=="__main__":
	main()