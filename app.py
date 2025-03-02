# from flask import Flask, request, render_template, jsonify
from llm_wrapper import LLMInterface
from satellite import EOSDataFetcher
from flask import Flask, render_template, request, jsonify
import json
import openai
from openai import OpenAI
app = Flask(__name__)
llm_interface = LLMInterface("")

api_key  = "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"
client = OpenAI(api_key=api_key)

# def get_completion(prompt, model="gpt-3.5-turbo"):
#    #  messages = [{"role": "user", "content": prompt}]
#    
#    #  response = client.chat.completions.create(
#    #          messages=messages,
#    #          model="gpt-4o"  # or your desired model
#    #      )
#    #  return response.choices[0].message.content
#    if '?' in prompt:
#       llm_interface = llm_interface.overwrite_question(prompt)
#    else:
#       llm_interface.add_context(prompt)
#    response = llm_interface.get_response()
#    return response

@app.route("/get")
def get_bot_response():
    global llm_interface  # Ensure we're referring to the global variable
    prompt = request.args.get('msg')
    
    # Call the method without reassigning llm_interface
    if '?' in prompt:
        llm_interface.overwrite_question(prompt)
    else:
        llm_interface.add_context(prompt)
    
    response = llm_interface.get_response()
    return response

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/map")
def map():
    return render_template("map.html")

@app.route("/message")
def message():
    return render_template("message.html")

@app.route("/save_coords", methods=["POST"])
def save_coords():
    data = request.get_json()
    plot_coords = data.get("plot_coords")
    # Save the plot_coords or process them as needed
    print("Received coordinates:", plot_coords)
   #  print(plot_coords)
   #  print(type(plot_coords))
    array_of_arrays = json.loads(plot_coords)
    fetcher = EOSDataFetcher(array_of_arrays)
    result = fetcher.fetch_method()
    llm_interface.add_context(result)
   #  print(result)
    
    return jsonify({"status": "success", "plot_coords": plot_coords})


if __name__ == '__main__':
    app.run(debug=True)