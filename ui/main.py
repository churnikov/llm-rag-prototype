import asyncio
import random
import time

import gradio as gr
import aiohttp


async def async_process_prompt(prompt):
    url = 'https://llm-api.serve-dev.scilifelab.se/chat_with_website'  # replace with your URL
    payload = {
        "converter": {
            "meta": {},
            "extraction_kwargs": {}
        },
        "fetcher": {
            "urls": [
                "https://www.scilifelab.se/",
                "https://www.data.scilifelab.se/",
                "https://www.scilifelab.se/data-driven/about/",
                "https://www.scilifelab.se/data/",
                "https://www.scilifelab.se/training/",
                "https://www.scilifelab.se/about-us/",
            ]
        },
        "llm": {
            "generation_kwargs": {}
        },
        "prompt": {
            "query": prompt
        }
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            result = await response.json()
    return result['llm']['replies'][0] if result['llm']['replies'] else 'No response from bot.'


async def process_general_llm_prompt(prompt, history, model_name, *args, **kwargs):
    if model_name == "GPT-3.5":
        url = "https://llm-api.serve-dev.scilifelab.se/chat_gpt"
    elif model_name == "GPT-4":
        url = "https://llm-api.serve-dev.scilifelab.se/chat_gpt4"
    else:
        return "Invalid model name."
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={
            "llm": {
                "generation_kwargs": {}
            },
            "prompt_builder": {
                "question": prompt,
            }
        }
                                ) as response:
            result = await response.json()
    return result['llm']['replies'][0] if result['llm']['replies'] else 'No response from bot.'


async def process_prompt(prompt, history, *args, **kwargs):
    if history:
        history.pop()
    try:
        return await asyncio.wait_for(async_process_prompt(prompt), timeout=10)
    except asyncio.TimeoutError:
        return "Processing timed out."


# Make request to this endpoint with custom input values
#curl -X 'POST' \
#  'https://llm-api.serve-dev.scilifelab.se/test_pipeline_01' \
#  -H 'accept: application/json' \
#  -H 'Content-Type: application/json' \
#  -d '{
#  "first_addition": {
#    "value": 0,
#    "add": 0
#  }
#}'
async def request_dummy_prompt(value, add, *args, **kwargs):
    url = 'https://llm-api.serve-dev.scilifelab.se/test_pipeline_01'  # replace with your URL
    payload = {
        "first_addition": {
            "value": value,
            "add": add
        }
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            result = await response.json()
    return result["double"]["value"]


async def proces_dummy_prompt(value, add, *args, **kwargs):
    try:
        return await asyncio.wait_for(request_dummy_prompt(value, add), timeout=10)
    except asyncio.TimeoutError:
        return "Processing timed out."


if __name__ == "__main__":
    with gr.Blocks(theme="JohnSmith9982/small_and_pretty") as demo:
        with gr.Tab(label="Ask a question about SciLifeLab"):
            gr.Markdown(value="<h3>Ask a question about SciLifeLab</h3>"
                              "<p>This is a tool that can answer questions about SciLifeLab based on the information "
                              "that is available on scilifelab.se website on top of the general knowledge of a Large "
                              "Language Model (in this case ChatGPT 3.5).</p>"
                              "<p>You can ask one question at a time but the "
                              "question can be as detailed/as long as you wish.</p>"
                        )
            sll_chatbot = gr.Chatbot(height=600, show_label=False)
            with gr.Row():
                sll_msg = gr.Textbox(scale=7,
                                     show_label=False,
                                     placeholder="Ask a question about SciLifeLab")
                sll_submit = gr.Button(
                    "Ask",
                    variant="primary",
                    scale=1,
                    min_width=150,
                )
            async def respond_sll(message, chat_history):
                chat_history = [(message, await process_prompt(message, chat_history))]
                return "", chat_history
            sll_msg.submit(respond_sll, [sll_msg, sll_chatbot], [sll_msg, sll_chatbot])
            sll_submit.click(respond_sll, [sll_msg, sll_chatbot], [sll_msg, sll_chatbot])

        with gr.Tab(label="Ask geneal LLMs"):
            gr.Markdown(value="<h3>Ask general LLMs</h3>"
                              "<p>Here you can ask a question to one of the general LLMs in the list below (currently "
                              "two versions of ChatGPT).</p> "
                              "<p>You can compare the answers you get from these two LLMs and "
                              "from the specialized SciLifeLab tool in the first tab.</p>")
            general_model = gr.Dropdown(
                label="Model",
                choices=["GPT-3.5", "GPT-4"],
                value="GPT-3.5",
                allow_custom_value=False,
                interactive=True
            )
            general_chatbot = gr.Chatbot(height=500, show_label=False)
            with gr.Row():
                general_msg = gr.Textbox(scale=7,
                                         show_label=False,
                                         placeholder="Ask a question")
                general_submit = gr.Button(
                    "Ask",
                    variant="primary",
                    scale=1,
                    min_width=150,
                )
            async def respond_general(message, chat_history):
                chat_history = [(message, await process_general_llm_prompt(message, chat_history, general_model.value))]
                return "", chat_history
            general_msg.submit(respond_general, [general_msg, general_chatbot], [general_msg, general_chatbot])
            general_submit.click(respond_general, [general_msg, general_chatbot], [general_msg, general_chatbot])

        with gr.Tab(label="Dummy"):
            # Interface that adds two numbers
            gr.Interface(
                fn=proces_dummy_prompt,
                inputs=[
                    gr.Number(label="Value"),
                    gr.Number(label="Add")
                ],
                outputs=gr.Textbox(label="Result")
            )
        with gr.Tab(label="Home"):
            chatbot = gr.Chatbot()
            msg = gr.Textbox()
            clear = gr.ClearButton([msg, chatbot])
            def respond(message, chat_history):
                bot_message = random.choice(["How are you?", "I love you", "I'm very hungry"])
                chat_history = [(message, bot_message)]
                return "", chat_history

            msg.submit(respond, [msg, chatbot], [msg, chatbot])

    demo.queue()
    demo.launch(
        server_name="0.0.0.0",
        server_port=8000,
        favicon_path="assets/scilifelab_favicon.png"
    )
