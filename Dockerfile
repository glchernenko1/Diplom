FROM  nvidia/cuda:10.2-base

RUN apt-get update &&\
    apt-get install -y python3.8 &&\
    apt-get install -y python3-pip &&\
    apt-get install -y git

RUN apt-get install -y ffmpeg
RUN python3 -m pip install --upgrade pip
COPY requirements.txt .
RUN pip3 install -r requirements.txt
#RUN pip3 install torch==1.8.1+cu102 torchvision==0.9.1+cu102 torchaudio===0.8.1 -f https://download.pytorch.org/whl/torch_stable.html
# todo написать установку cuda
COPY src /src
COPY run.py /
COPY height_quality /height_quality
COPY low_quality /low_quality
COPY models /models
COPY results /results
COPY out_video /out_video
WORKDIR /