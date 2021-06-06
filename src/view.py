import logging
import src.video_feed as video_feed
from flask import Response, Blueprint, request, json, render_template
from src.downloader import Downloader
import src.logic as logic
from threading import Thread
import os


api = Blueprint('api', __name__)
log = logging.getLogger(__name__)

video_resolution_out_dict = \
    {'1080p': '1920x1080', '720p': '1280x720', '480p': '854x480', '360p': '640x360', '240p': '426x240'}


@api.route('/video_feed')
def video_feed_endpoint():
    try:
        return video_feed.processing()
    except Exception as e:
        log.exception(e)
        return Response(status=204)


@api.route('/video_resolution_out', methods=["POST"])
def video_resolution_out():
    try:
        return json.dumps(
            {"success": "true", "data": json.dumps(logic.video_resolution_out(request.form['resolution']))})
    except Exception as e:
        log.exception(e)
        return json.dumps({"success": "false", "message": "url не найден"})


@api.route('/video_resolution', methods=["POST"])
def video_resolution():
    try:
        return json.dumps(
            {"success": "true", "data": json.dumps(Downloader(request.form['url']).get_list_resolution())})
    except Exception as e:
        log.exception(e)
        return json.dumps({"success": "false", "message": "url не найден"})


@api.route('/progress_bar')
def progress_bar():
    try:
        return json.dumps({"success": "true", "data": logic.progress_bar()})
    except Exception as e:
        log.exception(e)
        return json.dumps({"success": "false", "message": "????"})


@api.route('/create_video', methods=["POST"])
def create_video():
    try:
        if os.path.exists('out_video/output.mp4'):
            os.remove('out_video/output.mp4')
        url = request.form['url']
        quality_download = request.form['quality_download']
        quality_out = video_resolution_out_dict[request.form['quality_out']]
        Downloader.prepared_path('low_quality')
        Downloader.prepared_path('results')
        Thread(target=logic.create_video, args=(url, quality_download, quality_out,)).start()
        return json.dumps({"success": "true"})
    except Exception as e:
        log.exception(e)
        return json.dumps({"success": "false", "message": "????"})


@api.route('/create_video_is_finish')
def create_video_is_finish():
    try:
        return json.dumps({"is_finish": os.path.exists('out_video/output.mp4')})
    except Exception as e:
        log.exception(e)
        return json.dumps({"success": "false", "message": "False"})
