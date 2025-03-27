import pickle
from flask import Flask, request, jsonify,app,url_for, render_template
import numpy as np
import pandas as pd

app = Flask(__name__)
# Load the model from the file
regmodel = pickle.load(open('regmodel.pkl', 'rb'))
scalar = pickle.load(open('scaler.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('home.html')

# Creating a predict api
@app.route('/predict_api', methods=['POST'])
def predict():
    # Get the data from the data key in the request
    # Assuming the data is sent as JSON in the request body
    data = request.json['data']
    print(data)
    # # Convert the data to a DataFrame
    # data_df = pd.DataFrame([data])
    # Just like in the juptyter notebook, we standardize the data
    # Convert the DataFrame to a numpy array
    data_array = np.array(list(data.values())).reshape(1, -1)
    # Standardize the data using the scalar object
    data_array = scalar.transform(data_array)
    # Make prediction using the model
    prediction = regmodel.predict(data_array)
    print(prediction)
    # Return the prediction as a JSON response
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
    app.run(debug=True)
