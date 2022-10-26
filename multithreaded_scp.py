import paramiko
import os
from scp import SCPClient
import sys

import paramiko
# import multiprocessing
from os import listdir
from os.path import join
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from fnmatch import fnmatch
from multiprocessing import Pool

import threading
import logging
from logging import NullHandler
from tqdm import tqdm

def progress(filename, size, sent):
    sys.stdout.write("%s's progress: %.2f%%   \r" % (filename, float(sent)/float(size)*100) )



class Multicopy():

	def __init__(self, server_ip, username, password, key_filename, dest, thread_no= 0):
		self.server_ip = server_ip
		self.username = username
		self.password = password
		self.key_filename = key_filename

		self.ssh = paramiko.SSHClient()

		self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

		self.ssh.connect(self.server_ip, username=self.username, password=self.password, key_filename=self.key_filename)

		while self.ssh.get_transport().active is False:
			time.sleep(0.1)

		self.scp = SCPClient(self.ssh.get_transport())

		self.dest = dest
		self.thread_no = thread_no




	def start_multicopy(self, files):

		pbar = tqdm(total=len(files), desc='Thread '+ str(self.thread_no) , position=self.thread_no, leave=True)
		for file in files:
			try:
				self.scp.put(file, recursive=False, remote_path=os.path.join(self.dest, file).replace("\\","/"))
			except Exception as e:
				print("Exception Handled in Thread", self.thread_no ," Details of the Exception:", e)
				self.ssh.connect(self.server_ip, username=self.username, password=self.password, key_filename=self.key_filename)
				self.scp = SCPClient(self.ssh.get_transport())
				self.scp.put(file, recursive=False, remote_path=os.path.join(self.dest, file).replace("\\","/"))


			pbar.update()
		pbar.close()





	def execute_command(self, command= 'ls'):
		stdin, stdout, stderr = self.ssh.exec_command(command)
		print(stdout.readlines())


	def close(self):
		self.ssh.close()


	def make_directories(self, src):
		subdirlist = [x[0] for x in os.walk(src)]
		for subdir in subdirlist:
			self.ssh.exec_command("mkdir " + os.path.join(self.dest, subdir).replace("\\","/"))












if __name__ == "__main__":




	src = 'path/to/my_local_upload_directory'				### Set the local directory path that needs to be uploaded
	server_ip = '1.2.3.4'									### Set the IP Address of the server here
	username = "user"										###	Set the RSA verification catchphrase here
	rsa_catchphrase = "rsa_catchphrase"
	rsa_keyfile = 'path/to/my/openssh-private-key-file'		### Set the path of the OpenSSH format RSA private key (don't forget to convert to OpenSSH format first)
	# src = "Recordings"
	dest = '/path/to/destination/directory/on/server'		### Set the destination directory on the server where the folder should be uploaded

	num_parallel = 40										### Set the number of parallel scp copy threads to be launched (more, the faster limited to the bandwidth upload speed)

	filenames=[]
	for path, subdirs, files in os.walk(src):
		for name in files:
			filenames.append(os.path.join(path, name))
	print(len(filenames))
	N = len(filenames)


	K  = int(N/num_parallel)


	threads = list()
	multicopy_engines = []
	multicopy_default = Multicopy(server_ip, username ,rsa_catchphrase, rsa_keyfile, dest)
	multicopy_default.make_directories(src)

	for i in range(num_parallel-1):

			multicopy_engines.append(Multicopy(server_ip, username ,rsa_catchphrase, rsa_keyfile, dest, i))
			x = threading.Thread(target=multicopy_engines[i].start_multicopy, args=([filenames[i*K:(i+1)*K]]))
			threads.append(x)
			x.start()
	i = num_parallel-1		# Last thread done separately
	multicopy_engines.append(Multicopy(server_ip, username ,rsa_catchphrase, rsa_keyfile, dest, i))
	x = threading.Thread(target=multicopy_engines[i].start_multicopy, args=([filenames[i*K:N]]))
	threads.append(x)
	x.start()



	format = "%(asctime)s: %(message)s"
	logging.basicConfig(format=format, level=logging.INFO,
	                    datefmt="%H:%M:%S")


	

	for index, thread in enumerate(threads):
	    logging.info("Main    : before joining thread %d.", index)
	    thread.join()
	    logging.info("Main    : thread %d done", index)
    	# multicopy_engines[i].close()								### Leave this disabled for the time being






