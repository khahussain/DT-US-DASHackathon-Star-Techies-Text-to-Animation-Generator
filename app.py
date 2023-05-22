from flask import Flask, render_template, request
import requests
import openai
import json
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
    api_key = 'AIzaSyBDGi4Gp30SSSIFIWB925BLGvDyYVpIaJw'
    limit = 5
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
        openai.api_key = "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"
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
if __name__ == '__main__':
     app.run(debug=True)
    