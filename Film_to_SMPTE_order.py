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
from argparse import RawTextHelpFormatter
import os
import argparse

# Set up args and the extension of files to process/
parser = argparse.ArgumentParser(description=("Remap a multi-channel RF64 wav file from:\n\n"
                                             "\t\tDOLBY SMPTE 5.1 Channel order (L R C LFE Ls Rs)\n"
                                             "\t\t\t\tto\n"
                                             "\t\tProTools & Film Channel order (L C R Ls Rs LFE)\n"),
                                 formatter_class=RawTextHelpFormatter)
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
            read_wav = WaveReader(os.path.join(item, file))
            if read_wav.channels == 6:
                in_file = os.path.join(item, file)
                out_file = os.path.join(item, file[:-4])
                reorderFolder = ffmpy3.FFmpeg(
                    inputs={in_file: None},
                    # set Film order
                    outputs={out_file + '_film.wav': "-rf64 auto -filter "
                                                     "'channelmap=FL-FL|FR-FC|FC-FR|LFE-SR|SL-LFE|SR-SL'"}
                    )
                reorderFolder.run()
            elif read_wav.channels == 8:
                in_file = os.path.join(item, file)
                out_file = os.path.join(item, file[:-4])
                reorderFolder = ffmpy3.FFmpeg(
                    inputs={in_file: None},
                    # set Film order
                    outputs={out_file + '_film.wav': "-rf64 auto -filter "
                                                     "'channelmap=FL-FL|FR-FC|FC-FR|LFE-BR|SL-LFE|SR-SL|BL-SR|BR-BL'"}
                    )
                reorderFolder.run()

elif os.path.isfile(item):
    read_wav = WaveReader(item)
    if read_wav.channels == 6:
        reorderFile = ffmpy3.FFmpeg(
            inputs={item: None},
            # set Film order
            outputs={item[:-4] + '_film.wav': "-rf64 auto -filter "
                                              "'channelmap=FL-FL|FR-FC|FC-FR|LFE-SR|SL-LFE|SR-SL'"}
            )
        reorderFile.run()
    elif read_wav.channels == 8:
        reorderFile = ffmpy3.FFmpeg(
            inputs={item: None},
            # set Film order
            outputs={item[:-4] + '_film.wav': "-rf64 auto -filter "
                                              "'channelmap=FL-FL|FR-FC|FC-FR|LFE-BR|SL-LFE|SR-SL|BL-SR|BR-BL'"}
            )
        reorderFile.run()
