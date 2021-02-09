FROM python:3

ENV PYTHONUNBUFFERED=1
ARG req_file=requirements.txt

RUN apt update

RUN apt install -y make gcc g++ binutils libproj-dev gdal-bin \
    ca-certificates  musl-dev make \
    libffi-dev libcairo2 libglib2.0-dev libpango-1.0-0 \
    libpangocairo-1.0-0


COPY ./requirements.txt requirements.txt

RUN python -m pip install --upgrade pip && \
    pip install --upgrade setuptools && \
    pip install --upgrade --requirement $req_file

COPY --chown=www-data:www-data . code

WORKDIR code
RUN mkdir logs

EXPOSE 8010

COPY docker-entrypoint.sh /docker-entrypoint.sh


#CMD ./wait_for_postgres.py && ./manage.py migrate && \
CMD ./manage.py migrate && \
    ./manage.py collectstatic --noinput && \
    ./manage.py populate_history --auto && \
    gunicorn --bind 0.0.0.0:$PORT --access-logfile - docker_django1_wsgi.py:application
