import chainlit as cl
from openai import OpenAI
from ipynb.fs.defs.GenAI_Homework_1_Part_1 import get_current_temperature, generate_temperature_response, extract_city_name, process_temperature_query, generate_response_in_armenian, convert_text_to_speech_and_save, generate_image_and_get_url, analyze_image_with_text 

@cl.on_message
async def main(message: cl.Message):
    with open('apikey.txt','r') as f:
        openai_api_key = f.read()

    client = OpenAI(api_key=openai_api_key)

    openweathermap_api_key = "3b3ab17dc8c57469292f3f52b3278c0f"

    english_response = process_temperature_query(message.content, client, openweathermap_api_key, openai_api_key)
    armenian_response = generate_response_in_armenian(english_response, client, openai_api_key)
    convert_text_to_speech_and_save(armenian_response, client, "Temperature_in_Armenian.mp3")
    image_url = generate_image_and_get_url(english_response, client)
    response_content = analyze_image_with_text(image_url, client)

    image = cl.Image(url=image_url, name="Temperature in Yerevan", display="inline")
    audio = cl.Audio(name="Temperature_in_Armenian.mp3", path="Temperature_in_Armenian.mp3", display="inline")
    elements = [image, audio]

# Send a response back to the user
    await cl.Message(
        content=f"""Received:\n
        {english_response}\n
        {armenian_response}\n
        {response_content}""",
	elements = elements,
    ).send()
