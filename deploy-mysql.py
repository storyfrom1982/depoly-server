import os
import sys
import pexpect
import socket

#mysql -u zhhelper -p -h 10.3.4.158
#ERROR 2003 (HY000): Can't connect to MySQL server on '10.3.4.158:3306' (111)
#vim /etc/mysql/mysql.conf.d/mysqld.cnf
#systemctl restart mysql
#https://stackoverflow.com/questions/1673530/error-2003-hy000-cant-connect-to-mysql-server-on-127-0-0-1-111
#https://newbedev.com/remote-connect-to-mysql-aws-lightsail

#mysql -uroot -pJianchi*8 -e "DROP USER zhhelper@127.0.0.1"
#mysql -uroot -pJianchi*8 -e "DROP DATABASE zhhelper"

#In MySQL, what does this mean? /*!40100 DEFAULT CHARACTER SET latin1 */
#https://stackoverflow.com/questions/9298368/in-mysql-what-does-this-mean-40100-default-character-set-latin1

#hostname -I

#https://stackoverflow.com/questions/33470753/create-mysql-database-and-user-in-bash-script

#https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04
#https://docs.rackspace.com/support/how-to/mysql-connect-to-your-database-remotely/


def install_mysql():
    os.system('systemctl stop mysql')
    os.system('apt-get -y purge mysql-server mysql-client mysql-common mysql-server-core-* mysql-client-core-*')
    os.system('rm -rf /etc/mysql /var/lib/mysql')
    os.system('apt -y autoremove')
    os.system('apt -y autoclean')

    os.system("apt update")
    os.system("apt install -y mysql-server libmysqlcppconn-dev")


def configure_mysql(password):
    info1 = r'Press y|Y for Yes, any other key for No:'
    info2 = r'Please enter 0 = LOW, 1 = MEDIUM and 2 = STRONG:'
    info3 = r'New password:'
    info4 = r'Re-enter new password:'
    info5 = r'Do you wish to continue with the password provided(.*?)'
    info6 = r'#'
    # info7 = r'(.*?)sudo(.*?)'

    child = pexpect.spawn('mysql_secure_installation')
    child.logfile = sys.stdout.buffer

    while True:
        i = child.expect([pexpect.TIMEOUT, info1, info2, info3, info4, info5, info6, pexpect.EOF])
        if i == 0:
            print('Timeout!')
            print(child.before, child.after)
            break
        elif i == 1:
            child.sendline(r'Y')
        elif i == 2:
            child.sendline(r'2')
        elif i == 3 or i == 4:
            child.sendline(password)
        elif i == 5:
            child.sendline(r'Y')
        elif i == 6:
            child.sendline(r'Y')
        else:
            break


def create_db(db, pw, host):
    dbname = db
    password = pw
    cmd = 'mysql -uroot -p' + password + ' -e "CREATE DATABASE ' + dbname + '/*\!40100 DEFAULT CHARACTER SET utf8 */;"'
    print(cmd)
    os.system(cmd)
    cmd = 'mysql -uroot -p' + password + ' -e "CREATE USER ' + dbname + '@' + host + ' IDENTIFIED BY \'' + password + '\';"'
    print(cmd)
    os.system(cmd)
    cmd = 'mysql -uroot -p' + password + ' -e "GRANT ALL PRIVILEGES ON ' + dbname + '.* TO ' + dbname + '@' + host + ';"'
    print(cmd)
    os.system(cmd)
    cmd = 'mysql -uroot -p' + password + ' -e "FLUSH PRIVILEGES;"'
    print(cmd)
    os.system(cmd)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("python3 deploy-mysql.py dbname password")
        exit(0)

    install_mysql()
    configure_mysql(sys.argv[2])
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print(s.getsockname()[0])
    create_db(sys.argv[1], sys.argv[2], s.getsockname()[0])
    s.close()
