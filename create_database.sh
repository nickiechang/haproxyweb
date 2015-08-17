#RET=`dpkg -l |grep mysql-server*`
#if [ $? -eq 0 ];
#if [ -f "/usr/sbin/mysqld" ];
#then
#    echo 'mysql-server package exists'
#else
#    echo 'mysql-server package not exists'
#	echo "mysql-server mysql-server/root_password password testlab" | sudo debconf-set-selections
#	echo "mysql-server mysql-server/root_password_again password testlab" | sudo debconf-set-selections
#	apt-get -y install mysql-server
#fi

#if [[ ! -z "`mysql -qfsBe "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME='haproxy'" 2>&1`" ]];
#RESULT=$(mysql -N -s -uroot -ptestlab -e "show databases like 'haproxy'")
#RESULT=`mysql -uroot -ptestlab --skip-column-names -e "SHOW DATABASES LIKE 'haproxy'"`
#if [ "$RESULT" = "haproxy" ]; 
#then
#    echo "Database exist"
#else
#    echo "Database not exist"
#    echo "create database haproxy" | mysql -uroot -ptestlab
#fi

sed -i 's/127\.0\.0\.1/0\.0\.0\.0/g' /etc/mysql/my.cnf
mysql -uroot -ptestlab -e 'USE mysql; UPDATE `user` SET `Host`="%" WHERE `User`="root" AND `Host`="localhost"; DELETE FROM `user` WHERE `Host` != "%" AND `User`="root"; FLUSH PRIVILEGES;'

mysql -uroot -ptestlab --skip-column-names -e "CREATE DATABASE IF NOT EXISTS haproxy;"
if [ $(mysql -N -s -uroot -ptestlab -e \
    "select count(*) from information_schema.tables where \
        table_schema='haproxy' and table_name='django_session';") -eq 1 ]; 
then
    echo "Table exist"
else
    echo "Table not exist"
	python /usr/share/haproxyweb/manage.py migrate
	#echo "from django.contrib.auth.models import User; User.objects.create_superuser('root', 'root@example.com', 'testlab')" | python manage.py shell
	#python /usr/share/haproxyweb/manage.py createsuperuser
fi
    
python /usr/share/haproxyweb/manage.py migrate

