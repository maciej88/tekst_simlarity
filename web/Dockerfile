FROM python:3
WORKDIR /usr/src/app
COPY requirments.txt ./
RUN pip install --no-cache-dir -r requirments.txt
RUN pip install -U spacy
RUN python -m spacy download en_core_web_sm
RUN pip install bcrypt
COPY . .
CMD ["python", "app.py"]