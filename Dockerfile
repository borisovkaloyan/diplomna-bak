FROM python:3.11.9-alpine3.20

WORKDIR /app
COPY dist/pariking_buddy_backend-1.0.1-py3-none-any.whl /app

RUN apk --update --no-cache add make automake gcc g++ subversion python3-dev python3
RUN pip install pariking_buddy_backend-1.0.1-py3-none-any.whl

EXPOSE 8000

CMD ["parking-buddy"]
