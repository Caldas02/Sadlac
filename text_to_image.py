import streamlit as st
import base64
import requests
import os

def generate_image(text_prompt):
    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

    body = {
      "steps": 40,
      "width": 1024,
      "height": 1024,
      "seed": 0,
      "cfg_scale": 5,
      "samples": 1,
      "style_preset": "photographic",
      "text_prompts": [
        {
          "text": text_prompt,
          "weight": 1
        },
        {
          "text": "blurry, bad",
          "weight": -1
        }
      ],
    }

    headers = {
      "Accept": "application/json",
      "Content-Type": "application/json",
      "Authorization": "sk-sjF5Jp2SUiywg8IlGvUSsJlDLd1OPtLIRneprV5fN5dBASRW",
    }

    try:
        response = requests.post(
          url,
          headers=headers,
          json=body,
        )

        response.raise_for_status()

        data = response.json()

        # make sure the out directory exists
        if not os.path.exists("./out"):
            os.makedirs("./out")

        if "caldas" in text_prompt.lower() or "nugu" in text_prompt.lower():
            return "unique_name_message"
        
        image = data["artifacts"][0]
        with open(f'./out/txt2img_{image["seed"]}.png', "wb") as f:
            f.write(base64.b64decode(image["base64"]))
        return f'txt2img_{image["seed"]}.png'
    
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            return "invalid_search_flag"
        else:
            raise e

def main():
    st.title("Text to Image Generator")

    st.warning("This app generates images based on given text prompts. Please note that the generated images may not accurately represent the text prompts provided.")

    text_prompt = st.text_input("Enter text prompt")

    if st.button("Generate Image"):
        if text_prompt:
            generated_image = generate_image(text_prompt)
            if generated_image == "unique_name_message":
                st.error("The name is unique, we could not find an image that matches your search.")
            elif generated_image == "invalid_search_flag":
                st.error("Your search is flagged as invalid.")
            else:
                st.image(f'./out/{generated_image}', caption='Generated Image', use_column_width=True)
                st.success("Image generated successfully!")
        else:
            st.warning("Please enter a text prompt.")

if __name__ == "__main__":
    main()
