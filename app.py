from flask import Flask, render_template, request
import requests
import openai
import json
from PIL import Image
from io import BytesIO
import imageio
import boto3
from botocore.client import Config
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

#Process1 to call the animation of the text
@app.route('/process1', methods=['POST'])
def process1():
    text = request.form['myText']
# Add your existing backend Python code here to process the text
    result = text_to_gif(text)
    return render_template('index.html', image_urls=result)

# def get_gifs_from_api(prompt):
#     api_key = "kk0uajO6KmWk3ps76bdrs99qs2Gw3iNt" # Replace with your GIPHY API key
#     url = f'https://api.giphy.com/v1/gifs/search?api_key={api_key}&q={prompt}&limit=5'
#     response = requests.get(url) 
    
#     if response.status_code == 200:
#         data = response.json()
#  # Extract GIF URLs from the API response
#         gif_urls = [gif['images']['original']['url'] for gif in data['data']]
#         return gif_urls
#     else:
#         print('Error occurred while fetching GIFs.')
#         return []
def text_to_gif(text_prompt):
    api_key = 'YOUR_API_KEY'
    limit = 10
    ckey = "star-techies"
    search_term = text_prompt
  # Set request parameters
    try:
        # Send GET request to the API endpoint
        response = requests.get("https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s" % (search_term, api_key, ckey, limit),verify = False)
        # Check the response status code
        if response.status_code == 200:
        # Retrieve the GIF URL from the response
            gif_urls = []
            r = json.loads(response.content)
            for i in range(0,limit):
                gif_url = r["results"][i]["media_formats"]["gif"]["url"]
                gif_urls.append(gif_url)
            return gif_urls
        else:
            print('Error generating GIF:', response.status_code)
            return []
    except requests.exceptions.RequestException as e:
        print('Error generating GIF:', e)

#Process2 to call the image of the text
@app.route('/process2', methods=['POST'])
def process2():
    text = request.form['myText']
# Add your existing backend Python code here to process the text
    result = image_generator(text)

    return render_template('index.html', image_urls=result)
def image_generator(prompt):
        openai.api_key = "YOUR_API_KEY"
        response=openai.Image.create(
        prompt=prompt,
        n=5,
        size="1024x1024"
        
        )
        image_urls = response["data"]  
        img_urls = []
        for i, image_url in enumerate(image_urls):
            img_urls.append(image_url["url"])
            
        return img_urls

#Process3 to make the image to gif
@app.route('/process3', methods=['POST'])
def process3():
    text = request.form['myText']
# Add your existing backend Python code here to process the text
    result = image_to_gif_generator(text)

    return render_template('index.html', image_urls=result)

def create_gif(image_urls, output_path):
    frames = []
    max_width = 0
    max_height = 0

 # Find the maximum width and height among all images
    for url in image_urls:
        try:
            response = requests.get(url,verify=False)
            image = Image.open(BytesIO(response.content))
            width, height = image.size
            max_width = max(max_width, width)
            max_height = max(max_height, height)
        except Exception as e:
            print(f"Error processing image from {url}: {e}")

 # Create a blank canvas with the maximum width and height
    canvas = Image.new('RGB', (max_width, max_height), (255, 255, 255))

# Paste each image onto the canvas
    for url in image_urls:
        try:
            response = requests.get(url,verify=False)
            image = Image.open(BytesIO(response.content))
            width, height = image.size

 # Calculate the offset to center the image
            x_offset = (max_width - width) // 2
            y_offset = (max_height - height) // 2

 # Create a copy of the canvas
            frame = canvas.copy()

 # Paste the image onto the frame at the center
            frame.paste(image, (x_offset, y_offset))

 # Append the frame to the frames
            frames.append(frame)
        except Exception as e:
            print(f"Error processing image from {url}: {e}")

 # Save the frames as a GIF
    imageio.mimsave(output_path, frames, format='GIF', duration=900)

def upload_gif_to_s3(file_path):

# Specify your AWS access keys and other details
    access_key = 'YOUR_AWS_IAM_ACCESS_KEY'
    secret_key = 'YOUR_AWS_IAM_SECRET_KEY'
    bucket_name = 'star-techies1'
    region_name = 'ap-south-1'

# Create a Boto3 S3 client

    s3 = boto3.client('s3',
                      config = Config(signature_version='s3v4'),
                      aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key,
                      verify=False)

 # Generate a unique object key based on the file name
    object_key = file_path

# Upload the file to the S3 bucket

    s3.upload_file(file_path, bucket_name, object_key)

# Generate the public URL of the uploaded file

    public_url = f"https://{bucket_name}.s3.{region_name}.amazonaws.com/{file_path}"
    return public_url

def image_to_gif_generator(prompt):
    gif_urls = []
    for index in range(2):
        openai.api_key = "YOUR_API_KEY"
        response=openai.Image.create(
        prompt=prompt,
        n=5,
        size="1024x1024"
        )
        image_urls = response["data"]
        img_urls = []
        for i, image_url in enumerate(image_urls):
            img_urls.append(image_url["url"])
        if(index == 0):
            output_file = 'output_file1.gif'
            create_gif(img_urls,output_file)
            public_url = upload_gif_to_s3(output_file)
            gif_urls.append(public_url)
        elif(index == 1):
            output_file = 'output_file2.gif'
            create_gif(img_urls,output_file)
            public_url = upload_gif_to_s3(output_file)
            gif_urls.append(public_url)
        elif(index == 2):
            output_file = 'output_file3.gif'
            create_gif(img_urls,output_file)
            public_url = upload_gif_to_s3(output_file)
            gif_urls.append(public_url)
        elif(index == 3):
            output_file = 'output_file4.gif'
            create_gif(img_urls,output_file)
            public_url = upload_gif_to_s3(output_file)
            gif_urls.append(public_url)
        elif(index == 4):
            output_file = 'output_file5.gif'
            create_gif(img_urls,output_file)
            public_url = upload_gif_to_s3(output_file)
            gif_urls.append(public_url)
    img_urls.clear()
    return gif_urls


if __name__ == '__main__':
        app.run(debug=True)
    
