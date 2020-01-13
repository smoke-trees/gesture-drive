import xgboost
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import numpy as np
import glob
import os

raw_embeds = []
labels = []
current_label = 0
label_dict = {}
for i in glob.glob("embeddings/right_hand/*"):
    current_embed = pickle.load(open(i, 'rb'))
    raw_embeds = raw_embeds + current_embed
    labels += [current_label] * len(current_embed)
    label_dict[current_label] = os.path.basename(i).split('.')[0]
    current_label += 1

np_embeds = np.array(raw_embeds)
print(label_dict)

print("Raw embedding shape = ", np_embeds.shape)
nsamples, nx, ny, each = np_embeds.shape
flattened_embeds = np_embeds.reshape((nsamples, nx * ny * each))
print("Flattened embeddings shape =", flattened_embeds.shape)

x_train, x_test, y_train, y_test = train_test_split(flattened_embeds, labels, test_size=0.3, shuffle=True)
model = xgboost.XGBClassifier()
model.fit(x_train, y_train)
y_pred = model.predict(x_test)
acc = accuracy_score(y_test, y_pred)
print("Accuracy = ", acc)
clf_report = classification_report(y_test, y_pred)
print(clf_report)

pickle.dump(model, open("model/5gestmodelright.pkl", 'wb'))
pickle.dump(label_dict, open("model/5gestmodellabelsright.pkl", 'wb'))
