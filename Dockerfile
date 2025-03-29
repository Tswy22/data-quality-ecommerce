FROM python:3.13-slim

WORKDIR /streamlit

COPY requirements.txt /streamlit/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /streamlit/

EXPOSE 8501

CMD ["streamlit", "run", "streamlit.py"]