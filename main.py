from chat import start
from ollama_interface import ai_message_core
from file_management import get_settings
import argparse

parser = argparse.ArgumentParser(
    prog="Better Ollama CLI",
    description="A better command line interface for Ollama",
)

parser.add_argument(
    "-a",
    "--auto",
    dest="auto",
    metavar="Prompt",
    type=str,
    nargs=1,
    help="Get AI response without user input",
)
parser.add_argument(
    "-m", "--model", dest="model", type=str, nargs=1, help="use instead of saved model"
)
parser.add_argument(
    "-s",
    "--system",
    dest="system",
    type=str,
    nargs=1,
    help="use instead of saved system message",
)

args = parser.parse_args()

if args.model == None:
    model_input = ""
else:
    model_input = args.model[0]

if args.system == None:
    system_message_input = ""
    has_system_input = False
else:
    system_message_input = args.system[0]
    has_system_input = True


if args.auto == None:
    start(model_input, system_message_input)
else:
    default_model, default_system = get_settings()
    if system_message_input == "":
        system_message_input = default_system
    if model_input == "":
        model_input = default_model

    message_input = args.auto[0]

    ai_message_core(
        model=model_input,
        messages=[{"role": "user", "content": message_input}],
        has_system=has_system_input,
        system_message={"role": "system", "content": system_message_input},
    )


