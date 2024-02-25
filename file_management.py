import readline
import json
import os
from datetime import datetime
from utils import (
    display_title,
    confirm_text,
    filename_input,
    numeric_input,
    featured_input,
)
from ollama_interface import choose_model


def write_settings(model, system_message):
    try:
        if not "settings" in os.listdir():
            os.mkdir("./settings")
        with open("./settings/model", "w") as settings:
            settings.writelines(model)
        with open("./settings/system_message", "w") as settings:
            settings.writelines(system_message)
    except:
        confirm_text("Failed to save settings")


def save_message_log(messages, model, system_message, deafult_save_name=""):
    successfull = False
    while not successfull:
        if deafult_save_name == "":
            deafult_save_name = f"conv_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

        print("Save conversation? Enter 'Discard' to not save.")
        print(f"Default save name is {deafult_save_name}\n")

        conversation_name = filename_input("Conversation name: ")
        if conversation_name == "Discard":
            confirm_text("Conversation not saved")
            return

        if conversation_name == "":
            conversation_name = deafult_save_name
        conversation_dir = "./conversations"
        try:
            if not os.path.exists(conversation_dir):
                os.mkdir(conversation_dir)

            conversation_log_path = os.path.join(
                conversation_dir, f"{conversation_name}.json"
            )

            conversation_log = open(conversation_log_path, "w+")
            data = {
                "messages": messages,
                "model": model,
                "system_message": system_message["content"],
            }

            json.dump(data, conversation_log, indent=4)
            conversation_log.close()

            confirm_text("Saving the conversation was successful")
            successfull = True
        except:
            confirm_text("Saving the conversation failed!")


def get_settings(no_interact=False):
    model = ""
    system_message = ""
    settings_path = "./settings"

    try:
        if not os.path.isdir(settings_path):
            if no_interact:
                return "mistral", ""
            print("Defaults are not set")
            model = choose_model(fallback="mistral")
            system_message = input("System Message: ")
            write_settings(model, system_message)
            return model, system_message

        with open(os.path.join(settings_path, "model"), "r") as settings:
            model = settings.readline().strip()

        with open(os.path.join(settings_path, "system_message"), "r") as settings:
            system_message = "\n".join([line.strip() for line in settings]).strip()

    except FileNotFoundError:
        print("Settings file not found.")
        return "mistral", ""

    except Exception as e:
        confirm_text(f"Setting retrieval failed: {str(e)}")
        return "mistral", ""

    return model, system_message


def load_messages():
    display_title("Load")

    if not "conversations" in os.listdir():
        confirm_text("Missing conversation folder")

        return [], "", "", ""

    list_of_conversations = os.listdir("./conversations/")
    names = []
    index = 0

    for conversation_name in list_of_conversations:
        display = conversation_name.removesuffix(".json")
        if display != conversation_name:
            print(f"[{index}] {display}")
            names.append(display)
            index += 1
    print()
    try:
        choice = numeric_input("Choice Index: ")
        loaded_conversation = json.load(open(f"./conversations/{names[choice]}.json"))

        return (
            loaded_conversation["messages"],
            loaded_conversation["model"],
            loaded_conversation["system_message"],
            names[choice],
        )
    except:
        confirm_text("Invalid Choice")

        return [], "", "", ""


if __name__ == "__main__":
    from utils import wrong_start_script

    wrong_start_script()
