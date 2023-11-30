FROM python:latest

WORKDIR /app

COPY /app .


RUN pip install -r requirements.txt

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver-linux64.zip https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/119.0.6045.105/linux64/chromedriver-linux64.zip
RUN unzip /tmp/chromedriver-linux64.zip chromedriver-linux64/chromedriver -d /usr/local/bin/
RUN mv /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver

# set display port to avoid crash
ENV DISPLAY=:99

RUN pip install -r requirements.txt

RUN chmod +x ./entrypoint.sh

ENTRYPOINT [ "/app/entrypoint.sh" ]

CMD ["echo", "Default argument from CMD instruction"]