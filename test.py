import threading
from multiping import multi_ping
import os
import argparse

from image2ipv6 import *

ip_address = "2001:4c08:2028:{X}:{Y}:{AA:x}:{BB:x}:{CC:x}"
rows = []
def generate_addresses(size = 16,x_off= 0,y_off = 20):
    addresses = []
    for i in range(x_off,x_off+size):
        for j in range(y_off, y_off+size):
            values = {'X': i,
                      'Y': j,
                      'AA': int((i-x_off)/size * 255),
                      'BB': 0,
                      'CC': int(((j-y_off)/size * 255))}
            addresses.append(ip_address.format(**values))
    return addresses


def get_addresses_from_file(filename):
    with open(filename,'r') as f:
        addresses = [line.replace('\n','') for line in f.readlines()]
    return addresses

def get_frames(foldername):
    for filename in sorted(os.listdir(foldername)):
        yield convert_image(os.path.join(foldername,filename))

def spam_them(threadnum, x_off, y_off, size):
    addresses = generate_addresses(size,x_off,y_off)
    threads = []
    for i in range(threadnum):
        t = threading.Thread(target=multi_ping, args=(addresses, 0.1))
        threads.append(t)
        t.start()


def play_frame(addresses, threadnum):
    threads = []
    for i in range(threadnum):
        t = threading.Thread(target=multi_ping, args=(addresses, 0.1))
        threads.append(t)
        t.start()

def play_movie(input_directory, x_offset=0, y_offset=0, scale='', threadnum=1, repeat=1):
    for filename in sorted(os.listdir(input_directory)):
        frame = convert_image(os.path.join(input_directory, filename), x_offset, y_offset, scale)

        if frame:
            print("sending frame {}".format(filename))
            for i in range(repeat):
                play_frame(frame, threadnum)

def play_movie_interlaced(input_directory, x_offset=0, y_offset=0, scale='', threadnum=1, repeat=1):
    for filename in sorted(os.listdir(input_directory)):
        rows = convert_image_interlaced(os.path.join(input_directory, filename), x_offset, y_offset, scale)
        print("sending frame {}".format(filename))

        for row in rows:
            for i in range(repeat):
                if threadnum == 1:
                    multi_ping(row, 0.1)

                else:
                    threads = []
                    for i in range(threadnum):
                        t = threading.Thread(target=multi_ping, args=(row, 0.1))
                        threads.append(t)
                        t.start()

def play_test(x_offset=0, y_offset=0, scale='', threadnum=1):
    frame = convert_image('test_pattern.png', x_offset, y_offset, scale)

    if frame:
        print("sending test pattern")
        while True:
            play_frame(frame, threadnum)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('-i', '--input', help='Select a directory to get frames from')
    mode.add_argument('-t', '--test', action='store_true', help='Just send a test screen')

    parser.add_argument('-x', '--x_offset', type=int, default=0, help='x offset, 0-160')
    parser.add_argument('-y', '--y_offset', type=int, default=0, help='y offset, 0-120')
    parser.add_argument('-s', '--scale', type=str, default='32x32', help='rescale image')
    parser.add_argument('-n', '--threadnum', type=int, default=10, help='number of threads to use for ping')
    parser.add_argument('-r', '--repeats', type=int, default=10, help='number of times to resend frame')
    parser.add_argument('-I', '--interlaced', action='store_true', help='use interlaced mode')



    args = parser.parse_args()

    if args.test:
        play_test(args.x_offset, args.y_offset, args.scale, args.threadnum)

    elif args.input:

        if args.interlaced:
            play_movie_interlaced(args.input, args.x_offset, args.y_offset, args.scale, args.threadnum, args.repeat)

        else:
            play_movie(args.input, args.x_offset, args.y_offset, args.scale, args.threadnum, args.repeat)