from dotenv import load_dotenv
import os
import google.generativeai as genai
import streamlit as st
from PIL import Image

# Load the API Key
load_dotenv()
genai.configure(api_key=os.getenv("key"))

# Function to load Google Gemini Vision Model and get response
def get_response_image(image, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([image[0], prompt])
    return response.text

# Function to load Google Gemini Pro Model and get response
def get_response(prompt, input):
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    response = model.generate_content([prompt, input])
    return response.text

# Prep Image Data
def prep_image(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File is uploaded!")

# Initialize the streamlit app
st.set_page_config(page_title="Personalized Fitness Trainer")
st.image('fitness_logo.jpg', width=400)
st.header("Personalized Fitness Trainer")

# Creating radio section choices
section_choice = st.radio("Choose Section:", ("Body Analysis", "Workout Plan", "Nutrition Plan", "Fitness Tips"))

###########################################################################################
if section_choice == "Body Analysis":
    upload_file = st.file_uploader("Upload a full-body picture", type=["jpg", "jpeg", "png"])
    image = ""
    if upload_file is not None:
        image = Image.open(upload_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

    input_prompt_body = """
    You are an expert personal trainer. Analyze the provided image and provide a summary of the person's physique, including:
    - Estimated body fat percentage
    - Muscle mass assessment
    - Areas that could benefit from improvement
    - General fitness level assessment
    Return the response using markdown.
    """

    submit = st.button("Analyze Body")
    if submit:
        image_data = prep_image(upload_file)
        response = get_response_image(image_data, input_prompt_body)
        st.subheader("Body Analysis:")
        st.write(response)

###########################################################################################
if section_choice == "Workout Plan":
    input_prompt_workout = """
    You are an expert personal trainer. Create a personalized workout plan based on the user's goals and fitness level.
    Consider the following:
    - User's fitness goals (e.g., weight loss, muscle gain, general fitness)
    - User's fitness level (beginner, intermediate, advanced)
    - User's available time per week
    - User's available equipment
    Provide a detailed workout plan with exercises, sets, reps, and rest periods.
    Return the response using markdown.
    """

    input_workout = st.text_area("Enter your fitness goals, level, time, and equipment:")
    
    submit1 = st.button("Generate Workout Plan")
    if submit1:
        response = get_response(input_prompt_workout, input_workout)
        st.subheader("Workout Plan:")
        st.write(response)

###########################################################################################
if section_choice == "Nutrition Plan":
    
    input_prompt_nutrition = """
    You are an expert nutritionist. Create a personalized nutrition plan based on the user's goals and dietary preferences.
    Consider the following:
    - User's fitness goals (e.g., weight loss, muscle gain, general fitness)
    - User's dietary preferences (e.g., vegetarian, vegan, gluten-free)
    - User's daily calorie intake
    - Macronutrient breakdown
    Provide a detailed meal plan with specific foods and portion sizes.
    Return the response using markdown.
    """
    
    input_nutrition = st.text_area("Enter your fitness goals, dietary preferences, and calorie intake:")
    
    submit2 = st.button("Generate Nutrition Plan")
    if submit2:
        response = get_response(input_prompt_nutrition, input_nutrition)
        st.subheader("Nutrition Plan:")
        st.write(response)

###########################################################################################
if section_choice == "Fitness Tips":
    
    input_prompt_tips = """
    You are an expert personal trainer. Provide general fitness tips and advice based on the user's inquiry.
    Consider topics such as:
    - Exercise techniques
    - Injury prevention
    - Motivation and consistency
    - Recovery and rest
    Return the response using markdown.
    """
    
    input_tips = st.text_area("Enter your fitness questions or topics:")
    
    submit3 = st.button("Get Fitness Tips")
    if submit3:
        response = get_response(input_prompt_tips, input_tips)
        st.subheader("Fitness Tips:")
        st.write(response)