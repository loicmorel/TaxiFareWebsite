
# write some code to build your image
FROM python:3.8.13-buster

WORKDIR /package

COPY requirements.txt /package/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY app.py /package/app.py
COPY config.py /package/config.py
COPY setup.py /package/setup.py
COPY setup.sh /package/setup.sh

CMD sh setup.sh && streamlit run app.py
