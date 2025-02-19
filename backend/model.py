from detoxify import Detoxify


detoxify_model = Detoxify("original")

def detect_toxicity(text):
    try:
        result = detoxify_model.predict(text)
        return result.get("toxicity", 0.0)
    except Exception as e:
        print(f"Error detecting toxicity: {e}")
        return 0.0
