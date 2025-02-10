FROM jasonish/suricata:latest

COPY suricata.yaml /etc/suricata/suricata.yaml

CMD ["-c", "/etc/suricata/suricata.yaml", "-i", "enp0s3"]
