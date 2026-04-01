from flask import Flask, render_template, request
import numpy as np
import joblib

# Load model
model = joblib.load('heart_disease_model.pkl')

app = Flask(__name__)

# Feature order (VERY IMPORTANT ⚠️)
feature_names = [
    "age", "sex", "cp", "trestbps", "chol",
    "fbs", "restecg", "thalach", "exang",
    "oldpeak", "slope", "ca", "thal"
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get values in correct order
        features = [float(request.form.get(name)) for name in feature_names]

        final_input = np.array(features).reshape(1, -1)

        # Prediction
        prediction = model.predict(final_input)[0]
        probability = model.predict_proba(final_input)[0][1]

        # Result formatting
        if prediction == 1:
            result = f"⚠️ High Risk ({probability*100:.2f}%)"
        else:
            result = f"✅ Low Risk ({(1-probability)*100:.2f}%)"

        return render_template('index.html', prediction_text=result)

    except Exception as e:
        return render_template('index.html', prediction_text=f"Error: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)