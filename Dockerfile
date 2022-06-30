FROM python:3.10.5-alpine3.16 as build

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src src
COPY run.py run.py

FROM python:3.10.5-alpine3.16 as final

WORKDIR /app

COPY --from=build /opt/venv /opt/venv

COPY --from=build /app/src src
COPY --from=build /app/run.py run.py

ENV PATH="/opt/venv/bin:$PATH"

CMD ["python", "run.py"]
