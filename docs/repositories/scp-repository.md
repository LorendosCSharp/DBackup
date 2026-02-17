## What is SCP?
***SCP*** stands for Secure Copy Protocol. With it you can transfer files from one machine to another with ssh.

But this tool uses rsync, basicly it is the same thing but in different package. 

## SSH Key
To transfer files with ease and secure, you need to provide a private key to DBackUp and a public key on your ***Destination Remote***.
### ***How do I obtain those keys?***

* You need ***openssh*** installed on your machine.
* Then use (Works on Linux and Windows): 
```
ssh-keygen -t ed25519 -f /path/to/folder/key_name
``` 

You will get two file in the folder you have choosed:

1. `key_name` DBackUp needs it
2. `key_name.pub` Destination machine needs it

### What do I do with those keys?

#### For `key_name.pub`

1. you need to add to end of `authorized_keys` file on the destination machine.
it is located in `~/.ssh/` on Linux

#### For `key_name`

1. You need to copy it to the directory where DBackUp `docker-compose.yml` is.

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

Every ***Destination Remote*** should have `rsync` installed on them.

* Windows

    * Install WSL 
    ```
    wsl --install
    ```

    * Inside WSL run 
    ```
    sudo apt install rsync
    ```

* Windows (Chocolatey)
```
choco install rsync
```

---

* macOS

    * Install brew
    ``` markdown
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh" 
    ```

    * Run 
    ```
    brew install rsync
    ```

---

* Debian / Ubuntu
```
sudo apt update
sudo apt install rsync
```

---

* Alpine
```
sudo apk add rsync
```