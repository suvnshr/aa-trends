FROM ubuntu:24.04

# Copy our cron to cron.d
COPY crontab /etc/cron.d/my-cron

# readable and writable to the owner, but read only to others
RUN chmod 644 /etc/cron.d/my-cron

RUN apt update

# Install curl and cron
RUN apt install -y cron curl

# Run Cron in foreground using -f
ENTRYPOINT cron -f