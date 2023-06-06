import joblib
import numpy as np
import selfies as sf
import pandas as pd

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from flask import Flask, render_template, request, send_file
import io
import csv
from rdkit import Chem
from rdkit.Chem import AllChem


app = Flask(__name__)

# Load the trained machine learning model
model = joblib.load('model.joblib')

# Define a function to make predictions
def predict_properties(smiles):

    # Convert the SMILES string into a molecular fingerprint
    fp = np.array(list(AllChem.GetMorganFingerprintAsBitVect(Chem.MolFromSmiles(smiles), 2)))
    
    # Make predictions using the trained model
    prediction = model.predict([fp])[0]
    
    # Format the predicted compound characteristics as a dictionary
    result = {'MolecularWeight': np.round(prediction[0], 2),
              'XLogP': np.round(prediction[1],2) ,
              'ExactMass': np.round(prediction[2], 2),
              'TPSA': np.round(prediction[3], 2),
              'Complexity': np.round(prediction[4], 2),
              'Charge': np.round(prediction[5], 2)}
    
    return result

def generate_compounds(selfie, num_sequences = 100, num_beams = 100, max_length = 35, min_length = 5):
    
    tokenizer = AutoTokenizer.from_pretrained("zjunlp/MolGen-large-opt")
    model = AutoModelForSeq2SeqLM.from_pretrained("zjunlp/MolGen-large-opt")

    sf_input = tokenizer(selfie, return_tensors="pt")
    # beam search
    molecules = model.generate(input_ids=sf_input["input_ids"],
                              attention_mask=sf_input["attention_mask"],
                              max_length=max_length,
                              min_length=min_length,
                              num_return_sequences=num_sequences,
                              num_beams=num_beams)
    
    selfies_output = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=True).replace(" ","") for g in molecules]

    return selfies_output

def smiles_generator(smiles, max_length, min_length, num_seq):

    selfie = sf.encoder(smiles)

    generated_selfies = generate_compounds(selfie, num_sequences = num_seq, num_beams = num_seq, max_length = max_length, min_length = min_length)

    generated_smiles = list(set([sf.decoder(cmp) for i, cmp in enumerate(generated_selfies)]))

    return generated_smiles, generated_selfies

def generate_dataset(generated_smiles, generated_selfies):

    prop_dict = {'MolecularWeight': [],
                'XLogP': [],
                'ExactMass': [],
                'TPSA': [],
                'Complexity': [],
                'Charge': [],
                'Smiles': [],
                'Selfis':[]}
    for i, smile in enumerate(generated_smiles):

        #Predict compound properties
        properties = predict_properties(smile)

        # Append results
        prop_dict['MolecularWeight'].append(properties['MolecularWeight'])
        prop_dict['XLogP'].append(properties['XLogP'])
        prop_dict['ExactMass'].append(properties['ExactMass'])
        prop_dict['TPSA'].append(properties['TPSA'])
        prop_dict['Complexity'].append(properties['Complexity'])
        prop_dict['Charge'].append(int(properties['Charge']))
        prop_dict['Smiles'].append(smile)
        prop_dict['Selfis'].append(generated_selfies[i])

    dataset = pd.DataFrame(prop_dict)  
    
    return dataset

def main(smiles, max_length, min_length, num_seq):

    generated_smiles, generated_selfies = smiles_generator(smiles, max_length, min_length, num_seq)

    dataset = generate_dataset(generated_smiles, generated_selfies)

    dataset.to_csv()

    return dataset

# Define a route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Define a route for the prediction page
@app.route('/', methods=['POST'])
def predict_page():
    # Get the SMILES sequence from the form data
    smiles = request.form['smiles']
    min_length = int(request.form['min_length'])
    max_length = int(request.form['max_length'])
    num_seq = int(request.form['num_seq'])
    save_methods = request.form["save-method"]
    
    # Make predictions using the predict function
    dataset = main(smiles, max_length, min_length, num_seq)

    if save_methods == 'csv':
        filename = 'GeneratedSmiles.csv'
        data = dataset.to_csv(index=False)
        file = io.StringIO(data)
        file_data = io.BytesIO(file.getvalue().encode())
    elif save_methods == 'excel':
        filename = 'GeneratedSmiles.xlsx'
        file_data = io.BytesIO()
        dataset.to_excel(index=False, excel_writer=file_data, engine='openpyxl')
        file_data.seek(0)
    elif save_methods == 'json':
        filename = 'GeneratedSmiles.json'
        data = dataset.to_json(orient='records')
        file = io.StringIO(data)
        file_data = io.BytesIO(file.getvalue().encode())

    # Send file as a response
    return send_file(file_data, as_attachment=True, attachment_filename=filename)

if __name__ == '__main__':
    app.run(debug=True)

    
