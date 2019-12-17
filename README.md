# tutorial-pdf-downloader

[![Build Status](https://api.travis-ci.com/Gunjan933/tutorial-pdf-downloader.svg?branch=master)](https://travis-ci.com/Gunjan933/tutorial-pdf-downloader) [![Known Vulnerabilities](https://img.shields.io/badge/vulnerabilities%20-0-brightgreen.svg?style=flat)](https://snyk.io//test/github/Gunjan933/tutorial-pdf-downloader?targetFile=requirements.txt) [![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/Gunjan933/tutorial-pdf-downloader/graphs/contributors) [![python >=3.5](https://img.shields.io/badge/python->=3.5-blue.svg?style=flat)](#python-support)

Downloads full tutorial PDFs from **[Javatpoint](https://www.javatpoint.com/)**, **[Tutorialspoint](https://www.tutorialspoint.com/)**  and other websites.

## Disclaimer / Please note:

These websites can provide free and quality education by showing advertisements, that's their only source of income. Don't overuse this script, as it gives their server huge pressure. This script is for those, who are poor, who don't have the luxury of stable and sustained internet connection. As I think education should be free for all, doesn't mean I support piracy. This is for educational purposes only. Always support their work, either by paying or visiting their websites.

## Usage

### First install depedencies:
Make sure you have pip installed, then run

```console
pip install --user -r requirements.txt
 ```
### Set up download links:
* Copy any links from any tutorial from **[Javatpoint](https://www.javatpoint.com/)** or **[Tutorialspoint](https://www.tutorialspoint.com/)** or **both** and paste it in `download_links.py`.
	- To see examples, open **[download_links.py](./download_links.py)**
* If you want to download all listed tutorial in both sites, then jump to next step.

### Run the Downloader:
* To download each links from `download_links.py` that you set earlier:

	```console
	python main.py -u
	```
* To download all tutorials from Javatpoint:

	```console
	python main.py -j
	```
* To download all tutorials from Tutorialspoint:

	```console
	python main.py -t
	```
* To download all tutorials from Javatpoint and Tutorialspoint:

	```console
	python main.py -a
	```
* To check usages or help:

	```console
	python main.py -h
	```

## Save location

PDFs are saved in the same directory, in which you cloned the repository.
```
-- some_parent_directory
   |
   |-- tutorial-pdf-downloader
   |   |
   |   |--main.py
   |   |--download_links.py
   |   |--requirements.txt
   |   |--README.md
   |
   |
   |-- downloads
       |
       |--artificial-intelligence
       |--mobile-computing
```

## Changelog
* Added **[Tutorialspoint](https://www.tutorialspoint.com/)** support.

## Future works
* ~~Add **[Tutorialspoint](https://www.tutorialspoint.com/)** support.~~
* Add GUI.

## Bugs / Issues
* If found, please report it in issues section.

## Contribute
* Any contributions or suggestions are welcome.