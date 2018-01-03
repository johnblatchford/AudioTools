'''
     Quick tool to remap a multi-channel RF64 wav between:
         DOLBY / SMPTE 5.1 Channel order (L R C LFE Ls Rs)
                        &
         ProTools & Film Channel order (L C R Ls Rs LFE)
'''
import ffmpy3
from wavefile import WaveReader
import os

wav_ext = '.wav'
class AudioTools(object):
    """
    Class to setup the input and output files for channel ordering
    """
    def __init__(self, input_file, output_format):
        """
         __init__ generates the input & output files, as well as output format
        :param input_file: file or folder of WAV's
        :param output_format:  -Film or -SMPTE
        """
        if os.path.isdir(input_file):
            self.wav_files = [os.path.join(input_file, f) for f in os.listdir(input_file) if f.endswith(wav_ext)]
        elif os.path.isdir(input_file):
            self.wav_files = [input_file]
        self.output_format = output_format

    def detect(self):
        """
        Will detect if the file is a 5.1 or 7.1
        :return: 6 or 8
        """
        files = self.wav_files
        for filename in files:
            if filename.endswith(wav_ext):
                # check to see if file is 5.1 or 7.1 for processing
                read_wav = WaveReader(filename)
                """
                Will return 6 for a 5.1 or 8 for a 7.1
                """
                return read_wav.channels


    # def smpte_to_film(self):
    #     if self.detect(self.wav_files) == 6:
    #         in_file = os.path.join(item, file)
    #         out_file = os.path.join(item, file[:-4])
    #         reorderFolder = ffmpy3.FFmpeg(
    #             inputs={in_file: None},
    #             # set Film order
    #             outputs={out_file + '_film.wav': "-rf64 auto -filter 'channelmap=0|2|1|4|5|3:5.1'"}
    #         )
    #         reorderFolder.run()
    #
    # elif read_wav.channels == 8:
    # in_file = os.path.join(item, file)
    # out_file = os.path.join(item, file[:-4])
    # reorderFolder = ffmpy3.FFmpeg(
    #     inputs={in_file: None},
    #     # set Film order
    #     outputs={out_file + '_film.wav': "-rf64 auto -filter 'channelmap=0|2|1|4|5|6|7|3:7.1'"}
    # )
    # reorderFolder.run()
    #
    # def film_to_smpte(self):
    #     # TODO write method
    #     return files






