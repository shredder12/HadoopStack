import paramiko
import socket
import subprocess
import random

from time import sleep



from hadoopstack.services.make_config_parser import configParserHelper

def ssh_check(instance_ip, key_location):
    '''
    Check if the ssh is up and running
    '''

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    while(True):
        try:
            ssh.connect(hostname=instance_ip,
                        username="ubuntu",
                        key_filename=key_location)
        
        except socket.error, (value, message):
            if value == 113 or 111:
                print "checking for ssh..."
                sleep(1)
                continue
            else:
                print "socket.error: [Errno", value, "]", message

        except paramiko.SSHException:
            print "paramiko.error: connection refused. Discarding instance"
            return False
        
        return True

def configure_master(private_ip_address, key_location, job_name):

    if not ssh_check(private_ip_address, key_location):
        print "Unable to ssh into master{0}. Aborting!!!".format(private_ip_address)
        return False

    subprocess.call(("knife bootstrap {0} -x ubuntu -i {1} \
        -N {2}-master --sudo -r 'recipe[hadoopstack::master]' \
        --no-host-key-verify".format(private_ip_address,
         key_location, job_name)).split())

    return True

def configure_slave(private_ip_address, key_location, job_name):

    if not ssh_check(private_ip_address, key_location):
        print "Unable to ssh into node {0}. Skipping it".format(private_ip_address)
        return False

    subprocess.call((
        "knife bootstrap {0} -x ubuntu -i {1} \
        -N {2}-slave-{3} --sudo -r 'recipe[hadoopstack::slave]' \
        --no-host-key-verify".format(private_ip_address,
            key_location,
            job_name,
            str(random.random()).split('.')[1])
        ).split()
    )

    return True

def configure_cluster(data):
    '''
    Configure Hadoop on the cluster using Chef

    '''

    job_name = data['job']['name']
    key_location = configParserHelper().get("commonConfig","DEFAULT_KEY_LOCATION") + "/hadoopstack-" + job_name + ".pem"
 
    for node in data['job']['nodes']:

        if node['role'] == 'master':
            if not configure_master(node['private_ip_address'], key_location, job_name):
                return False

        elif node['role'] == 'slave':
            configure_slave(node['private_ip_address'], key_location, job_name)

    return True