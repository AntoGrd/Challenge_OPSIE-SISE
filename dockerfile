FROM python:3.9

RUN mkdir Streamlit
WORKDIR Streamlit

COPY requirements.txt ./requirements.txt
RUN pip install -U pip
RUN pip install -U wheel
RUN pip install -U setuptools
RUN pip install -r requirements.txt

COPY . .

CMD ["streamlit","run","Accueil.py"]
