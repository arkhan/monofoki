# Build environment for monofoki: glyph import, ligatures, Nerd Font patch.
# Pinned donor fonts/tools; run via ./build.sh
FROM docker.io/library/debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl unzip git fontconfig \
        fontforge python3-fontforge python3-fonttools \
        fonts-dejavu-core woff2 \
    && rm -rf /var/lib/apt/lists/*

ARG CASCADIA_VERSION=2407.24
ARG FIRA_VERSION=6.2
ARG NERD_FONTS_VERSION=v3.5.1

# Donor fonts and Ligaturizer scripts (LigatureCreator, ligatures.py)
RUN mkdir -p /opt/donors /opt/fira \
    && curl -fsSL -o /tmp/cascadia.zip https://github.com/microsoft/cascadia-code/releases/download/v${CASCADIA_VERSION}/CascadiaCode-${CASCADIA_VERSION}.zip \
    && unzip -q -j /tmp/cascadia.zip 'ttf/static/CascadiaCode-*.ttf' -d /opt/donors \
    && curl -fsSL -o /tmp/fira.zip https://github.com/tonsky/FiraCode/releases/download/${FIRA_VERSION}/Fira_Code_v${FIRA_VERSION}.zip \
    && unzip -q -j /tmp/fira.zip 'ttf/FiraCode-*.ttf' -d /opt/fira \
    && git clone --depth 1 https://github.com/ToxicFrog/Ligaturizer.git /opt/Ligaturizer \
    && mkdir -p /opt/patcher \
    && curl -fsSL -o /tmp/patcher.zip https://github.com/ryanoasis/nerd-fonts/releases/download/${NERD_FONTS_VERSION}/FontPatcher.zip \
    && unzip -q /tmp/patcher.zip -d /opt/patcher \
    && rm /tmp/*.zip

ENV LANG=C.UTF-8 \
    PYTHONIOENCODING=utf-8 \
    CASCADIA_DIR=/opt/donors \
    FIRA_DIR=/opt/fira \
    LIGATURIZER_DIR=/opt/Ligaturizer \
    PATCHER_DIR=/opt/patcher

WORKDIR /work
ENTRYPOINT ["script_helper/build_all.sh"]
