# Better Ollama CLI
This project is designed provide most of the core Ollama functionality, but with a more user friendly interface.

This program has only been tested on Linux.

The program assumes that you have ollama installed, as well as a model already pulled.
See https://github.com/ollama/ollama for more details

# Use

1. Ensure you are inside the project folder

2. Create a virtual environment
'''
python -m venv ./venv/
'''

3. Activate the virtual environment
'''
source ./venv/bin/activate
'''

4. Install all required packages.
'''
pip install -r requirements.txt
'''

5. In a different shell, start ollama. (only required if not already running)
'''
ollama start
'''
or 
'''
systemctl start ollama.service
'''

6. Finally, start the program
'''
python ./main.py
'''

