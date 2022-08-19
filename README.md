# Certificate-Bot

It's a python script that checks for SSL/TLS hosts certificate validity  
If there's a certificate about to expire it will send a slack notification , it will do the same for various other issues like incomplete certificate chain for example

## Info

- This script is meant to be run in scheduled ci/cd pipeline or in cronjob
- There are a few variables that need to be adjusted in the script

**HOSTS** - is list of tuples of ('host', port) pairs, where host is a string and port is an integer

**SLACK_WEBHOOK** - is your slack webhook url

**DAYS_BEFORE_WARNING** - is the days the certificate is still valid for until the bot sends alerts

Also make sure to customize `slack_payload.json.j2` for your environment

## Running the script

- Install the required modules using pip

```shell
python3 -m pip install -r requirements.txt
```

- Run the script after that

```shell
python3 main.py
```

## License

[Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)
