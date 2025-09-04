FROM python:3

RUN apt-get update && apt-get -y install cron

# TODO : via bind: ne pas refaire une image docker à chaque modif de cron
COPY scripts-cron /etc/cron.d/scripts-cron
RUN chmod 0644 /etc/cron.d/scripts-cron
RUN echo "Start of logs" > /var/log/cron.log

WORKDIR /scripts

COPY requirements.txt lib/ *.py config.json ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#CMD ["cron",  "&&", "tail", "-f", "/var/log/cron.log"]
CMD ["cron","-f", "-l", "2"]
