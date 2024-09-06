FROM eclipse-temurin:22

WORKDIR /app

RUN apt-get update && apt-get install -y curl
RUN curl -LO https://github.com/plantuml/plantuml/releases/latest/download/plantuml.jar

ENV RYE_HOME="/opt/rye"
ENV PATH="$RYE_HOME/shims:$PATH"

RUN curl -sSf https://rye.astral.sh/get | RYE_INSTALL_OPTION="--yes" bash

COPY . .
RUN rye sync --no-dev --no-lock

ENTRYPOINT [ "rye", "run", "md2tree" ]
