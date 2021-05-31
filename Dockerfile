FROM python

RUN apt-get update

RUN apt-get install -y ffmpeg

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install torch==1.8.1+cpu torchvision==0.9.1+cpu torchaudio==0.8.1 -f https://download.pytorch.org/whl/torch_stable.html
# todo написать установку cuda
COPY src /src
COPY run.py /
COPY height_quality /height_quality
COPY low_quality /low_quality
COPY models /models
COPY results /results
COPY out_video /out_video
WORKDIR /