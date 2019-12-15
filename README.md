# tutorial-pdf-downloader
Downloads full tutorial pdf from javatpoint, tutorialspoint and other websites
## Usage
### First install depedencies:
Make sure you have pip installed, and run

```bash
pip install --user -r requirements.txt
 ```
### Set up download links:
* Copy any links from any tutorial from **[Javatpoint](https://www.javatpoint.com/)** and paste it in `download_links.py`.
* If you want to download every tutorial, then jump to next step.

### Run the Downloader:
* To download each links from `download_links.py` that you set earlier:

	```bash
	python downloader.py -u
	```
* To download all tutorials from Javatpoint:

	```bash
	python downloader.py -a
	```
* To check usages or help:

	```bash
	python downloader.py -h
	```

## Future works
* Add Tutorialspoint support.
* Add GUI.

## Bugs/ Issues
* If found, please report it in issues section.

## Contribute
* Any contributions or suggestions are welcome.