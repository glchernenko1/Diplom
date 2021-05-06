from pytube import YouTube
import os
import subprocess
from threading import Thread


class Downloader(object):
    def __init__(self, url):
        self.url = url
        self.fhd = 137
        self.hd = 22
        self.sd = 18
        self.p240 = 133

    def download_audio(self):
        # m_url = YouTube(url).streams.get_by_itag(fhd).url
        # process_call_str = 'ffmpeg -i "{0}" -vn -acodec copy output-audio.aac'.format(str(m_url))
        # subprocess.getstatusoutput(process_call_str)
        # process_call_str = 'ffmpeg -ss {1} -to {2} -i "{0}"' \
        #                    ' -acodec aac -b:a 192k -avoid_negative_ts make_zero "{3}" -y' \
        #     .format(str(m_url), str(start), str(end), os.getcwd() + "/ds1a1.mp4")
        # status = subprocess.getstatusoutput(process_call_str)[1]
        # index = status.find('Duration')
        # return status[index + 10: index + 21]
        pass  # Todo сделать нормальное скачивание звука

    def df_test(self, n, quality, path):
        m_url = YouTube(self.url).streams.get_by_itag(quality).url
        process_call_str = 'ffmpeg -i "{0}" -vf fps=1/"{1}" "{2}"/img%07d.png -y'.format(str(m_url), str(n), str(path))
        #subprocess.getstatusoutput(process_call_str)
        Thread(target=subprocess.getstatusoutput, args=(process_call_str,)).start()

    def download_df(self, quality, path):
        tmp = str(YouTube(self.url).streams.get_by_itag(quality))
        fps = tmp[tmp.find('fps=') + 5:tmp.find('fps=') + 7]
        m_url = YouTube(self.url).streams.get_by_itag(quality).url
        process_call_str = 'ffmpeg -i "{0}" -vf fps="{1}" "{2}"/img%07d.png -y'.format(str(m_url), fps, str(path))
        subprocess.getstatusoutput(process_call_str)

    def prepared_path(self, path):
        if not os.path.isdir(path):
            os.mkdir(path)
        else:
            files = os.listdir(path)
            for f in files:
                os.remove(path + '/' + f)

    def df_tests(self, n, low_quality=133, height_quality=137):
        low_path, height_path = 'low_quality', 'height_quality'
        self.prepared_path(low_path)
        self.prepared_path(height_path)
        tmp1 = Downloader(self.url)
        tmp2 = Downloader(self.url)
        tmp1.df_test(n, low_quality, low_path)
        tmp2.df_test(n, height_quality, height_path)


#
# video.download_df(video.sd, 'low_quality')
#video.prepared_path('low_quality')
# df_test('https://www.youtube.com/watch?v=MtTvKW4CpnI', 12,  sd, 'low_quality')
# df('https://www.youtube.com/watch?v=MtTvKW4CpnI',  sd, 'low_quality')
# prepared_path('low_quality')
# prepared_path('low_quality')
# ss = "00:01:00"
# t = "00:01:00.01"
#print(YouTube('https://www.youtube.com/watch?v=vAbN2dIdOvE').streams)
video = Downloader('https://www.youtube.com/watch?v=vAbN2dIdOvE')
#
video.df_tests(15)
#video.df_test(15, video.p240, 'height_quality')
#Downloader(video.url).df_test(15, video.fhd, 'height_quality')