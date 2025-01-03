FROM python:3.11.9

ARG API_KEY

ENV OPENAI_API_KEY=${API_KEY}

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "screening_fiches_PEP_user_interface.py", "--server.port=8501"]