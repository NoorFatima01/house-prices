import pickle
import os
from flask import Flask, request, jsonify, render_template
import numpy as np

app = Flask(__name__)

# Load the model from the file
regmodel = pickle.load(open('regmodel.pkl', 'rb'))
scalar = pickle.load(open('scaler.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('home.html')

# Creating a predict API
@app.route('/predict_api', methods=['POST'])
def predict():
    # Get the data from the data key in the request
    # Assuming the data is sent as JSON in the request body
    data = request.json['data']
    print(data)

    # Convert input data to NumPy array and reshape
    data_array = np.array(list(data.values())).reshape(1, -1)

    # Standardize the data
    data_array = scalar.transform(data_array)

    # Make prediction
    prediction = regmodel.predict(data_array)
    print(prediction)

    return jsonify({'prediction': prediction[0]})


@app.route('/predict', methods=['POST'])
def predict_form():
    data = [float(x) for x in request.form.values()]
    final_input = scalar.transform(np.array(data).reshape(1, -1))
    print(final_input)

    prediction = regmodel.predict(final_input)
    print(prediction)

    return render_template("home.html", prediction_text="The predicted value is {}".format(prediction[0]))


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Get PORT from env or default to 5000
    app.run(host="0.0.0.0", port=port)
