import src.video_optimization as video_optimization
from flask import Response, request
import os


def _rewind(range_header, size, length):
    byte1, byte2 = 0, None
    if range_header:
        from_bytes, until_bytes = range_header.replace('bytes=', '').split('-')
        if from_bytes:
            byte1 = int(from_bytes)
        if until_bytes:
            byte2 = int(until_bytes)
        length = size - byte1
        if byte2:
            length = byte2 + 1 - byte1
    return byte1, length


def processing(): # file_path: str, file_name: str

    file = open(os.path.join('out_video/output.mp4'), 'rb')
    file = video_optimization.processing(file)
    size = file.seek(0, 2)
    length = size

    range_header = request.headers.get('Range', None)
    byte1, length = _rewind(range_header, size, length)
    file.seek(byte1)

    def generate():
        while True:
            buffer = file.read(204800)
            if not buffer:
                break
            yield buffer

    response = Response(generate(), 206, mimetype="video/mp4", content_type='video/mp4')
    response.headers.add('Content-Encryption', 'disabled')
    response.headers.add('Accept-Ranges', 'bytes')
    response.headers.add('Cache-Control', 'max-age=20480000')
    response.headers.add('Content-Length', length)
    response.headers.add('Content-Range', 'bytes %d-%d/%d' % (byte1, byte1 + length - 1, size))
    response.headers.add('Connection:', 'Upgrade, Keep-Alive')
    response.headers.add('Keep-Alive', 'timeout=15, max=100')
    response.headers.add('Upgrade:', 'h2c')
    return response
