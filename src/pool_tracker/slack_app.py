import os
from mongoengine.errors import NotUniqueError
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from pool_tracker.Player import Player
from pool_tracker.utils import connect_db, inactivate_player
import logging


logger = logging.getLogger(__name__)

if not os.environ.get("SLACK_BOT_TOKEN", None):
    raise Exception(f"no token: {os.environ.get("SLACK_BOT_TOKEN")}")

if not os.environ.get("SLACK_APP_TOKEN", None):
    raise Exception(f"no token, app: {os.environ.get("SLACK_BOT_TOKEN")}")

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

connect_db()

# Listens to incoming messages that contain "hello"
@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click",
                },
            }
        ],
        text=f"Hey there <@{message['user']}>!",
    )


@app.action("button_click")
def action_button_click(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"<@{body['user']['id']}> clicked the button")

@app.command("/add-me")
def add_player(ack, say, command):
    ack()
    name = command['user_name']
    player = None
    try:
        player = Player(name=name).save()
    except NotUniqueError:
        player = Player.objects(name=name).first()
        player.active = True
        player.save()
    message = f"Your user name is {player.name} and your current score is {player.elo}"
    say(message)

@app.command("/delete-me")
def inactivate_player_slack(ack, say, command):
    ack()
    name = command['user_name']
    player = inactivate_player(name)
    message = f"Successfully made {player.name} inactive"
    say(message)

def start_app():
    logger.info(f"slack bot token: {os.environ.get("SLACK_BOT_TOKEN")}")
    logger.info(f"slack bot token: {os.environ.get("SLACK_APP_TOKEN")}")
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()

# Start your app
if __name__ == "__main__":
    start_app()