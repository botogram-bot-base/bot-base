FROM python:3.8-alpine as base
RUN mkdir /code
WORKDIR /code

FROM base as builder
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install --prefix=/install -r /requirements.txt

FROM base
COPY --from=builder /install /usr/local
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY ./ /code/

SHELL ["sh"]
CMD ["python", "start.py"]