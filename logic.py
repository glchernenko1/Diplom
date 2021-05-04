from downloader import Downloader
import metrics
import test
url = 'https://www.youtube.com/watch?v=vAbN2dIdOvE' #todo получаем откудато url
download = Downloader(url)
download.df_tests(10)
test.test_model()
print(metrics.compare('results', 'height_quality'))