1. Decide based on your use case:
   - use joblib for large models or NumPy-heavy data
   - use pickle for small or simple Python objects

2. To save a model with joblib:
   from joblib import dump
   dump(model, "model.joblib")

3. To load a model with joblib:
   from joblib import load
   model = load("model.joblib")

4. To save a model with pickle:
   import pickle
   with open("model.pkl", "wb") as f:
       pickle.dump(model, f)

5. To load a model with pickle:
   import pickle
   with open("model.pkl", "rb") as f:
       model = pickle.load(f)

6. Remember performance differences:
   - joblib is faster for large arrays
   - pickle is fine for small objects

7. Remember limitations:
   - do not load files from untrusted sources
   - both depend on Python version compatibility

8. For ML workflows:
   - prefer joblib for scikit-learn models
   - use pickle only when simplicity is enough
