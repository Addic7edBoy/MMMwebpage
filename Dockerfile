FROM python:3.8.7

# RUN adduser --debug max

WORKDIR /home/MMMwebpage

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY app app
COPY migrations migrations
COPY microblog.py config.py boot.sh .env ./
RUN chmod +x boot.sh

ENV FLASK_APP=microblog.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV TEMPLATES_AUTO_RELOAD=True
ENV SPOTIPY_REDIRECT_URI="http://127.0.0.1:5000/usage-confirm"


# RUN chown -R max:max ./
# USER max

EXPOSE 5000
ENTRYPOINT ["/bin/bash", "./boot.sh"]
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "microblog:app"]
