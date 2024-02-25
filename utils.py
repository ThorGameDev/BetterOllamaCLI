import readline
import os


def display_title(words: str) -> None:
    print(f"\n~~~~~~~~~~~~~~~~~~~~  {words}  ~~~~~~~~~~~~~~~~~~~~\n")


def featured_input(prompt: str) -> str:
    output = input(prompt)
    if output.removeprefix('"""') != output:
        output = output.removeprefix('"""')
        output += "\n"
        while True:
            try:
                line = input("... ")
                if line.removesuffix('"""') != line:
                    output += line.removesuffix('"""')
                    break
                output += line
                output += "\n"
            except KeyboardInterrupt:
                break
    if output == "***" and os.name == "posix":
        os.system("touch ./external_chat_input.txt")
        os.system("xdg-open ./external_chat_input.txt")
        input("Continue? ")
        with open("./external_chat_input.txt", "r") as file:
            output = file.read().strip()
        os.system("rm ./external_chat_input.txt")
    output = output.strip()
    return output


def clear() -> None:
    os.system("cls" if os.name == "nt" else "printf '\033c'")


def confirm_text(confirm_message: str) -> None:
    print(f"\n{confirm_message}\n")
    if os.name == "nt":
        os.system("pause")
    else:
        os.system("/bin/bash -c 'read -s -n 1 -p \"Press any key to continue...\"'")
        print()

def numeric_input(prompt: str) -> int:
    out = None
    while out == None:
        out = input(prompt)
        try:
            out = int(out)
        except:
            out = None
    return out

def filename_input(prompt: str) -> str:
    out = None
    illegal_characters = ["/", "\0", "\\", '"', "?", "*", "$", "&", "@", "|", "\\", "(", ")"]
    while out == None:
        out = input(prompt)
        if any(char in illegal_characters for char in out):
            out = None
    return out.strip()


def wrong_start_script():
    print("Please start the program by running 'main.py'\nThank you!")


if __name__ == "__main__":
    wrong_start_script()
