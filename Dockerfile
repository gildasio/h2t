FROM python:3.7-alpine as build
WORKDIR /wheels
RUN apk update --no-cache \
  && apk add --no-cache \
    g++ \
    gcc \
    libxml2 \
    libxml2-dev \
    libxslt-dev \
    linux-headers
COPY requirements.txt /opt/h2t/
RUN pip3 wheel -r /opt/h2t/requirements.txt


FROM python:3.7-alpine
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