#スクレイピング用Pythonコンテナ

FROM alpine
MAINTAINER A-tak

RUN apk update
RUN apk add python3
RUN pip3 install requests
RUN pip3 install beautifulsoup4
ADD scraping_test.py .
ADD result.py .
RUN chmod 755 scraping_test.py
CMD ["/scraping_test.py"]
