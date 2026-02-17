# DBackUp small tool to backup your Docker containers


[Docs](gh pages site is generating)

## Example docker-compose.yml
``` 
    version: "3.9"

    services:
        dbackup:
            build: lorendos:dbackup:v1.0
            container_name: DBackup
            volumes:
            - /var/run/docker.sock:/var/run/docker.sock
            - ./work:/app/work
            - ./ssh_key:/app/ssh_key
            labels:
            - dbackup.runner=this
            restart: no

            env_file:
            - .env

        postgres:
            image: postgres:16
            environment:
            POSTGRES_PASSWORD: example
            labels:
            - dbackup.on=true
            - mytool.type="postgres"
            volumes:
            - pgdata:/var/lib/postgresql/data

        sqlite:
            image: alpine
            command: ["sh", "-c", "sleep infinity"]
            labels:
            - dbackup.on=true
            - mytool.type="sqlite"
            volumes:
            - ./sqlite-data:/data

        volumes:
            pgdata:

```

### Requirements
>***Note: Currently works only with docker compose***

* Every docker container you want to backup, you need to mark with label 
```
- dbackup.on=true
```

* The container that is ***DBackUp***, you need to mark with label
```
- dbackup.runner=this
```

* If you want to use copy over ssh, you need to provide a ssh_key, see [SCP Repository](https://github.com/LorendosCSharp/DBackup/blob/main/docs/repositories/scp-repository.md).

## Example .env
```
ON_EVENTS_BACKUP=true
PERIODIC_SCAN=true

REPOS=telegram,scp

TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_USER_IDS=user_id,user_id2

REMOTE_ADDRESSES=root@some.random.ip.address:/destination_folder,root@some.other.ip.address:/destination_folder2
```

