FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VIRTUALENVS_CREATE=true
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1

RUN apt update && apt install -y --no-install-recommends curl wget

RUN curl -sL https://deb.nodesource.com/setup_20.x | bash - && apt-get install -y nodejs

RUN  python -m pip install --upgrade pip

RUN useradd -ms /bin/bash python

RUN pip install poetry

USER python

WORKDIR /home/python/app

ENV PYTHONPATH=${PYTHONPATH}/home/python/app
ENV PATH="$PATH:$PYTHONPATH/.venv/bin"


CMD ["tail", "-f", "/dev/null"]