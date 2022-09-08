#!/usr/bin/python
import sys
import re
import os
from collections import OrderedDict
import jutsu
import argparse


# todo:
#  alternative info source (there are other url formats and better sources on the page)
#  film url processing
#  interactive mode
#  ffmpeg interaction
def quality(q, urls):
    k = sorted(urls.keys(), key=(lambda a: int(a[:2]) if len(a) > 4 else int(a[:1])))
    if q == 'best':
        u = urls[k[-1]]
    elif q == 'worst':
        u = urls[k[0]]
    else:
        try:
            u = urls[q]
        except KeyError:
            u = urls[k[-1]]
    return u


def slicer(*rules):
    p1 = re.compile(r'(\d+)-(\d+)')
    for i in rules:
        print(i)
        tr = re.search(p1, i)
        if tr:
            # convert literal range to real range (incl.direction)
            yield range(*(lambda a: [a[0] - 1, a[1], 1 if a[1] >= a[0] else -1])(list(map(int, tr.groups()))))
        else:
            # convert indice to single number range
            try:
                yield range(int(i) - 1, int(i))
            except ValueError:
                raise LookupError  # just an exception it wouldn't normally throw


def eplinteract():
    rules = filter(''.__ne__, input('> ').split())
    try:
        slicer(rules)
    except LookupError:  # specific for wrong input
        print("Wrong range.")
        return eplinteract()
    return rules


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
    parser.add_argument('-ep', action='append', type=str, default=None,
                        help='''Numbers of episodes to download from page,\
 required to download a page (you will be prompted otherwise)
  Can be specified many times e.g. -ep 12-5 -ep 2; -ep 5-12
  numbers are: s2e''')
    parser.add_argument('-q', dest='quality', choices=['worst', '240p', '360p', '480p', '720p', '1080p', 'best'],
                        default='720p',
                        help='Quality to use on the page. If not available, use any best. Default is 720p')

    d = parser.add_mutually_exclusive_group()
    d.add_argument('-d', '--download', dest='dmode', action='store_const',
                   const=1, default=1, help='Download the file.')
    d.add_argument('-g', '--link', dest='dmode', action='store_const',
                   const=2, help='Get the link in quiet mode.')
    parser.add_argument('--progress', action='store_const', default=False,
                        const=True, help='Show download progress in download mode.')
    parser.add_argument('-o', '--out', type=str, dest='outfile', default=None,
                        help='''Output file (directory for Page mode) path. Does not overwrite. (downloaded container is MP4)
  Default: current directory, guessed file name.''')
    parser.add_argument('--chunk-size', type=int, default=2 ** 18,
                        help='''Size of each chunk to download before write.
  May affect download performance, default 262144,
  works best with a power of two.''')
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
        episode = jutsu.Episode(args.url)
        video = quality(args.quality, episode.urls)
        if args.dmode == 2:
            print(video)
            sys.exit(0)
        else:
            outfile = args.outfile if args.outfile else '{}_s{}_e{}.mp4'.format(*pinfo)
            jutsu.download(video, outfile, progress=args.progress, chunk_size=args.chunk_size)
    elif m == 2:
        if args.ep:
            sliced = slicer(*args.ep)
        else:
            print('\n'.join(['{}) S{} EP{}'.format(i + 1,
                                                   *jutsu.get_info(eplist[i])[1:]) for i
                             in range(len(eplist))]) +
                  '\nWhat do you want downloaded? (for example 1-15; 1-15 20-25 17; 2)')
            sliced = slicer(*eplinteract())
            #
            # formatting :)
        epl = [eplist[j] for j in OrderedDict.fromkeys([ii for i in sliced for ii in i])]
        # make list of eps to download
        # dict duplicate removing is slow but preserves order
        # and my time writing a c wrapper :)
        for url in epl:
            episode = jutsu.Episode(url)
            video = quality(args.quality, episode.urls)
            if args.dmode == 2:
                print(video)
                continue
            pinfo = jutsu.get_info(url)
            outfile = os.path.join(args.outfile, '{}_s{}_e{}.mp4'.format(*pinfo)) if args.outfile else \
                '{}_s{}_e{}.mp4'.format(*pinfo)
            jutsu.download(video, outfile, progress=args.progress, chunk_size=args.chunk_size)
