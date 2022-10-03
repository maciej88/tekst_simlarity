FROM python:3
WORKDIR /usr/src/app
COPY requirments.txt ./
RUN pip install --no-cache-dir -r requirments.txt && \
    python -m spacy download en_core_news_sm && \
    python -m spacy link en_core_news_sm es
COPY . .
CMD ["python", "app.py"]