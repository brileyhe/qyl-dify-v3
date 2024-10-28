# base image
FROM python:3.10-slim-bookworm AS base

WORKDIR /app/racio

# Install Poetry
ENV POETRY_VERSION=1.8.3

# if you located in China, you can use aliyun mirror to speed up
# RUN pip install --no-cache-dir poetry==${POETRY_VERSION} -i https://mirrors.aliyun.com/pypi/simple/

RUN pip install --no-cache-dir poetry==${POETRY_VERSION}

# Configure Poetry
ENV POETRY_CACHE_DIR=/tmp/poetry_cache
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_VIRTUALENVS_CREATE=true
ENV POETRY_REQUESTS_TIMEOUT=15

FROM base AS packages

# if you located in China, you can use aliyun or ustc mirror to speed up
RUN sed -i 's@deb.debian.org@mirrors.aliyun.com@g' /etc/apt/sources.list.d/debian.sources
# RUN sed -i 's@deb.debian.org@mirrors.ustc.edu.cn@g' /etc/apt/sources.list.d/debian.sources

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc g++ libc-dev libffi-dev libgmp-dev libmpfr-dev libmpc-dev

# Install Python dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install --sync --no-cache --no-root

# COPY requirements.txt /requirements.txt

# RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
# RUN --mount=type=cache,target=/root/.cache/pip \
#     pip install --prefix=/pkg -r requirements.txt

# production stage
FROM base AS production

ENV FLASK_APP app.py
ENV DEPLOY_ENV PRODUCTION

EXPOSE 5003

# set timezone
ENV TZ UTC

WORKDIR /app/racio


# if you located in China, you can use aliyun or ustc mirror to speed up
RUN sed -i 's@deb.debian.org@mirrors.aliyun.com@g' /etc/apt/sources.list.d/debian.sources
# RUN sed -i 's@deb.debian.org@mirrors.ustc.edu.cn@g' /etc/apt/sources.list.d/debian.sources

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl wget vim nodejs ffmpeg libgmp-dev libmpfr-dev libmpc-dev \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# COPY --from=packages /pkg /usr/local

# Copy Python environment and packages
ENV VIRTUAL_ENV=/app/racio/.venv
COPY --from=packages ${VIRTUAL_ENV} ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# Copy source code
COPY . /app/racio/

# Copy entrypoint
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ARG COMMIT_SHA
ENV COMMIT_SHA ${COMMIT_SHA}

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]