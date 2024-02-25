import readline
from utils import display_title, featured_input, clear, confirm_text, numeric_input
import file_management
import ollama_interface


class Conversation:
    def __init__(self, model: str, init_messages: list, system_message) -> None:
        self.messages = init_messages
        self.has_system = system_message != ""
        self.system_message = {"role": "system", "content": system_message}
        self.model = model

    def ai_message(self) -> None:
        ollama_interface.ai_message(
            self.model, self.messages, self.has_system, self.system_message
        )

    def render_chat(self) -> None:
        clear()
        if self.has_system:
            display_title("System Message")
            print(self.system_message["content"])
        for message in self.messages:
            if message["role"] == "user":
                display_title("User")
            elif message["role"] == "assistant":
                display_title(self.model)
            print(message["content"])

    def command(self, command_text: str) -> None:
        display_title("Command")

        if command_text == "/help" or command_text == "/?":
            print("/help   Display this menu")
            print("/bye    Leave chat")
            print("/exit   Leave chat without saving")
            print("/redo   Force the AI to redo message")
            print("/fix    Change your previous message")
            print("/switch Change the AI model mid conversation")
            print("/system Change the system message")
        elif command_text == "/redo":
            self.messages = self.messages[:-1]
            self.render_chat()
            self.ai_message()
        elif command_text == "/fix":
            self.messages = self.messages[:-2]
            self.render_chat()
        elif command_text == "/switch":
            selected_model = ollama_interface.choose_model(self.model)
            if selected_model == self.model:
                confirm_text("No model change occurred.")
            self.model = selected_model
        elif command_text == "/system":
            new_system_message = featured_input("System Message: ")
            self.system_message["content"] = new_system_message
            self.has_system = new_system_message != ""

    def main(self) -> None:
        self.render_chat()

        while True:
            display_title("User")
            content_in = featured_input(">>> ")

            if content_in == "":
                continue
            elif content_in[0] != "/":
                self.messages.append({"role": "user", "content": content_in})
                self.render_chat()
                self.ai_message()
            elif content_in == "/bye":
                return
            elif content_in == "/exit":
                self.messages = []
                return
            else:
                self.command(content_in)


def start_conversation(messages, model, system_message, savename="") -> None:
    current_conversation = Conversation(model, messages[::], system_message)
    # Actual conversation
    try:
        current_conversation.main()
    except (KeyboardInterrupt, EOFError):
        confirm_text("Conversation Interrupted")
    except:
        confirm_text("Conversation quit unexpectedly")

    # Save

    if len(current_conversation.messages) == 0:
        return
    if current_conversation.messages == messages:
        return

    file_management.save_message_log(
        current_conversation.messages,
        current_conversation.model,
        current_conversation.system_message,
        savename,
    )


def main_loop(model, system_message):
    while True:
        clear()
        display_title("Options")
        print("1. Begin conversation")
        print("2. Load old conversation")
        print("3. Load old conversation with current model and system")
        print(f"4. Change model from {model}")
        print(f"5. Change system message")
        if system_message != "":
            print('   System message:\n   """')
            for line in system_message.split("\n"):
                print(f"      {line}")
            print('   """')
        print("6. Quit")
        print()
        choice = numeric_input("Choice: ")

        if choice == 1:
            start_conversation([], model, system_message)
        elif choice == 2:
            conv_messages, _model, _system, name = file_management.load_messages()
            if conv_messages != []:
                start_conversation(conv_messages, _model, _system, name)
        elif choice == 3:
            conv_messages, nill, nill, name = file_management.load_messages()
            if conv_messages != []:
                start_conversation(conv_messages, model, system_message, name)
        elif choice == 4:
            selected_model = ollama_interface.choose_model(model)
            if selected_model == model:
                confirm_text("No model change occurred.")
            model = selected_model
            file_management.write_settings(model, system_message)
        elif choice == 5:
            system_message = featured_input("System Message: ")
            file_management.write_settings(model, system_message)
        elif choice == 6:
            return


def start(model="", system_message=""):
    if not ollama_interface.is_ollama_running():
        print("Ollama is not running. please create process with 'ollama start'")
        return
    new_model, new_system_message = file_management.get_settings()
    if model == "":
        model = new_model
    if system_message == "":
        system_message = new_system_message
    try:
        main_loop(model, system_message)
        clear()
    except:
        clear()
        print("Main loop quit unexpectedly.")


if __name__ == "__main__":
    from utils import wrong_start_script

    wrong_start_script()
