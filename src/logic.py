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
    process_call_str = 'ffmpeg -r "{0}" -f image2 -i results/img%7d.png -y -an  -movflags faststart output.mp4'.format(str(fps))
    subprocess.getstatusoutput(process_call_str)

create_video('https://www.youtube.com/watch?v=fB-LPJDFDl8', '480p')