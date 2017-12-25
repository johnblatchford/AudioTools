''' 2017 John Blatchford

Quick tool to remap a multi-channel RF64 wav file from:
 DOLBY SMPTE 5.1 Channel order (L R C LFE Ls Rs)
                to
 ProTools & Film Channel order (L C R Ls Rs LFE)

 Script runs the equivalent to:
 ffmpeg -i in_file.wav -filter 'channelmap=0|2|1|4|5|3:5.1' FILM.wav

'''
import ffmpy
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
item = args.i
wav_ext = '.wav'

#figure out if arg is folder or file
if os.path.isdir(item):
    for file in os.listdir(item):
        if file.endswith(wav_ext):
            in_file = os.path.join(item, file)
            out_file = os.path.join(item, file[:-4])
            ff = ffmpy.FFmpeg(
                inputs={in_file: None},
                outputs={out_file + '_SMPTE.wav': "-filter 'channelmap=0|2|1|5|3|4:5.1'"}
                )
            ff.run()

elif os.path.isfile(item):
    ff = ffmpy.FFmpeg(
        inputs={item: None},
        outputs={item[:-4] + '_SMPTE.wav': "-filter 'channelmap=0|2|1|5|3|4:5.1'"}
        )
    ff.run()