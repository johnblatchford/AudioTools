''' 2017 John Blatchford

Quick tool to remap a multi-channel RF64 wav file from:
 DOLBY SMPTE 5.1 Channel order (L R C LFE Ls Rs)
                to
 ProTools & Film Channel order (L C R Ls Rs LFE)

 Script runs the equivalent to:
 ffmpeg -i in_file.wav -filter 'channelmap=0|2|1|4|5|3:5.1' FILM.wav

'''
import ffmpy3
from wavefile import WaveReader
import os
import sys
import argparse

# If script is run without arguments, display the usage.
usage = "\nusage: Film_to_SMPTE_order.py -i path/to/folder/of/waves/ or /path/to/wav/file.wav\n"
arguments = sys.argv[1:]
if len(arguments) == 0:
    print(usage)
    sys.exit()

# Set up args and the extension of files to process
parser = argparse.ArgumentParser()
parser.add_argument("-i", help="File/Folder for processing")
args = parser.parse_args()
# Initialize variables
item = args.i
wav_ext = '.wav'

# figure out if arg is folder or file
if os.path.isdir(item):
    for file in os.listdir(item):
        if file.endswith(wav_ext):
            # check to see if file is 5.1 or 7.1 for processing
            read_wav = WaveReader(file)
            if read_wav.channels() == 6:
                in_file = os.path.join(item, file)
                out_file = os.path.join(item, file[:-4])
                reorderFolder = ffmpy3.FFmpeg(
                    inputs={in_file: None},
                    # set SMPTE order
                    outputs={out_file + '_SMPTE.wav': "-filter 'channelmap=0|2|1|5|3|4:5.1'"}
                    )
                reorderFolder.run()
            elif read_wav.channels() == 8:
                in_file = os.path.join(item, file)
                out_file = os.path.join(item, file[:-4])
                reorderFolder = ffmpy3.FFmpeg(
                    inputs={in_file: None},
                    # set SMPTE order
                    outputs={out_file + '_SMPTE.wav': "-filter 'channelmap=0|2|1|7|3|4|5|6:7.1'"}
                    )
                reorderFolder.run()

elif os.path.isfile(item):
    read_wav = WaveReader(item)
    if read_wav.channels() == 6:
        reorderFile = ffmpy3.FFmpeg(
            inputs={item: None},
            # set SMPTE order
            outputs={item[:-4] + '_SMPTE.wav': "-filter 'channelmap=0|2|1|5|3|4:5.1'"}
            )
        reorderFile.run()
    elif read_wav.channels() == 8:
        reorderFile = ffmpy3.FFmpeg(
            inputs={item: None},
            # set SMPTE order
            outputs={item[:-4] + '_SMPTE.wav': "-filter 'channelmap=0|2|1|7|3|4|5|6:7.1'"}
        )
        reorderFile.run()