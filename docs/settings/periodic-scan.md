### What is it?

***Periodic Scan*** checks files at fixed time intervals and backs up anything that changed since the last scan.

Default time is 7 day (604800 seconds), you can define your own time in `.env` file under `RUN_TASK` variable

```
RUN_TASK=604800
```

You can disable it in same `.env` file under `PERIODIC_SCAN` variable

```
PERIODIC_SCAN=false
```
\(By default it is enabled)
---

### How it works

1. Wait for scan interval
2. Scan directories
3. Backup data
4. Send to repositories

Repeats forever.

---

### Use it when

scheduled backups are enough

---
