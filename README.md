# jutsuload

### is a module and script for downloading videos from `jut.su` russian anime website

anything may be broken, not work, burn your pc? :), etc  
basic features are tested to work on few episodes
tested on python 3.10.6 and requests 2.28.1

## Features

Uses browser headers.  
Can guess season and episode from URL (not all types are supported).  
Downloader for videos, with progress functionality.  
Does not overwrite files.  
Has small dependency list.
And other non-mentioned from `--help`  
Can download episode lists or few episodes from them.

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

Default naming scheme is: `<anime-name>_s<season>_e<episode>.mp4`, as
in `https://jut.su/<anime-name>/season-<season>/episode-<episode>.html`

### Example

```
$ python main.py https://jut.su/yakusoku-neverland/season-2/episode-7.html -q worst --progress

79.00/79.01MB, 51269.724KB/s, 2620.389KB/s avg           Done
```

```
$ python .\main.py https://jut.su/yakusoku-neverland/
1) S1 EP1
2) S1 EP2
3) S1 EP3
4) S1 EP4
5) S1 EP5
6) S1 EP6
7) S1 EP7
8) S1 EP8
9) S1 EP9
10) S1 EP10
11) S1 EP11
12) S1 EP12
13) S2 EP1
14) S2 EP2
15) S2 EP3
16) S2 EP4
17) S2 EP5
19) S2 EP7
20) S2 EP8
21) S2 EP9
22) S2 EP10
23) S2 EP11
What do you want downloaded? (for example 1-15; 1-15 20-25 17; 2)
> 1-4
(files are being downloaded in specified order)
```