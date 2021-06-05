from src.downloader import Downloader
import src.metrics as metrics
from PIL import Image
import src.test as test
import os


def resize_data_frame():
    height_quality_size = Image.open('height_quality/img0000001.png').size
    results_quality_size = Image.open('results/img0000001.png').size
    if results_quality_size[1] == height_quality_size[1]:
        return
    if results_quality_size[1] > height_quality_size[1]:
        files = os.listdir('results')
        for f in files:
            Image.open('results/' + f).resize(height_quality_size, Image.ANTIALIAS).save('results/' + f)
    else:
        files = os.listdir('height_quality')
        for f in files:
            Image.open('height_quality/' + f).resize(results_quality_size, Image.ANTIALIAS).save(
                'height_quality/' + f)


def best_model(url, low_quality):
    download = Downloader(url)
    download.df_tests(10, height_quality=download.get_list_resolution()[0], low_quality=low_quality)
    reslt= {}
    models = os.listdir('models')
    for f in models:
        print(f)
        test.test_model('models/'+f)
        resize_data_frame()
        reslt.update({f: metrics.average_metrics('results', 'height_quality')})
        download.prepared_path('results')
    best = ['none', [-1,1]]
    for key in reslt.keys():
        if best[1][0] < reslt[key][0]:
            best[1] = reslt[key]
            best[0] = key
    return best

