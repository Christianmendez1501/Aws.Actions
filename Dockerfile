FROM python
WORKDIR /
COPY app.py ./
COPY . .
EXPOSE 8080
CMD [ "python", "app.py" ]