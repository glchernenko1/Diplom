from pytube import YouTube
import os
import subprocess
from threading import Thread


class Downloader(object):
    def __init__(self, url):
        self.url = url
        tmp = YouTube(url).streams
        list_res = ['1080p', '720p', '480p', '360p', '240p', '144p']
        self.youtube_res = dict(zip(list_res, [tmp.filter(res=item).first() for item in list_res]))
        self.len = YouTube(url).length

    def get_list_resolution(self):
        list_res = []
        for key in self.youtube_res.keys():
            if self.youtube_res.get(key) is not None:
                list_res.append(key)
        return list_res

    def get_fps(self):
        tmp = str(self.youtube_res[self.get_list_resolution()[0]])
        return int(tmp[tmp.find('fps=') + 5:tmp.find('fps=') + 7])

    # def download_audio(self):
    #     # m_url = YouTube(url).streams.get_by_itag(fhd).url
    #     # process_call_str = 'ffmpeg -i "{0}" -vn -acodec copy output-audio.aac'.format(str(m_url))
    #     # subprocess.getstatusoutput(process_call_str)
    #     # process_call_str = 'ffmpeg -ss {1} -to {2} -i "{0}"' \
    #     #                    ' -acodec aac -b:a 192k -avoid_negative_ts make_zero "{3}" -y' \
    #     #     .format(str(m_url), str(start), str(end), os.getcwd() + "/ds1a1.mp4")
    #     # status = subprocess.getstatusoutput(process_call_str)[1]
    #     # index = status.find('Duration')
    #     # return status[index + 10: index + 21]
    #     pass  # Todo сделать нормальное скачивание звука

    def df_test(self, n, quality, path):
        return 'ffmpeg -i "{0}" -vf fps=1/"{1}" "{2}"/img%07d.png -y'\
            .format(str(self.youtube_res[quality].url), str(n), str(path))

    def download_df(self, quality, path='low_quality'):
        tmp = str(self.youtube_res[quality])
        fps = tmp[tmp.find('fps=') + 5:tmp.find('fps=') + 7]
        process_call_str = \
            'ffmpeg -i "{0}" -vf fps="{1}" ' \
            '"{2}"/img%07d.png -y'.format(
            str(self.youtube_res[quality].url), fps, str(path))
        subprocess.getstatusoutput(process_call_str)
        return fps

    @staticmethod
    def prepared_path(path):
        if not os.path.isdir(path):
            os.mkdir(path)
        else:
            files = os.listdir(path)
            for f in files:
                os.remove(path + '/' + f)

    def df_tests(self, n, low_quality='240p', height_quality='720p'):
        low_path, height_path = 'low_quality', 'height_quality'
        self.prepared_path(low_path)
        self.prepared_path(height_path)
        Thread(target=subprocess.getstatusoutput,
               args=(self.df_test(n, low_quality, low_path),)).start()
        subprocess.getstatusoutput(self.df_test(n, height_quality, height_path))

