import test_model
import test
from downloader import Downloader
import subprocess

def create_video(url, quality):
    model_name = test_model.best_model(url, quality)
    download = Downloader(url)
    fps = download.download_df(quality)
    print(model_name)
    test.test_model('models/' + model_name[0])
    process_call_str = 'ffmpeg -i'

create_video('https://www.youtube.com/watch?v=fB-LPJDFDl8', '360p')