# IC Abroad

## Running the web server

Run the following commands. Make sure that you have poetry installed.

```sh
poetry update
poetry run python icabroad/app.sh
```

The web server should then be running.

## Config file example

Make sure to change it to the correct ones

```yaml
mysql_host: 'localhost'
mysql_user: 'lovedbsomuch'
mysql_password: 'hardpass'
mysql_db: 'icabroad'
```