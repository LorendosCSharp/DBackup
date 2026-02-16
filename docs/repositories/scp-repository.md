## What is SCP?
***SCP*** stands for Secure Copy Protocol. With it you can transfer files from one machine to another with ssh.<br> 
But this tool uses rsync, basicly it is the same thing but in different package. 

## SSH Key
To transfer files with ease and secure, you need to provide a private key to DBackUP and a public key on your host.
### ***How do I obtain those keys?***<br>
You need ***openssh*** installed on your machine.<br>
Then use ```ssh-keygen -t ed25519 -f /path/to/folder/key_name``` (Works on Linux and Windows)<br><br>
You will get two file in the folder you have choosed:

1. `key_name` DBackUp needs it
2. `key_name.pub` Destination machine needs it

### What do I do with those keys?
#### For `key_name.pub`

1. you need to add to end of `authorized_keys` file on the destination machine.
it is located in `~/.ssh/` on Linux

#### For `key_name`

1. You need to copy it to the directory where DBackups `docker-compose.yml` is.
2. Bind it to the container in `volume:` like 
```
volume:
    - key_name:/app/ssh_key
```

## Destination Remotes
***Destination Remote*** the remotes that would recive the backups

You can add them into your `.env` file under `REMOTE_ADDRESSES` variable:
```
REMOTE_ADDRESSES=root@some.random.ip.address:/destination_folder
```
If you want multiple ***Destination Remote***s, you can separate them with comma `,`

