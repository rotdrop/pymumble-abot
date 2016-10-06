#!/usr/bin/env python
"""
TITLE:  abot
AUTHOR: Ranomier (ranomier@fragomat.net)
DESC:   a simple bot that receives sound from a sound device (for me jack audio kit)
"""

import argparse
import sys
from multiprocessing import Process
from time import sleep

from thrd_party import pymumble
import pyaudio
__version__ = "0.0.4"

class MuRunner(object):
    """ TODO """
    def __init__(self, run_dict, args_dict):
        self.run_dict = run_dict
        self.args_dict = args_dict
        self.__join_dicts()
        self.run()

    def __join_dicts(self):
        for name in self.run_dict.keys():
            if name in self.args_dict:
                self.run_dict[name]["args"] = self.args_dict[name]


    def run(self):
        """ TODO """
        for name, cdict in self.run_dict.items():
            print("generating process for:", name)
            self.run_dict[name]["process"] = Process(target=cdict["func"], args=cdict["args"])
            print("starting process for:", name)
            self.run_dict[name]["process"].start()

    def check(self):
        """ TODO """
        print(self.run_dict)




class Audio(object):
    """ TODO """
    def __init__(self, mumble_object, args_dict):
        self.mumble = mumble_object
        self.run_list = {"input": {"func": self.__input_loop, "process": None},
                         "output": {"func": self.__output_loop, "process": None}}
        MuRunner(self.run_list, args_dict)

    def __output_loop(self, periodsize):
        """ TODO """
        return None

    def __input_loop(self, periodsize):
        """ TODO """
        p_in = pyaudio.PyAudio()
        stream = p_in.open(input=True,
                           channels=1,
                           format=pyaudio.paInt16,
                           rate=pymumble.constants.PYMUMBLE_SAMPLERATE,
                           frames_per_buffer=periodsize)
        while True:
            data = stream.read(periodsize)
            if not data:
                print("no data, exiting loop")
                break
            self.mumble.sound_output.add_sound(data)
            print(data)
        stream.close()
        return True

def main():
    """swallows parameter. TODO: move functionality away"""
    parser = argparse.ArgumentParser(description='Alsa input to mumble')
    parser.add_argument("-H", "--host", dest="host", type=str, required=True,
                        help="A hostame of a mumble server")

    parser.add_argument("-u", "--user", dest="user", type=str, required=True,
                        help="Username you wish, Default=abot")

    parser.add_argument("-p", "--password", dest="password", type=str, default="",
                        help="Password if server requires one")

    parser.add_argument("-s", "--setperiodsize", dest="periodsize", type=int, default=256,
                        help="Lower values mean less delay. WARNING:Lower values could be unstable")

    parser.add_argument("-b", "--bandwidth", dest="bandwidth", type=int, default=96000,
                        help="Bandwith of the bot (in bytes/s). Default=96000")

    parser.add_argument("-c", "--certificate", dest="certfile", type=str, default=None,
                        help="Path to an optional openssl certificate file")

    args = parser.parse_args()

    abot = pymumble.Mumble(args.host, args.user, certfile=args.certfile, password=args.password)

    abot.set_application_string("abot (%s)" % __version__)
    abot.set_codec_profile("audio")
    abot.start()
    abot.is_ready()
    abot.set_bandwidth(args.bandwidth)

    Audio(abot, {"output": (args.bandwidth, ), "input": (args.bandwidth, )})
    while True:
        sleep(100)

    #stream = p_in.open(input=True,
    #                   channels=1,
    #                   format=pyaudio.paInt16,
    #                   rate=pymumble.constants.PYMUMBLE_SAMPLERATE,
    #                   frames_per_buffer=args.periodsize)




if __name__ == "__main__":
    sys.exit(main())
