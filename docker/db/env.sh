echo '[client]' > /mysqld_exporter-0.15.1.linux-amd64/.my.cnf && \
echo 'user=$MYSQL_USER' >> /mysqld_exporter-0.15.1.linux-amd64/.my.cnf && \
echo 'password=$MYSQL_PASSWORD' >> /mysqld_exporter-0.15.1.linux-amd64/.my.cnf && \
echo 'host=$MYSQL_HOST' >> /mysqld_exporter-0.15.1.linux-amd64/.my.cnf && \
echo 'port=$MYSQL_PORT' >> /mysqld_exporter-0.15.1.linux-amd64/.my.cnf

cd mysqld_exporter-0.15.1.linux-amd64; ./mysqld_exporter --config.my-cnf=./.my.cnf
