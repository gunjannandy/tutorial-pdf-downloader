import multiprocessing as mp
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool
import requests, time, os, weasyprint, argparse

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

def javatpoint(url, tutorial=None):
	if tutorial is None:
		tutorial = url.split("/")[-1]
	if not os.path.exists('..'+os.sep+'Javatpoint_Downloads'+os.sep+tutorial):
		os.makedirs('..'+os.sep+'Javatpoint_Downloads'+os.sep+tutorial)
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

	# for i,link in enumerate(links):
	# 	print(i,link)

	pages = []
	with Pool(processes = 2*mp.cpu_count()) as pool:
		pages = pool.map(get_page, links)

	page = str_soup[:str_soup.find("<body")] + "\n<body>\n" + "".join(pages)+ "\n</body>\n</html>"

	with open ('..'+os.sep+'Javatpoint_Downloads'+os.sep+tutorial+os.sep+tutorial+".html","w") as f:
		f.write(page)
	# os.system('xdg-open page.html')

	print("Converting in pdf, please wait, it may take a while...")
	html = weasyprint.HTML('..'+os.sep+'Javatpoint_Downloads'+os.sep+tutorial+os.sep+tutorial+".html")
	main_doc = html.render()
	pdf = main_doc.write_pdf()
	with open('..'+os.sep+'Javatpoint_Downloads'+os.sep+tutorial+os.sep+tutorial+".pdf", 'wb') as f:
		f.write(pdf)

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

	with Pool(processes = 2*mp.cpu_count()) as pool:
		pool.starmap(javatpoint, zip(links, tutorials))
	return

def main():

	if not os.path.exists('..'+os.sep+'Javatpoint_Downloads'):
		os.makedirs('..'+os.sep+'Javatpoint_Downloads')
	parser = argparse.ArgumentParser(description="download pdf of any tutorial on javatpoint")
	parser.add_argument("-a", "--all", action="store_true", help="download all tutorials from javatpoint")
	parser.add_argument("-u", "--url", action="store_true", help="download all tutorials mentioned in 'download_links.txt'")
	args = parser.parse_args()

	if args.all:
		javatpoint_all()
	elif args.url:
		links = []
		with open ("download_links.txt","r") as f:
			links = f.read().split("\n")
		for link in links:
			if "https://www.javatpoint.com/" not in link:
				print(link + " is not a valid javatpoint link!")
				return
		with Pool(processes = 2*mp.cpu_count()) as pool:
			pool.map(javatpoint, links)

	return

if __name__=="__main__":
	main()