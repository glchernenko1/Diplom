from pytube import YouTube
import os
import subprocess
from threading import Thread
import glob

fhd = 137
hd = 22
sd = 18


def dowload(url, start, end, quality):
    m_url = YouTube(url).streams.get_by_itag(quality).url
    process_call_str = 'ffmpeg -ss {1} -to {2} -i "{0}"' \
                       ' -acodec aac -b:a 192k -avoid_negative_ts make_zero "{3}" -y' \
        .format(str(m_url), str(start), str(end), os.getcwd() + "/ds1a1.mp4")
    status = subprocess.getstatusoutput(process_call_str)[1]
    index = status.find('Duration')
    return status[index + 10: index + 21]


def df_test(url, n, quality, path):
    m_url = YouTube(url).streams.get_by_itag(quality).url
    process_call_str = 'ffmpeg -i "{0}" -vf fps=1/"{1}" "{2}"/img%07d.png -y'.format(str(m_url), str(n), str(path))
    subprocess.getstatusoutput(process_call_str)


def prepared_path(path):
    if not os.path.isdir(path):
        os.mkdir(path)
    else:
        files = glob.glob('/' + path)
        for f in files:
            os.remove(f)


def df_tests(url, n, low_quality=sd, height_quality=fhd):
    low_path, height_path = 'low_quality', 'height_quality'
    prepared_path(low_path)
    prepared_path(height_path)
    th_low = Thread(target=df_test(url, n, low_quality, low_path))
    th_height = Thread(target=df_test(url, n, height_quality, height_path))
    th_height.start()
    th_low.start()


df_tests('https://www.youtube.com/watch?v=ES8yryhGjaQurl', 30)

print(YouTube("https://www.youtube.com/watch?v=ES8yryhGjaQurl").streams)
ss = "00:01:00"
t = "00:01:00.01"
