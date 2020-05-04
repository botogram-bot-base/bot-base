from invoke import task
from source.objects.config_parser import Config
from os import path as p


@task
def setup(c):
    print("[+] Welcome to the Bot-Base initial configuration")
    path = input("[?] First of all, where do you want to save your config "
                 "file? [\"./data/configs/config.json\"] "
                 ) or "./data/configs/config.json"

    if p.exists(path):
        while True:
            choice = input("[?] A config file is already present in this path,"
                           " do you want to overwrite it and continue? [y/N] "
                           ) or "n"
            if choice.lower() == "n":
                exit(0)
            elif choice.lower() != "y":
                print("[-] Please input Y or N only (case-insensitive)")
            else:
                break

    config = Config(load_from_json=False)
    config.add_category("telegram")
    # Required Configuration from here
    config.telegram.add_keys({
        "bot-token": input("[?] Insert your Telegram Bot Token: ")})

    config.add_category("redis")

    redis_config = {
        "ip": input("[?] Insert the Redis server IP: [localhost] "
                    ) or "localhost",
        "port": input("[?] Insert the Redis server port: [6379] ") or 6379,
        "database": input("[?] Insert the Redis database to use ("
                          "normally a number from 0 to 15): [0] "
                          ) or 0,
        "password": input("[?] Insert the Redis server password: [] "
                          ) or None
    }
    config.redis.add_keys(redis_config)

    print("[+] Initial configuration done!")

    config.save_to_json(path=path)
    print("[+] You're now ready to use Bot-Base!")
