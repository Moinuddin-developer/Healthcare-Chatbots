import streamlit as st
import numpy as np
import pandas as pd
import os
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import _tree

# Title for the bot page
st.title("Healthcare Diagnosis Chatbot")

# Load datasets
training_dataset = pd.read_csv('Training.csv')
test_dataset = pd.read_csv('Testing.csv')

# Slicing and Dicing the dataset to separate features from predictions
X = training_dataset.iloc[:, 0:132].values
y = training_dataset.iloc[:, -1].values

# Dimensionality Reduction for removing redundancies
dimensionality_reduction = training_dataset.groupby(training_dataset['prognosis']).max()

# Encoding String values to integer constants
labelencoder = LabelEncoder()
y = labelencoder.fit_transform(y)

# Splitting the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

# Implementing the Decision Tree Classifier
classifier = DecisionTreeClassifier()
classifier.fit(X_train, y_train)

# Save column names
cols = training_dataset.columns[:-1]

# Load doctor data
doc_dataset = pd.read_csv('doctors_dataset.csv', names=['Name', 'Description'])
diseases = pd.DataFrame(dimensionality_reduction.index, columns=['prognosis'])
doctors = pd.DataFrame({
    'name': doc_dataset['Name'],
    'link': doc_dataset['Description'],
    'disease': diseases['prognosis']
})

# Chatbot Function
def execute_bot():
    st.write("Please reply with 'yes' or 'no' for the following symptoms:")

    symptoms_present = []

    def print_disease(node):
        node = node[0]
        disease = labelencoder.inverse_transform(node.nonzero()[0])
        return disease

    def tree_to_code(tree, feature_names):
        tree_ = tree.tree_
        feature_name = [
            feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree_.feature
        ]

        def recurse(node, depth):
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_name[node]
                threshold = tree_.threshold[node]
                st.write(f"Do you experience {name}?")
                ans = st.radio(f"{name}?", ["yes", "no"], key=name)
                
                if ans.lower() == "yes":
                    val = 1
                else:
                    val = 0
                
                if val <= threshold:
                    recurse(tree_.children_left[node], depth + 1)
                else:
                    symptoms_present.append(name)
                    recurse(tree_.children_right[node], depth + 1)
            else:
                present_disease = print_disease(tree_.value[node])
                st.write(f"You may have: **{present_disease[0]}**")
                
                symptoms_given = dimensionality_reduction.columns[
                    dimensionality_reduction.loc[present_disease[0]].values[0].nonzero()
                ]
                # confidence_level = len(symptoms_present) / len(symptoms_given)
                # Update confidence level calculation to handle zero symptoms case
                if len(symptoms_given) > 0:
                    confidence_level = len(symptoms_present) / len(symptoms_given)
                else:
                    confidence_level = 0  # Set confidence level to 0 if no symptoms are found

                st.write(f"**Confidence level:** {confidence_level:.2f}")

                
                st.write(f"**Symptoms present:** {', '.join(symptoms_present)}")
                st.write(f"**Confidence level:** {confidence_level:.2f}")
                
                doctor_row = doctors[doctors['disease'] == present_disease[0]]
                st.write("Consult:", doctor_row['name'].values[0])
                st.write("Visit:", doctor_row['link'].values[0])

        recurse(0, 1)

    tree_to_code(classifier, cols)

    if st.sidebar.button("Back to home"):
        os.system("streamlit run chatbot_ui.py")
        st.rerun() 

# Run the bot function
execute_bot()
