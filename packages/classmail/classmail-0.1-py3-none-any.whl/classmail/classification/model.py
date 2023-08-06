# classification/model.py
import random
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from flair.data import Sentence
from flair.models import TextClassifier
from lime.lime_text import LimeTextExplainer
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score)


class Model():
    def __init__(self, path, use_this_text_classifier=None):
        if type(use_this_text_classifier) == TextClassifier:
            self.classifier = use_this_text_classifier
        else:
            self.classifier = TextClassifier.load(
                "{}\\final-model.pt".format(path))

        self.path = path

    def _predict_one_exemple(self, text):
        sentence = Sentence(text)
        self.classifier.predict(sentence, multi_class_prob=True)

        predictions = [str(l) for l in sentence.labels]
        predictions.sort()
        return predictions

    def _get_probs(self, predictions):
        pred_probs = [[float(str(pred).split()[-1][1:-1])
                       for pred in preds]for preds in predictions]
        return pred_probs

    def _get_labels_names(self, predictions):
        labels_names = [" ".join(str(pred).split()[:-1])
                        for pred in predictions[0]]
        return labels_names

    def _get_prediction_probabilities(self, text_inputs):
        predictions = self.predict(text_inputs)
        predictions_prob = self._get_probs(predictions)

        return np.asarray(predictions_prob).astype(np.float64)

    def predict(self, text_inputs):
        """
        Use flair model to make classification (get all flair predictions with probabilities)

        Parameters
        ----------
        text_inputs : pandas series or list<str> or str
            String(s) to classify
        Returns
        -------
        list<list<str>> (List of flair predictions : [["label (probablity)"]])
        """
        if len(text_inputs) == 0:
            raise ValueError("Empty string")

        elif type(text_inputs) == str:
            text_inputs = [text_inputs]
        # list for predictions
        predictions = []
        # loop through input list and predict
        for text_input in text_inputs:
            preds = self._predict_one_exemple(text_input)
            predictions.append(preds)

        return predictions

    def get_predictions(self, text_input):
        """
        Use flair model to make classification (get only the class with highest probability)

        Parameters
        ----------
        text_inputs : pandas series or list<str> or str
            String(s) to classify
        Returns
        -------
        str (class with highest probability)
        """
        pred_dicts = self.get_prediction_dicts(text_input)
        predicted_class = [max(probs, key=probs.get)
                           for probs in pred_dicts]

        return predicted_class

    def get_prediction_dicts(self, text_inputs):
        """
        Use model to make classification (get a dict containing all predictions with probabilities)

        Parameters
        ----------
        text_inputs : pandas series or list<str> or str
            String(s) to classify
        Returns
        -------
        list<dict> ([{prediction:probability}])
        """
        predictions = self.predict(text_inputs)
        pred_probs = self._get_probs(predictions)
        labels_names = self._get_labels_names(predictions)

        pred_dicts = [dict(zip(labels_names, pred))
                      for pred in pred_probs]
        return pred_dicts

    def evaluate(self, predicted_labels, true_labels, average="weighted"):
        """
        Evaluate model with classif metrics : accuracy,precision,recall,F1-score.
        Average parameter comes from https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html
        """
        print("Accuracy:", accuracy_score(predicted_labels, true_labels))
        print("F1-score:", f1_score(predicted_labels, true_labels, average=average))
        print("Precision:", precision_score(
            predicted_labels, true_labels, average=average))
        print("Recall:", recall_score(
            predicted_labels, true_labels, average=average))

    def generate_preds_true_df(self, text, pred_labels, true_labels, export_to=None):
        """Generate a dataframe to explore predictions"""
        df = pd.DataFrame(
            {"Text": text, "Prediction": pred_labels, "True label": true_labels})

        df.index.name = '#'
        df["Good prediction"] = (df['Prediction'] == df['True label'])

        if export_to is not None:
            df.to_csv(export_to, sep=";", encoding="utf-8")

        return df

    def plot_discriminant_words(self, sorted_contributions, label, nb_words=15, title="default"):
        """
       Model explanation. Plot discriminant for the given label.

        Parameters
        ----------
        sorted_contributions : dict 
            Result from model.get_statistical_explanation
        label : str 
            Result from model.get_statistical_explanation
        nb_words : int, optionnal (default value=15)
            Number of words to plot
        title : str, optionnal (default value="Most important words for label")
            Title of the plot
        Returns
        -------
        None
        """
        if title == "default":
            title = "Most important words for {}".format(label)

        supporters = sorted_contributions[label]['supporters'][:nb_words]
        detractors = sorted_contributions[label]['detractors'][:nb_words]

        top_words = supporters.index.tolist()
        top_scores = supporters.tolist()
        bottom_words = detractors.index.tolist()
        bottom_scores = detractors.tolist()

        y_pos = np.arange(len(top_words))
        top_pairs = [(a, b) for a, b in zip(top_words, top_scores)]
        top_pairs = sorted(top_pairs, key=lambda x: x[1])

        bottom_pairs = [(a, b) for a, b in zip(bottom_words, bottom_scores)]
        bottom_pairs = sorted(bottom_pairs, key=lambda x: x[1], reverse=True)

        top_words = [a[0] for a in top_pairs]
        top_scores = [a[1] for a in top_pairs]

        bottom_words = [a[0] for a in bottom_pairs]
        bottom_scores = [a[1] for a in bottom_pairs]

        fig = plt.figure(figsize=(10, 10))

        plt.subplot(121)
        plt.barh(y_pos, bottom_scores, align='center', alpha=0.5)
        plt.title('Irrelevant', fontsize=20)
        plt.yticks(y_pos, bottom_words, fontsize=14)
        plt.suptitle('Key words', fontsize=16)
        plt.xlabel('Importance', fontsize=20)

        plt.subplot(122)
        plt.barh(y_pos, top_scores, align='center', alpha=0.5)
        plt.title('Relevant', fontsize=20)
        plt.yticks(y_pos, top_words, fontsize=14)
        plt.suptitle(title, fontsize=16)
        plt.xlabel('Importance', fontsize=20)

        plt.subplots_adjust(wspace=0.8)
        plt.show()

    def get_statistical_explanation(self, X_test, class_names, sample_size=100):
        """
        Model interpretation using LIME librarie (https://github.com/marcotcr/lime).
        See the terms used by the model to make classification.

        Parameters
         ----------
        X_test : pandas DataFrame 
            Text inputs
        class_names : list<str >
            Name list of your classes
        sample_size : str, optionnal (default value=100)
            Number of inputs to take for the explanation
         Returns
         -------
         Dict of dicts ({category: {detractors:[term1,term2,...], supporters:[term1,term2,...]}} where
         supporters (detractors) are terms that are relevant (irrelevant) for the category.)
         """
        random.seed(42)
        class_names.sort()
        mapping = dict(zip(range(len(class_names)), class_names))

        sample_sentences = random.sample(X_test.values.tolist(), sample_size)
        explainer = LimeTextExplainer(bow=False)

        labels_to_sentences = defaultdict(list)
        contributors = defaultdict(dict)

        # First, find contributing words to each class
        for sentence in sample_sentences:
            probabilities = self._get_prediction_probabilities(sentence)
            curr_label = probabilities[0].argmax()
            labels_to_sentences[curr_label].append(sentence)
            exp = explainer.explain_instance(
                sentence, self._get_prediction_probabilities, num_features=10, labels=[curr_label])
            listed_explanation = exp.as_list(label=curr_label)

            for word, contributing_weight in listed_explanation:
                if word in contributors[curr_label]:
                    contributors[curr_label][word].append(contributing_weight)
                else:
                    contributors[curr_label][word] = [contributing_weight]

        # average each word's contribution to a class, and sort them by impact
        average_contributions = {}
        sorted_contributions = {}
        for label, lexica in contributors.items():
            curr_label = label
            curr_lexica = lexica
            average_contributions[curr_label] = pd.Series(
                index=curr_lexica.keys())
            for word, scores in curr_lexica.items():
                average_contributions[curr_label].loc[word] = np.sum(
                    np.array(scores))/sample_size
            detractors = average_contributions[curr_label].sort_values()
            supporters = average_contributions[curr_label].sort_values(
                ascending=False)
            sorted_contributions[mapping[curr_label]] = {
                'detractors': detractors,
                'supporters': supporters
            }
        return sorted_contributions

    def _explain_one_instance(self, instance, class_names, num_features):
        explainer = LimeTextExplainer(class_names=class_names, bow=False)
        exp = explainer.explain_instance(
            instance, self._get_prediction_probabilities, num_features=num_features, top_labels=1)
        return exp

    def visualize_one_ex(self, X_test, y_test, index, num_features=10):
        """Model explanation. See the terms used by the model to make classification for one exemple"""
        print('Index: %d' % index)
        print('True class: %s' % y_test[index])

        class_names = sorted(y_test.unique())

        exp = self._explain_one_instance(
            X_test[index], class_names, num_features)
        exp.show_in_notebook(text=True)
        return exp

    def plot_confusion_matrix(self, pred_labels, true_labels, pred_labels_axename="Predicted label",
                              true_labels_axename="True label", inverse_axis=False, title="", cmap="YlGnBu"):
        """Plot confusion matrix using seaborn and sklearn"""
        label_names = np.unique(true_labels)

        conf_mat = confusion_matrix(
            true_labels, pred_labels, labels=label_names)
        conf_mat_normalized = conf_mat.astype(
            'float') / conf_mat.sum(axis=1)[:, np.newaxis]
        sns.heatmap(conf_mat_normalized, xticklabels=label_names,
                    yticklabels=label_names, cmap=cmap)

        if inverse_axis:
            x_label = pred_labels_axename
            ylabel = true_labels_axename
        else:
            x_label = true_labels_axename
            ylabel = pred_labels_axename

        plt.xlabel(x_label)
        plt.ylabel(ylabel)

        plt.title(title)
        plt.show()
