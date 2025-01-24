import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, 
    classification_report, 
    confusion_matrix, 
    precision_score, 
    recall_score, 
    f1_score
)
import joblib
import re

df = pd.read_csv("data/phishing_dataset.csv")


df['label'] = df['label'].map({"bad": 1, "good": 0})

def extract_features(url):
    length = len(url)
    num_dots = url.count('.')
    has_https = 1 if url.startswith('https') else 0
    return [length, num_dots, has_https]

X = df['url'].apply(extract_features).tolist()
y = df['label'].values


X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=42
)

model = LogisticRegression(class_weight='balanced')


model.fit(X_train, y_train)


y_pred = model.predict(X_test)


acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print("Accuracy:  {:.4f}".format(acc))
print("Precision: {:.4f}".format(prec))
print("Recall:    {:.4f}".format(rec))
print("F1-score:  {:.4f}".format(f1))


print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))


print("Classification Report:")
print(classification_report(y_test, y_pred, target_names=['good','bad']))


joblib.dump(model, "model.pkl")
print("Model saved to model.pkl.")
