import argparse
import logging
import os
import time

import sentry_sdk
from brownie import network
from cache import cache
from github_push import push_to_repo_branch
from helper_v2 import open, register_all_contracts, unlock_options
from telegram_bot_group_update import send_message as send_tg_message

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


sentry_sdk.init(dsn=os.environ["SENTRY_DSN"])

MAX_KEEPER_HALT_TIME = 120


def monitor_keeper(environment):
    logger.info(f"Monitor Keeper {time.time()}")
    # fetch the checkpoints from the all the keepers
    all_keepers = ["open", "close", "early_close", "cancel", "revoke", "update"]
    for bot_name in all_keepers:
        checkpoint_cache_key = f"{bot_name}_checkpoint"
        last_checkpoint = cache.get(checkpoint_cache_key)
        if not last_checkpoint:
            continue

        now = time.time()
        lag = now - float(last_checkpoint)

        # logger.info(f"Keeper {bot_name} lag: {round(lag/60, 1)} minutes")
        logger.info(f"Keeper {bot_name} lag: {round(lag/60, 2)} min")
        halting_cache_key = f"{bot_name}_halted_1"
        if lag > MAX_KEEPER_HALT_TIME:
            logger.info(f"Keeper {bot_name} lag exceeded 2 minutes")

            # Alarm should be raised
            # Check if we have already raised the alarm
            last_alert_time = cache.get(halting_cache_key)
            if not last_alert_time or (now - float(last_alert_time)) > 3600:
                logger.info(f"Keeper {bot_name} sending alert")
                cache.set(halting_cache_key, time.time(), 3600)
                send_tg_message(
                    f"Keeper Halted:\nChain: {environment}\nName: {bot_name}\nSince: {round(lag/60, 1)} minutes\n\nTrying to Autorecover..."
                )
                push_to_repo_branch(
                    gitHubFileName="README.md",
                    fileName="README.md",
                    repo_slug="Buffer-Finance/Instant-Trading-Backend",
                    branch=os.environ.get("BRANCH", "master-v10"),
                    user="bufferfinance",
                    email="heisenberg@buffer.finance",
                    token=os.environ.get("GITHUB_TOKEN"),
                )
                logger.info(f"Keeper Halted: {environment} {bot_name}, Sending alert")
            else:
                logger.info(
                    f"Keeper already halted: {environment} {bot_name}, Not sending alert"
                )
        else:
            # keeper is working again so delete the alarm cache
            last_alert_time = cache.get(halting_cache_key)
            if last_alert_time:
                logger.info(
                    f"Keeper Recovered:\nChain: {environment}\nName: {bot_name}\n"
                )
                send_tg_message(
                    f"Keeper Recovered:\nChain: {environment}\nName: {bot_name}\n"
                )
                cache.delete(halting_cache_key)


BOT_FUNCTION_MAPPING = {
    "open": open,
    "close": unlock_options,
}
parser = argparse.ArgumentParser(description="Keeper Bots")

parser.add_argument(
    "--bot",
    type=str,
)
environment = os.environ["ENVIRONMENT"]
available_networks = os.environ["NETWORK"].split(",")
current_network_index = 0


def save_checkpoint(bot_name):
    cache_key = f"{bot_name}_checkpoint"
    now = time.time()
    cache.set(cache_key, now)
    logger.info(f"Checkpoint saved for {bot_name}: {now}")


def infinite_loop(bot_name, func):
    def wrapper(*args, **kwargs):
        while True:
            try:
                func(*args, **kwargs)
                save_checkpoint(bot_name)
            except Exception as e:
                if "429" in str(e):
                    logger.info(f"Handled rpc error {e}")
                elif "unsupported block number" in str(e):
                    logger.info(f"Handled rpc error {e}")
                elif "oracle.buffer.finance" in str(e):
                    logger.exception(e)
                else:
                    logger.exception(e)
                time.sleep(int(os.environ["WAIT_TIME"]))
            time.sleep(int(os.environ["DELAY"]))

    return wrapper


def main(bot_name):
    if bot_name == "monitor_keeper":
        infinite_loop(bot_name, monitor_keeper)(environment)
        raise SystemExit(1)
    else:
        if bot_name not in BOT_FUNCTION_MAPPING:
            logger.info(f"Invalid bot name {bot_name}")
            raise ValueError(f"Invalid bot name {bot_name}")
        register_all_contracts(environment)
        # network.connect(available_networks[current_network_index])
        logger.info(f"connected {network.show_active()}")

        logger.info(f"Starting {bot_name}...")
        infinite_loop(bot_name, BOT_FUNCTION_MAPPING[bot_name])(environment)
        logger.info(f"Exiting {bot_name}...")
        raise SystemExit(1)  # Doing this so the process can be restarted by Railway


if __name__ == "__main__":
    args = parser.parse_args()
    main(args.bot)
