### `/source/`

source file

### in `/cltzz/` directory
  
#### run the app

make sure you have the database file `db.splite3` at local, then do the following:

```
python manage.py makemigrations engine
python manage.py migrate
```

use `python manage.py runserver` to run at local



address|status
---|---
`localhost:xxxx/engine/`| ok
`localhost:xxxx/engine/result`|ok
`localhost:xxxx/engine/detail`| ok