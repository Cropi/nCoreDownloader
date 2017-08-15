# nCoreDownloader
## Description
Automation download tool for NCORE torrents.
## How to run (on Ubuntu 16.04)
### 	Install dependencies
```
	sudo add-apt-repository ppa:jonathonf/python-3.6
	sudo apt update
	sudo apt install python3.6

	sudo apt-get install python-pip
	pip install request
	pip install
```


### Configure
```
Utorrent -> preferences -> General -> Uncheck "Display window with torrent details" (Why? Add torrents without asking)
                        -> Directories -> Automatically load .torrents from: PATH/TO/THE/SCRIPT/torrents
Open settings.py folder and configure it:
	-nCore username
	-nCore password
	-timeDuration

Open searchList file and write there what do you want to download (EACH ONE IN A SINGLE ROW)
    Example: Game of thrones s07e04
             Game of thrones s07e03
             Game of thrones s07e02
```

### Run
```
	python download.py
```