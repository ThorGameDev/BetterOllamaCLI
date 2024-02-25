import readline
from utils import display_title, numeric_input
import ollama


def ai_message(model, messages, has_system, system_message):
    display_title(model)
    ai_message_core(model, messages, has_system, system_message)


def ai_message_core(model, messages, has_system, system_message):
    message = {"role": "assistant", "content": ""}
    try:
        ai_context = messages[:]
        if has_system:
            ai_context.insert(0, system_message)
        stream = ollama.chat(model=model, messages=ai_context, stream=True)

        for chunck in stream:
            content = chunck["message"]["content"]
            print(content, end="", flush=True)
            message["content"] += content
        messages.append(message)
        print()
    except (KeyboardInterrupt, EOFError):
        message["content"] += "<<Message Interrupted>>"
        messages.append(message)
        print("\nMessage Interrupted\n")


def is_ollama_running() -> bool:
    try:
        ollama.list()
        return True
    except:
        return False


def choose_model(fallback: str = "NO_CHOICE_WAS_MADE_ERROR") -> str:
    total_model_list = ollama.list()["models"]
    names = []
    index = 0

    for model_dictionary in total_model_list:
        print(f"[{index}] {model_dictionary['name']}")
        names.append(model_dictionary["name"])
        index += 1
    try:
        model_index = numeric_input("Model Index: ")
        choice_model = names[model_index]

        return choice_model
    except:
        print("invalid choice")
    return fallback


if __name__ == "__main__":
    from utils import wrong_start_script

    wrong_start_script()
