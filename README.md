# Multithreaded-SCP-Python-for-Lightspeed-Cloud-Upload

While working on cloud deep learning projects, ever wished that you could directly copy large datasets of GBs in size directly from your local disk to the Virtual Machine on the cloud?

The conventional tools such as SCP, SFTP work great but when run in one thread, can give you quite low data transfer speed, much lower than what your internet bandwidth upload speed permits.

This tool is useful to run SCP in multiple threads in a python program which can boost your data transfer speed by multiple times. You can launch as many threads as your CPU cores permit and acheive
the speed up to the maximum allowed by your ISP's bandwidth provided.


# Requirements
paramiko

scp

threading

logging

tqdm

# Parameters to set in the file

	src = 'path/to/my_local_upload_directory'				### Set the local directory path that needs to be uploaded
	server_ip = '1.2.3.4'							### Set the IP Address of the server here
	username = "user"							###	Set the RSA verification catchphrase here
	rsa_catchphrase = "rsa_catchphrase"
	rsa_keyfile = 'path/to/my/openssh-private-key-file'			### Set the path of the OpenSSH format RSA private key (don't forget to convert to OpenSSH format first)
	# src = "Recordings"
	dest = '/path/to/destination/directory/on/server'			### Set the destination directory on the server where the folder should be uploaded

	num_parallel = 40							### Set the number of parallel scp copy threads to be launched (more, the faster 											limited to the bandwidth upload speed)

