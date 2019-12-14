import requests, time, os, weasyprint
import multiprocessing as mp
from multiprocessing.dummy import Pool
from bs4 import BeautifulSoup

def get_page(url):
	print(url.split("/")[-1] + "                   \r")
	while True:
		try:
			page_response = requests.get(url, timeout=5)
			soup = BeautifulSoup(page_response.content, "html.parser")
			str_soup = str(soup)
		except:
			print("Could not connect, trying again in 1 seconds!\r",end="")
			time.sleep(1)
			continue
		else:
			break
	page = str_soup[str_soup.find("<h1"):str_soup.find("<hr")]
	return page

def main():
	url = "https://www.javatpoint.com/artificial-intelligence-tutorial"
	tryAgain=0
	print("Setting connection\r",end="")
	while tryAgain<5:
		try:
			page_response = requests.get(url, timeout=5)
			soup = BeautifulSoup(page_response.content, "html.parser")
			str_soup = str(soup)
		except:
			raise
			# print("Could not connect, trying again in 1 seconds!\r",end="")
			# time.sleep(1)
			# continue
		tryAgain+=1
	links = []

	for div in soup.find_all("div", attrs={"class":"leftmenu"}):
		for a in div.find_all("a"):
			links.append("https://www.javatpoint.com/" + a["href"])

	pages = []
	with Pool(processes = 2*mp.cpu_count()) as pool:
		pages = pool.map(get_page, links[1:])

	page = str_soup[:str_soup.find("<body")] + "\n<body>\n" +  str_soup[str_soup.find("<h1"):str_soup.find("<hr")] + "".join(pages)+ "\n</body>\n</html>"

	with open ("page.html","w") as f:
		f.write(page)
	print("Completed")
	# os.system('xdg-open page.html')

	pdf = weasyprint.HTML(page).write_pdf()

	file('page.pdf', 'wb').write(pdf)
	os.system('xdg-open page.pdf')

if __name__=="__main__":
	main()