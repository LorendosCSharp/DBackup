
### What is it?

***Event Scan*** create backups immediately when container is started or updated

You can enable it in `.env` file under `ON_EVENTS_BACKUP` variable

```
ON_EVENTS_BACKUP=true
```
\(By default it is disabled)


---

### How it works

1. Monitor containers
2. Detect change
3. Backup data
4. Send to configured repositories

Runs continuously.

---

### Use it when

* changes must be backed up instantly
* data is critical or frequently updated

---
