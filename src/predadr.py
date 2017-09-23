from sklearn.externals import joblib
from sklearn.feature_extraction import FeatureHasher
from pandas import DataFrame
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem, MACCSkeys
from os import path


class Predadr(object):

    def __init__(self, classifier=path.join(path.dirname(__file__),'..','resources', 'classifier.pkl'), number_of_hash_features=50):

        self.classifier = joblib.load(classifier)
        self.hasher = FeatureHasher(n_features=number_of_hash_features, input_type="string")

        label_dictionary = DataFrame.from_csv(path.join(path.dirname(__file__),'..','resources', 'dictionary.tsv'), sep='\t')
        label_definitions = np.load(path.join(path.dirname(__file__),'..','resources', 'definitions.npy'))

        self.label_names = list()
        for umls in label_definitions:
            self.label_names.append(label_dictionary[label_dictionary.umls_meddra == umls].umls_def.values[0])

    def create_features(self, chemical):

        SMILES_hash = self.hasher.transform([chemical]).toarray()[0]

        mol = Chem.MolFromSmiles(chemical)
        fingerprint_1 = Chem.RDKFingerprint(mol, 1, 7, 2048, 2, True, 0.0, 128, True, True, 0, 0, None, None)
        fingerprint_2 = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=250)
        fingerprint_3 = MACCSkeys.GenMACCSKeys(mol)

        fingerprints = fingerprint_1 + fingerprint_2 + fingerprint_3

        fingerprints = np.array(fingerprints).astype(bool)

        return np.concatenate((SMILES_hash, fingerprints))

    def get_adrs(self, prediction):
        predicted_true = list()
        predicted_false = list()
        for i in range(len(prediction)):
            if prediction[i] == 0:
                predicted_false.append(self.label_names[i])
            elif prediction[i] == 1:
                predicted_true.append(self.label_names[i])
            else:
                print("Unexpected prediction")
        return predicted_true, predicted_false

    def predict(self, smiles):
        f = self.create_features(smiles)
        prediction = self.classifier.predict([f])
        return self.get_adrs(prediction[0])