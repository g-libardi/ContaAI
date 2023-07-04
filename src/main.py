import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton, QShortcut, QLineEdit, QLabel, QSpinBox
from PyQt5.QtGui import QColor, QPalette, QFont, QKeySequence, QTextCursor
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import re
import os

model_path = os.path.join(os.getcwd(), 'gpt2_small_contaAI')
device = torch.device('cpu')

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('ContaAI Text Editor')
window.setGeometry(100, 100, 600, 450)

# Set the background color to a gray dark blue
palette = QPalette()
palette.setColor(QPalette.Window, QColor('#2c3e50'))
window.setPalette(palette)

# Set the text box color to a light gray
text_palette = QPalette()
text_palette.setColor(QPalette.Base, QColor('#3f4e5e'))

# Set the text color to white
text_palette.setColor(QPalette.Text, QColor('#ffffff'))

# Set the font size to 14
font = QFont()
font.setPointSize(14)

text_box = QTextEdit(window)
text_box.setPalette(text_palette)
text_box.setFont(font)

# Add the text box to a vertical layout
layout = QVBoxLayout()
layout.addWidget(text_box)

# Add a vertical layout for the label and input
v_layout = QVBoxLayout()
layout.addLayout(v_layout)

# Add the label and a spin box to set the max_new_tokens parameter
max_new_tokens_label = QLabel('Words per Run', window)
max_new_tokens_label_palette = QPalette()
max_new_tokens_label_palette.setColor(QPalette.WindowText, QColor('#ffffff'))
max_new_tokens_label.setPalette(max_new_tokens_label_palette)
v_layout.addWidget(max_new_tokens_label)

max_new_tokens_edit = QSpinBox(window)
max_new_tokens_edit.setMinimum(1)
max_new_tokens_edit.setMaximum(1001)
max_new_tokens_edit.setFont(QFont("", 10))
v_layout.addWidget(max_new_tokens_edit)

# Define a function to run the model
# Load the tokenizer and model from local files
tokenizer = AutoTokenizer.from_pretrained('pierreguillou/gpt2-small-portuguese')
model = AutoModelForCausalLM.from_pretrained(model_path)
pipe = pipeline('text-generation', model=model, tokenizer=tokenizer)

# Keep track of the previous 15 predictions
previous_predictions = []

# Set the default max_new_tokens value
max_new_tokens = 1

# Define a function to run the model
def run_model():
    global previous_predictions, max_new_tokens, button
    
    # Move the cursor to the end of the text box
    cursor = text_box.textCursor()
    cursor.movePosition(QTextCursor.End)
    text_box.setTextCursor(cursor)
    
    # Get the text from the text box
    prompt = text_box.toPlainText()[-1000:]
    
    # Tokenize the text
    result = pipe(prompt, max_new_tokens=max_new_tokens, num_return_sequences=1)
    result = result[0]['generated_text'][len(prompt):]
    result = filter_string(result)
    
    # Save the previous prediction
    previous_predictions.append(text_box.toPlainText())
    
    # If there are more than 50 predictions, remove the oldest one
    if len(previous_predictions) > 50:
        previous_predictions.pop(0)
    
    # Insert the new prediction
    text_box.insertPlainText(result)
    
    # Enable the undo button
    undo_button.setEnabled(True)

# Define a function to filter the string
def filter_string(text):
    text = re.sub(r'\n{3,}', '\n\n', text)  # Replace three or more consecutive newlines with two newlines
    text = re.sub(r' {2,}', ' ', text)  # Replace two or more consecutive spaces with a single space
    return text

def undo_prediction():
    global previous_predictions, undo_button
    
    # Check if there are any predictions to undo
    if len(previous_predictions) == 0:
        return
    
    # Save the current position of the cursor
    cursor = text_box.textCursor()
    position = cursor.position()
    
    # Set the text box to the previous prediction
    text_box.setPlainText(previous_predictions[-1])
    
    # Restore the position of the cursor
    cursor.setPosition(position)
    text_box.setTextCursor(cursor)
    
    # Remove the last prediction from the buffer
    previous_predictions.pop()
    
    # Disable the undo button if there are no more predictions to undo
    if len(previous_predictions) == 0:
        undo_button.setEnabled(False)

# Define a function to update the max_new_tokens parameter
def update_max_new_tokens(text):
    global max_new_tokens
    
    # Try to parse the text as an integer
    try:
        max_new_tokens = int(text)
    except ValueError:
        pass

# Define the button and undo_button objects
button = QPushButton('Run Model (Ctrl + R)', window)
layout.addWidget(button)

undo_button = QPushButton('Undo (Ctrl + U)', window)
layout.addWidget(undo_button)

# Connect the button to the run_model function
button.clicked.connect(run_model)

# Connect the undo button to the undo_prediction function
undo_button.clicked.connect(undo_prediction)

# Connect the max_new_tokens edit to the update_max_new_tokens function
max_new_tokens_edit.textChanged.connect(update_max_new_tokens)

# Add keyboard shortcuts to the buttons
undo_shortcut = QShortcut(QKeySequence("Ctrl+U"), window)
undo_shortcut.activated.connect(undo_prediction)

run_shortcut = QShortcut(QKeySequence("Ctrl+R"), window)
run_shortcut.activated.connect(run_model)

window.setLayout(layout)
window.show()
sys.exit(app.exec_())