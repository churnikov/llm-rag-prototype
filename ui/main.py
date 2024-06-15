import asyncio

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
            "urls": ["https://www.scilifelab.se/", "https://data.scilifelab.se/"],
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


async def process_prompt(prompt, *args, **kwargs):
    try:
        return await asyncio.wait_for(async_process_prompt(prompt), timeout=6)
    except asyncio.TimeoutError:
        return "Processing timed out."


if __name__ == "__main__":
    with gr.Blocks(theme="JohnSmith9982/small_and_pretty") as demo:
        with gr.Tab(label="<h3>Chat with SciLifeLab websites</h3>"):
            gr.ChatInterface(
                fn=process_prompt,
                fill_height=False
            )
        with gr.Tab(label="Geneal LLMs"):
            gr.ChatInterface(
                fn=process_general_llm_prompt,
                additional_inputs=[
                    gr.Dropdown(
                        label="Model",
                        choices=["GPT-3.5", "GPT-4"],
                        value="GPT-3.5",
                        allow_custom_value=False
                    )
                ],
                additional_inputs_accordion=gr.Accordion(
                    label="Model options",
                    open=True
                ),
                fill_height=False
            )

    demo.queue()
    demo.launch(
        debug=True,
        server_name="0.0.0.0",
        server_port=8000,
        favicon_path="assets/scilifelab_favicon.png",
        auth=("username", "password")
    )
