<<<<<<< HEAD
FROM python:3.7-alpine as build
=======
FROM python:3.8.1-alpine as build
>>>>>>> f42cbaa0437a44151c0057aa772fe4273ffd0cd9
WORKDIR /wheels
RUN apk update --no-cache \
  && apk add --no-cache \
    g++=9.2.0-r3 \
    gcc=9.2.0-r3 \
    libxml2=2.9.10-r1 \
    libxml2-dev=2.9.10-r1 \
    libxslt-dev=1.1.34-r0 \
    linux-headers=4.19.36-r0
COPY requirements.txt /opt/h2t/
RUN pip3 wheel -r /opt/h2t/requirements.txt

<<<<<<< HEAD
FROM python:3.7-alpine
=======
FROM python:3.8.1-alpine
>>>>>>> f42cbaa0437a44151c0057aa772fe4273ffd0cd9
WORKDIR /opt/h2t
ARG VCS_REF
ARG VCS_URL="https://github.com/gildasio/h2t"
LABEL org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.vcs-url=$VCS_URL
COPY --from=build /wheels /wheels
COPY . /opt/h2t/
RUN pip3 install -r requirements.txt -f /wheels \
  && rm -rf /wheels \
  && rm -rf /root/.cache/pip/*

ENTRYPOINT ["python", "h2t.py"]
