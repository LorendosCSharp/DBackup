## Repository is destination for your files

---

## Types

You can define different types of ***Repositories***.
For that add in `.env` file under `REPOS` an avaliable ***Repository***
```
REPOS=telegram,scp
```
If you want multiple ***Repositories*** you need to separate them with comma `,`


Following ***Repositories*** are avaliable now:

* ### [telegram](telegram-repository.md)
Backups are send as messages containing the files
* ### [scp](scp-repository.md)
Backups are send as files to remote machine