# jutsuload
### is a module and script for downloading videos from `jut.su` russian anime website
anything may be broken, not work, burn your pc? :), etc  
basic features are tested to work on few episodes
## Features
Uses browser headers.  
Can guess season and episode from URL (not all types are supported).  
Downloader for videos, with progress functionality.  
Does not overwrite files.  
Has small dependency list.
And other non-mentioned from `--help`  
(but episode lists don't work yet)
## Promised 
Implement installing it as a module;  
todo in main.py
## Usage
```
$ python .\main.py --help                                                                                   
usage: main.py [-h] [-e | -p] [-ep EP] [-q {worst,240p,360p,480p,720p,1080p,best}] [-d | -g] [--progress] [-o OUTFILE] [--chunk-size CHUNK_SIZE] URL

Example script using functions of my Jut.su helper module.

positional arguments:
  URL                   Episode URL or episode list page URL. (default mode: guess and download)

options:
  -h, --help            show this help message and exit
  -e, --episode         Episode mode.
  -p, --page            Page mode (episode list page).
  -ep EP                Numbers of episodes to download from page,
                                                        required to download a page (you will be prompted otherwise.
                                                        can be specified many times e.g. -ep 12-5 -ep 2; -ep 5-12
  -q {worst,240p,360p,480p,720p,1080p,best}
                        Quality to use on the page.
                                                        If not available, use any best. Default is 720p
  -d, --download        Download the file.
  -g, --link            Get the link in quiet mode.
  --progress            Show download progress in download mode.
  -o OUTFILE, --out OUTFILE
                        Output file path. Does not overwrite. (downloaded container is MP4)
                                                        Default: current directory, guessed file name.
  --chunk-size CHUNK_SIZE
                        Size of each chunk to download before write.
                                                        May affect download performance, default 262144,
                                                        works best with a power of two.
```
### Example
```
$ python main.py https://jut.su/yakusoku-neverland/season-2/episode-7.html -q worst --progress

79.00MB, 39422.964KB/s           Done
```