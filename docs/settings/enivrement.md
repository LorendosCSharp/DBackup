| Variable          | Value                                         | Default           | Note
| ----------------- | -----                                         | ----------------- | -----
| ON_EVENTS_BACKUP  | bool                                          | false             | Runs Scan/Backup Generation on every event of Docker (update/start)
| PERIODIC_SCAN     | bool                                          | true              | Runs Scan/Backup Generation every fixed time period
| RUN_TASK          | time                                          | 604800            | Is given in seconds, default 7 days
| REPOS             | [Repository](../repositories/repository.md)   | none              | Type of Repository that would receive the Backups
| TELEGRAM_BOT_TOKEN| int                                           | none              | Telegram Token for a Bot
| TELEGRAM_USER_IDS | list[int]                                     | none              | IDs of user. Separate them with ` , `: user1,user2
| REMOTE_ADDRESSES  | list[str]                                     | none              | Remote Addresses. Separate them with ` , `: user@ip:/location,user2@ip2:/location2