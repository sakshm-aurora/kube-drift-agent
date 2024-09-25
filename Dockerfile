# Dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY agent/ ./agent/

ENV INCLUDE_SECRETS_OPTION=exclude

# Command to run the agent as a module
CMD ["python", "-m", "agent.main"]