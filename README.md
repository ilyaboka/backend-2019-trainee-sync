# Pitter Sync

### Sync service for Pitter project

For sending emails set EMAIL\_HOST, EMAIL\_PORT, EMAIL\_HOST\_USER, EMAIL\_HOST\_PASSWORD and EMAIL\_USE\_SSL
in local.env file.
If you using gmail enable [less secure app access](https://myaccount.google.com/security).


### Usage

- `make up` - Run in docker-compose
- `make down` - Stop and remove docker-compose services
- `make lint` - Run linter
- `make format` - Run auto-formatter for src/
- `make test` - Run tests
