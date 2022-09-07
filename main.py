#!/usr/bin/python
import sys
import jutsu
import argparse

# todo:
#  episode list page mode (options are placeholders)
#  alternative info source (there are other url formats and better sources on the page)
#  film url processing
#  interactive mode
#  ffmpeg interaction
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Example script using functions of my Jut.su helper module.',
                                     formatter_class=argparse.RawTextHelpFormatter)  # formatter to support newlines
    parser.add_argument('url', metavar='URL', type=str,
                        help='Episode URL or episode list page URL. (default mode: guess and download)')
    m = parser.add_mutually_exclusive_group()
    m.add_argument('-e', '--episode', dest='mode', action='store_const',
                   default=0, const=1, help='Episode mode.')
    m.add_argument('-p', '--page', dest='mode', action='store_const',
                   const=2, help='Page mode (episode list page).')
    parser.add_argument('-ep', help='''Numbers of episodes to download from page,
                        \trequired to download a page (you will be prompted otherwise.
                        \tcan be specified many times e.g. -ep 12-5 -ep 2; -ep 5-12''')
    parser.add_argument('-q', dest='quality', choices=['worst', '240p', '360p', '480p', '720p', '1080p', 'best'],
                        default='720p', help='''Quality to use on the page.
                        \tIf not available, use any best. Default is 720p''')

    d = parser.add_mutually_exclusive_group()
    d.add_argument('-d', '--download', dest='dmode', action='store_const',
                   const=1, default=1, help='Download the file.')
    d.add_argument('-g', '--link', dest='dmode', action='store_const',
                   const=2, help='Get the link in quiet mode.')
    parser.add_argument('--progress', action='store_const', default=False,
                        const=True, help='Show download progress in download mode.')
    parser.add_argument('-o', '--out', type=str, dest='outfile', default=None,
                        help='''Output file path. Does not overwrite. (downloaded container is MP4)
                        \tDefault: current directory, guessed file name.''')
    parser.add_argument('--chunk-size', type=int, default=2 ** 18,
                        help='''Size of each chunk to download before write.
                        \tMay affect download performance, default 262144,
                        \tworks best with a power of two.''')
    args = parser.parse_args()
    m = args.mode
    try:
        pinfo = jutsu.get_info(args.url)
        m = 1
    except ValueError:
        try:
            eplist = jutsu.get_eps(args.url)
            m = 2
        except:
            raise ValueError("Can't work with this link type")
    if m == 1:
        page = jutsu.Episode(args.url)
        k = sorted(page.urls.keys(), key=(
            lambda a: int(a[:2]) if len(a) > 4 else int(a[:1])))
        if args.quality == 'best':
            url = page.urls[k[-1]]
        elif args.quality == 'worst':
            url = page.urls[k[0]]
        else:
            try:
                url = page.urls[args.quality]
            except KeyError:
                url = page.urls[k[-1]]
        if args.dmode == 2:
            print(url)
            sys.exit(0)
        else:
            outfile = args.outfile if args.outfile else f"{pinfo[0]}_s{pinfo[1]}_e{pinfo[2]}.mp4"
            jutsu.download(url, outfile, progress=args.progress, chunk_size=args.chunk_size)
