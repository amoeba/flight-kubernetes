FROM ubuntu:22.04

WORKDIR /work

ARG BUILD_PRESET=debug
ARG PARALLELISM=8

RUN \
    --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install -y --reinstall ca-certificates && \
    update-ca-certificates && \
    apt-get -y --no-install-recommends install \
    build-essential \
    cmake \
    ccache \
    git \
    libssl-dev \
    wget \
    flex \
    bison \
    zlib1g-dev

# Install perf
RUN wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.15.78.tar.gz
RUN tar xzf linux-5.15.78.tar.gz
WORKDIR /work/linux-5.15.78/tools/perf
RUN make && mv perf /work/
WORKDIR /work

# Set up Arrow build
ADD src src

RUN cmake --preset ${BUILD_PRESET} ./src && \
    cmake --build ./src/build/${BUILD_PRESET} --parallel $PARALLELISM && \
    mv ./src/build/${BUILD_PRESET}/server ./server

ENV LD_LIBRARY_PATH=/usr/local/lib

EXPOSE 8815/tcp

ENTRYPOINT [ "./server", "8815"]
