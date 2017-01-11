#! /user/bin/python
"""
Script to must be run as root - to backup
yum
pip

"""
__author__ = 'Thach_'
import sys
import os
from datetime import date, datetime
import logging
import os
from socket import gethostname
from logging import getLogger, INFO
from log import LoggingSetup

import variables
from subprocess import call
from utils import send_email_notice
LOGGING_DIR = '/opt/logs/'
RECIPIENTS = "tbui@farmobile.com,thachrocky@icloud.com"


hipchat = '''
echo "[atlassian-hipchat]
name=Atlassian Hipchat
baseurl=http://downloads.hipchat.com/linux/yum
enabled=1
gpgcheck=1
gpgkey=https://www.hipchat.com/keys/hipchat-linux.key
" > /etc/yum.repos.d/atlassian-hipchat.repo
'''
google = '''
cat << EOF > /etc/yum.repos.d/google-chrome.repo
[google-chrome]
name=google-chrome - \$basearch
baseurl=http://dl.google.com/linux/chrome/rpm/stable/\$basearch
enabled=1
gpgcheck=1
gpgkey=https://dl-ssl.google.com/linux/linux_signing_key.pub
EOF
'''

log = getLogger('Fedora 24 installed')


class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


class Fedora22(object):
    _desk_file = 'desk.bak'
    _work_file = 'work.bak'

    def __init__(self, desk_install=True):
        self.log_file = ''
        self.setup_logging()
        self.desk = desk_install
        self.rpm_undone = []
        self.yum_undone = []
        self.pip_undone = []
        self.report_message = ''

    def setup_logging(self):
        # set logging directory, create it if it does not exist
        setup_log = LoggingSetup(process_name='Installed_Fed24',
                                 subdirectory='installed_fed24',
                                 daily_file=False,
                                 console_level=INFO,
                                 file_level=INFO)
        setup_log.init_logging()

    @property
    def install_list_desk(self):
        # logging.info("Backup for desk")
        # file_contains = resource_string('backup_fed22', self._desk_file)
        # return literal_eval(file_contains)
        return variables.server

    @property
    def install_list_work(self):
        # logging.info("Backup for desk")
        # file_contains = resource_string('backup_fed22', self._work_file)
        # return literal_eval(file_contains)
        return variables.server

    @property
    def install_list(self):
        if self.desk is False:
            return self.install_list_work
        return self.install_list_desk

    def update(self):
        """
        update before install

        """
        call("yum upgrade -y", shell=True)

    def get_google(self):
        call(google, shell=True)

    def get_qgis(self):
        call("yum copr enable neteler/liblas", shell=True)
        call("yum copr enable neteler/grass70", shell=True)
        call("yum copr enable neteler/QGIS-2.14-Essen", shell=True)
        call("yum install qgis qgis-grass qgis-python -y", shell=True)

    def get_hipchat(self):
        call(hipchat, shell=True)

    def install_rpm(self):
        list_rpm = self.install_list['rpm']
        for row in list_rpm:
            print "rpm {}".format(row)
            rpm = call("rpm {}".format(row), shell=True)
            if str(rpm)[0] != '0':
                logging.info("rpm {} : failed!".format(row))
                self.rpm_undone.append(row)
            logging.info("rpm {} : done!".format(row))

        self.report('rpm', self.rpm_undone)

    def get_queue(self, list_jobs):
        queue_jobs = Queue()
        for job in list_jobs:
            queue_jobs.enqueue(job)
        return queue_jobs
    
    def iterate_install_yum(self, yum_queue):
        """
        This function try to install until it fails twice
        :param yum_queue: 
        :return: remain fails jobs - list
        """
        run_count = 0
        real_count = 0
        size = yum_queue.size()
        while run_count < size * 2:
            if yum_queue.isEmpty():
                break
            package = yum_queue.dequeue()
            run_result = call("yum install {} -y".format(package), shell=True)
            if str(run_result)[0] != '0':
                yum_queue.enqueue(package)  
                print "yum install {} -y : fails - {}".format(package, run_count)
               
            else:
                size = yum_queue.size()  # adjust size and run_count
                run_count -= 2
                if run_count < 0:
                    run_count = 0
                    print "yum install {} -y : done! - {}".format(package, run_count)
            print(real_count)
            run_count += 1
            real_count += 1

        remain = []
        while not yum_queue.isEmpty():
            temp = yum_queue.dequeue()
            remain.append(temp)
        return remain
    
    def report(self, task, undone_jobs):
        self.report_message += "\n--------{}-----------\n".format(task)
        self.report_message += "\nTotal {} packages installed: {}\n".format(task,
                                                                            len(self.install_list[task]))
        self.report_message += "\n"
        self.report_message += "\n ".join(self.install_list[task])
        if len(undone_jobs) > 0:
            self.report_message += "\n--------{}- failed -----------\n".format(task)
            self.report_message += "Total {} packages did not install: {} \n".format(
                task, len(undone_jobs)
            )
            self.report_message += "\n"
            self.report_message += "\n".join(undone_jobs)
        
    
    def install_yum(self):
        """
        install all the yum package first

        """
        yum_jobs = self.install_list['yum']
        yum_queue = self.get_queue(yum_jobs)
        size = yum_queue.size()
        print "Total yum jobs need to install: {}".format(size)
        logging.info("Total yum jobs need to install: {}".format(size))
        
        self.yum_undone = self.iterate_install_yum(yum_queue)
        self.report('yum', self.yum_undone)

    def iterate_install_pip(self, pip_queue):
        """
        This function try to install until it fails twice
        :param pip_queue:
        :return: remain fails jobs - list
        """
        run_count = 0
        real_count = 0
        size = pip_queue.size()
        while run_count < size * 2:
            if pip_queue.isEmpty():
                break
            package = pip_queue.dequeue()
            run_result = call("pip install {} ".format(package), shell=True)
            if str(run_result)[0] != '0':
                pip_queue.enqueue(package)
                print "pip install {} : fails - {}".format(package, run_count)

            else:
                size = pip_queue.size()  # adjust size and run_count
                run_count -= 2
                if run_count < 0:
                    run_count = 0
                    print "pip install {} : done! - {}".format(package, run_count)
            print(real_count)
            run_count += 1
            real_count += 1

        remain = []
        while not pip_queue.isEmpty():
            temp = pip_queue.dequeue()
            remain.append(temp)
        return remain

    def install_pip(self):
        """
        install pip

        """
        pip_jobs = self.install_list['pip']
        pip_queue = self.get_queue(pip_jobs)
        size = pip_queue.size()
        print "Total pip jobs need to install: {}".format(size)
        logging.info("Total pip jobs need to install: {}".format(size))

        self.pip_undone = self.iterate_install_pip(pip_queue)
        self.report('pip', self.pip_undone)

    def report_and_send_message(self):
        """
        Print message and send email

        """
        print self.report_message
        send_email_notice(self.report_message, RECIPIENTS)

    def set_email_active(self):
        call('systemctl status sendmail.service', shell=True)
        call('systemctl restart sendmail.service', shell=True)

    def backup(self):
        self.install_rpm()
        self.update()
        self.get_google()
        # self.get_hipchat()
        self.install_yum()
        self.install_pip()
        self.set_email_active()
        self.report_and_send_message()




if __name__ == '__main__':
    desk = True
    if len(sys.argv) > 2:
        if sys.argv[1].__str__().strip() != 'work':
            print "Backing up desk\n"
            desk = False
    Fedora22(desk).backup()
