FROM python:3.11.5-alpine

RUN apk update --no-interactive \
    && apk add git --no-interactive
    # Por supuesto, Alpine tiene problemas de DNS, entonces tenemos que decirle manualmente cuál es la IP de GitHub...
    # Tal vez se rompa en un futuro, desgraciadamente
RUN git -c http.curloptResolve="+github.com:443:140.82.114.3" clone https://github.com/HappyGick/act3compnubeME.git \
    && cd act3compnubeME \
    && pip install -r requirements.txt
WORKDIR /act3compnubeME
COPY ./.env .
ENTRYPOINT [ "fastapi", "run", "main.py" ]