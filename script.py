import gradio as gr
from datetime import datetime

from modules import shared

params = {
    "display_name": ""
}

HISTORY = []
LAST_INPUT = None

def get_label():
    return datetime.now().strftime("%I:%M:%S %p")

def input_modifier(string, state):
    global LAST_INPUT
    LAST_INPUT = string
    return string

def output_modifier(string, state):
    global LAST_INPUT, HISTORY
    if LAST_INPUT:
        label = get_label()
        output_text = string
        input_text = LAST_INPUT
        HISTORY += [(label, output_text, input_text)]
        LAST_INPUT = None
    return string

def select(selected_label):
    if not HISTORY:
        return "...", "...", gr.update(choices=["None"], value="None")

    label, output_text, input_text = HISTORY[-1]
    labels = [i[0] for i in HISTORY][::-1]

    for entry in HISTORY:
        if entry[0] == selected_label:
            label, output_text, input_text = entry
            break
    
    output_text, input_text = output_text.strip(), input_text.strip()

    return output_text, input_text, gr.update(choices=labels, value=label)

def clear(selected_label):
    global HISTORY
    HISTORY = []
    return select(selected_label)

def ui():
    with gr.Tab("History"):
        with gr.Row().style(equal_height=True):
            clear_btn = gr.Button("Clear", elem_classes='refresh-button')
            dropdown = gr.Dropdown(["None"], value="None", show_label=False, elem_classes='slim-dropdown')
            reload_btn = gr.Button("Reload", elem_classes='refresh-button')
        with gr.Column():
            with gr.Tab("Output"):
                output_area = gr.TextArea("...", show_label=False)
            with gr.Tab("Input"):
                input_area = gr.TextArea("...", show_label=False)

    args = ([dropdown], [output_area, input_area, dropdown])
    kwargs = {'show_progress': False, 'queue': False}

    shared.gradio['Generate'].click(select, *args, **kwargs)

    clear_btn.click(clear, *args, **kwargs)
    reload_btn.click(select, *args, **kwargs)
    dropdown.change(select, *args, **kwargs)
