FROM python:3.9

RUN apt-get update &&\
apt-get install -yq libavdevice-dev libavfilter-dev libopus-dev libvpx-dev pkg-config libsrtp2-dev -y
WORKDIR /var/www/5scontrol
COPY req-serv.txt .
RUN pip install -r req-serv.txt
RUN pip install "opencv-python-headless<4.3"

COPY . .

EXPOSE 8050

RUN mkdir -p /usr/src/app

ADD entrypoint.sh /usr/src/app/

RUN ["chmod", "+x", "/usr/src/app/entrypoint.sh"]

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]