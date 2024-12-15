# monitoring

- close port 5000 from public ips:
iptables -I INPUT -p tcp ! -s 172.18.0.0/16 --dport 5000 -j DROP
