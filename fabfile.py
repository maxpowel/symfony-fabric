from fabric.api import env, run
from fabric.context_managers import cd
from fabric.contrib.files import exists

#env.hosts = ['user@host']
env.key_filename = '/Users/maxpowel/.ssh/id_rsa'

projects = {
    "blog": "/var/www/alvaro"
}


def pull():
    with cd(projects["blog"]):
        run('git pull')

def install():
    with cd(projects["blog"]):
        if not exists('composer.phar'):
            install_composer()

        run('php composer.phar install')


def assets():
    with cd(projects["blog"]):
        run("php bin/console assets:install")


def install_composer():
    with cd(projects["blog"]):
        run("php -r \"copy('https://getcomposer.org/installer', 'composer-setup.php');\"")
        run("php -r \"if (hash_file('SHA384', 'composer-setup.php') === '55d6ead61b29c7bdee5cccfb50076874187bd9f21f65d8991d46ec5cc90518f447387fb9f76ebae1fbbacf329e583e30') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;\"")
        run("php composer-setup.php")
        run("php -r \"unlink('composer-setup.php');\"")


def db_prepare(database, user, password):
    run("sudo mysql -e \"CREATE DATABASE IF NOT EXISTS {database};\"".format(database=database))
    run("sudo mysql -e \"CREATE USER '{user}'@'%' IDENTIFIED BY '{password}';\"".format(user=user, password=password))
    run("sudo mysql -e \"GRANT ALL PRIVILEGES ON {database}.* TO '{user}'@'%';\"".format(user=user, database=database))
    run("sudo mysql -e \"FLUSH PRIVILEGES;\"")


def cc(env='prod', debug=False):
    with cd(projects["blog"]):
        run("php bin/console cache:clear --env={env} {debug}".format(env=env,debug="--no-debug" if not debug else "--debug"))

def su(force=False, dump=False):
    with cd(projects["blog"]):
        run("php bin/console doctrine:schema:update {force} {dump}".format(force="--force" if force else "", dump="--dump-sql" if dump else ""))

def permissions():
    with cd(projects["blog"]):
        run("sudo chmod -R 777 var/cache var/log")

def console(command, **kwargs):
    params = " ".join(["--"+"=".join([attr,value]) for attr,value in kwargs.iteritems()])
    print(params)
    with cd(projects["blog"]):
        run("php bin/console {command} {params}".format(command=command, params=params))

def create_user(username, email, password, admin=False):

    with cd(projects["blog"]):
        run("php bin/console fos:user:create {username} {email} {password} {admin}".format(username=username, email=email, password=password, admin="--super-admin" if admin else ""))


