# encoding: utf-8
#!/usr/bin/python

import os, tempfile, sys, shutil, re
from os import listdir
from os.path import isfile, join
from datetime import datetime

class CoreNLP:
    """This is a wrapper class for the Stanford CoreNLP cli commands."""

    def __init__(self, jar_path):
        """
        Parameters
        ----------
        jar_path : str
            The path to Stanford CoreNLP's jar file.
        """

        self.jar_path = jar_path

    def train(self, training_data_path, prop_file_path):
        """
        Trains the classifier with the given prop file on the given data.
        The output will be saved to ./ .

        TODO: output_path

        Parameters
        ----------
        training_data_path : str
            The path to the annotated training files.
        prop_file_path : str
            The path to the .prop file of the model.
        """

        self._update_prop_(prop_file_path, training_data_path)
        command = f"java -cp {self.jar_path} edu.stanford.nlp.ie.crf.CRFClassifier -prop {prop_file_path}"
        output = run_cmd(command)
        return output

    def test_for_file(self, classifier_path, test_file_path):
        """
        TODO batch testing

        Parameters
        ----------
        classifier : str
            The path to the trained classifier.
        test_file_path : str
            The path to the annotated .tsv test file.
        """

        command = f"java -cp {self.jar_path} edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier {classifier_path} -testFile {test_file_path}"
        return run_cmd(command)

    def tokenize(self, input_dir, output_dir):
        """
        Takes all files in the `input_dir` and saves them tokenized in the
        `output_dir`.

        Parameters
        ----------
        input_dir : str
            The path to the files to be tokenized.
        output_dir : str
            The path to save the tokenized files.
        """

        output = ""
        for f in get_files(input_dir):
            command = f"java -cp {self.jar_path} edu.stanford.nlp.process.PTBTokenizer {input_dir+f} > {output_dir+f+'.tok'}"
            output += run_cmd(command)
        return output

    def annotate_tokenized_to_other(self, input_dir, output_dir):
        """
        Takes all files in the `input_dir` (that are already tokenized) and
        creates a .tsv annotation file for each in the `output_dir`. Every token
        will be assigned to O (other) entity type.

        Parameters
        ----------
        input_dir : str
            The path to the files to be annotated.
        output_dir : str
            The path to save the annotated files.
        """

        output = ""
        for f in get_files(input_dir):
            command = f"perl -ne 'chomp; print \"$_\tO\n\"' {input_dir+f} > {output_dir+f.split('.tok')[0]+'.tsv'}"
            output += run_cmd(command)
        return output

    def annotate_raw_to_other(self, input_dir, output_dir):
        """
        Takes all files in the `input_dir` and both tokenizes and annotates
        them. The output files will be saved to the `??utput_dir`. In between
        files (only tokenized) are not saved.

        Parameters
        ----------
        input_dir : str
            The path to the files to be tokenized and annotated.
        output_dir : str
            The path to save the annotated files.
        """

        output = ""
        tmp_dir = make_tmp_dir()
        output += self.tokenize(input_dir, tmp_dir)
        output += self.annotate_tokenized_to_other(tmp_dir, output_dir)
        remove_dir(tmp_dir)
        return output

    def convert_raw_with_ann_to_tsv(self, text_dir, ann_dir, output_dir):
        """
        This is specifically for the Markup annotation tool, which exports to
        .ann annotation files, but CoreNLP requires .tsv format.

        The corresponding files in the `text_dir` and `ann_dir` should have the
        same name, only different extenstion. (eg. file.txt, file.ann)

        Parameters
        ----------
        text_dir : str
            The path to the raw texts.
        ann_dir : str
            The path to the .ann files
        output_dir : str
            The path to save the annotated files.
        """

        tmp1 = make_tmp_dir()
        tmp2 = make_tmp_dir()
        token_start = "TOKEN"
        self._inject_entities_(text_dir,tmp1,self._get_annotations_(ann_dir),token_start)
        self.annotate_raw_to_other(tmp1, tmp2)
        self._apply_injected_entities_(tmp2, output_dir, token_start)
        remove_dir(tmp1)
        remove_dir(tmp2)

#-------------------------------------------------------------------------------
    def _get_annotation_(self, ann_text):
        lines = ann_text.split("\n")
        entities = {}
        arguments = {}
        for line in lines[:-1]:
            splitted_line = re.split('\t| ',line)
            if splitted_line[0][0] in "A":
                arguments[splitted_line[0]] = {
                    "type": splitted_line[1],
                    "entity": splitted_line[2],
                    "value": splitted_line[3]
                }
            else:
                entities[splitted_line[0]] = {
                    "type": splitted_line[1],
                    "start": int(splitted_line[2]),
                    "end": int(splitted_line[3]),
                    "value": splitted_line[4]}
        return {"entities": entities, "arguments": arguments}

    def _get_annotations_ (self, path):
        annotations = {}
        for f in get_files(path):
            annotations[f] = self._get_annotation_(get_text(path + f))
        return annotations

    def _get_injected_raw_(self, raw, entities, token_start):
        """
        Pasting in the entity types after each entity.
        """
        raw_w_entities = raw
        plus_index = 0
        for entity in entities:
            start = entities[entity]["start"]
            end = entities[entity]["end"]
            token = raw[start:end]
            token_parts = re.split(" |\t|\n",token)
            if raw[start] in [" ","\n","\t"]:
                replace_str = ""
            else:
                replace_str = " "
            for part in token_parts:
                replace_str += part +token_start+entities[entity]["type"]+" "
            raw_w_entities = raw_w_entities[:start+plus_index] + replace_str + raw_w_entities[end+plus_index:]
            plus_index += len(replace_str) - len(token)
        return raw_w_entities

    def _apply_injected_entities_(self, input_path, output_path, token_start):
        for f in get_files(input_path):
            text = get_text(input_path+f)
            new_text = ""
            for line in text.split("\n"):
                new_line = line
                parts = line.split(token_start)
                if len(parts) > 1:
                    new_line = parts[0] +"\t"+ parts[1].split("\t")[0]
                new_text += new_line +"\n"
            write_file(output_path+f,new_text[:-1])

    def _inject_entities_(self, input_path, output_path, annotations, token_start):
        for f in get_files(input_path):
            file_wo_ext = f.split(".txt")[0]
            raw = get_text(input_path + f)
            raw_w_entities = self._get_injected_raw_(raw, annotations[file_wo_ext+".ann"]["entities"], token_start)
            write_file(output_path+f+".txt", raw_w_entities)

    def _update_prop_(self, prop_file_path, training_data_path):
        training_files = get_files(training_data_path)
        training_list = ""
        for f in training_files:
            training_list += training_data_path + f + ","
        training_list = training_list[:-1]
        prop = get_text(prop_file_path)
        prop = re.sub("trainFileList =.*", "trainFileList = "+training_list, prop)
        write_file(prop_file_path, prop)


def make_tmp_dir():
    datestr = str(datetime.now()).replace(" ","-")
    tmp_dir = tempfile.gettempdir()+"/corenlp-"+datestr+"/"
    os.makedirs(tmp_dir)
    return tmp_dir

def remove_dir(dir):
    try:
        shutil.rmtree(dir)
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))

def get_files(path):
    return [f for f in listdir(path) if isfile(join(path, f))]

def write_file(path, text):
    with open(path, 'w', encoding='utf-8') as file:
        file.write(text)

def get_text(path):
    text = ""
    f = open(path, "r")
    text = f.read()
    f.close()
    return text

def run_cmd(command):
    stream = os.popen(command)
    return stream.read()
