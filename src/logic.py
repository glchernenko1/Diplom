import subprocess
import src.test_model as test_model
from src.downloader import Downloader
import src.test as test
import glob

is_test = True

list_res = ['1080p', '720p', '480p', '360p', '240p', '144p']

def video_resolution_out(resolution):
    if resolution == '144p':
        return list_res[2:4]
    if resolution == '240p':
        return list_res[1:3]
    if resolution == '360p':
        return list_res[:2]
    if resolution == '480p':
        return list_res[:1]
    if resolution == '720p' or resolution == '1080p':
        return list_res[0]

def progress_bar():
    if is_test:
        return 0
    res_count = len(glob.glob('results/*'))
    low_count = len(glob.glob('low_quality/*'))
    if low_count == 0:
        return 0
    return int(res_count / low_count * 100)


def build_video(fps, quality_out):
    process_call_str = 'ffmpeg -r "{0}" -f image2 -i results/img%7d.png -y -an -s "{1}"' \
                       ' -movflags faststart out_video/output.mp4'.format(str(fps), quality_out)
    subprocess.getstatusoutput(process_call_str)

def create_video(url, quality_download, quality_out):
    global is_test
    is_test = True
    model_name = test_model.best_model(url, quality_download)
    is_test = False
    download = Downloader(url)
    fps = download.download_df(quality_download)
    print(model_name)
    test.test_model('models/' + model_name[0])

    build_video(fps, quality_out)


