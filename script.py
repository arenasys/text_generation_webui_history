import gradio as gr
from datetime import datetime

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
        return "", "", gr.update(choices=[], value="")

    label, output_text, input_text = HISTORY[-1]
    labels = [i[0] for i in HISTORY][::-1]

    for entry in HISTORY:
        if entry[0] == selected_label:
            label, output_text, input_text = entry
            break

    return output_text, input_text, gr.update(choices=labels, value=label)

def ui():
    with gr.Tab("History"):
        with gr.Row().style(equal_height=True):
            dropdown = gr.Dropdown([], show_label=False, elem_classes='slim-dropdown')
            reload = gr.Button("Reload", elem_classes='refresh-button')
        with gr.Column():
            with gr.Tab("Output"):
                output_area = gr.TextArea("", show_label=False)
            with gr.Tab("Input"):
                input_area = gr.TextArea("", show_label=False)

    args = ([dropdown], [output_area, input_area, dropdown])

    reload.click(select, *args)
    dropdown.change(select, *args)