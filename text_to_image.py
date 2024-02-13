import streamlit as st
import base64
import requests
import os

def text_to_image(text_prompt):
    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

    headers = {
        "Accept": "application/json",
        "Authorization": "sk-sjF5Jp2SUiywg8IlGvUSsJlDLd1OPtLIRneprV5fN5dBASRW"
    }

    body = {
        "steps": 40,
        "width": 1024,
        "height": 1024,
        "seed": 0,
        "cfg_scale": 5,
        "samples": 1,
        "text_prompts": [
            {
                "text": text_prompt,
                "weight": 1
            },
            {
                "text": "blurry, bad",
                "weight": -1
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()

        data = response.json()

        # Make sure the 'out' directory exists
        if not os.path.exists("./out"):
            os.makedirs("./out")

        for image in data["artifacts"]:
            with open(f'./out/txt2img_{image["seed"]}.png', "wb") as f:
                f.write(base64.b64decode(image["base64"]))

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            st.error("Too many requests. Please try again later.")
        else:
            raise e

def main():
    st.title("Text to Image Generator")

    st.write("This app generates images based on given text prompts.")

    text_prompt = st.text_input("Enter text prompt", "Type here...")

    if st.button("Generate Image"):
        if text_prompt:
            try:
                text_to_image(text_prompt)
                st.success("Image(s) generated successfully!")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a text prompt.")

if __name__ == "__main__":
    main()
