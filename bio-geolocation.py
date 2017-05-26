# coding: utf-8
# Bio geolocation
# Looks up the location of sequences in GenBank and adds it to the FASTA file

import os
import re
import requests
import time
import json


# set the GenBank url
url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide&id={}&rettype=gb"

def load_file():
    """ load the file """
    file = open("suillus.fas","r")
    fas = file.read()

    # separate the fas file into a list of sequences
    sequences = fas.split('>')[1:]
    return(sequences)

def extract_name_id(sequences):
    """ get the ID and name from the sequences """
    sequences_processed = []

    for sequence in sequences:    
        try:
            # creating a local dict
            seq = {}

            # assession
            assession_regex = re.search(r'([A-Z]+\d+)', sequence)
            seq['assession'] = assession_regex.group()
            
            # name
            split_sequence = sequence.split(' ')
            seq['name'] = "{} {}".format(split_sequence[1], split_sequence[2])
            
            # add to dict
            sequences_processed.append(seq)
        except:
            continue

    return(sequences_processed)

def get_geolocation(sequences_processed):
    """ get the geolocation from GenBank """
    sequences_with_geolcation = []

    for sequence in sequences_processed:
        # local dict
        seq = {}
        seq['name'] = sequence['name']
        
        # formatting url
        seq['assession'] = str(sequence['assession'])
        formatted_url = url.format(seq['assession'])

        # getting the data and splitting it into lines
        resp = requests.get(formatted_url)
        resp_text = resp.text
        resp_lines = resp_text.split('\n')

        # ugly loop that checks if there is a country or lat_lon
        # variable and saves the output if at least one of them
        # is true
        for line in resp_lines:
            # regex search
            regex = re.search(r'(/country|/lat_lon)', line)
            try:
                # returns none if no matches found
                if regex.group():
                    if "/country=" in line.split('"')[0]:
                        seq['country'] = line.split('"')[1]
                    if "/lat_lon=" in line.split('"')[0]:
                        seq['lat_lon'] = line.split('"')[1]
            except:
                continue

        # append to list
        sequences_with_geolcation.append(seq)
        
        # don't kill the server and sleep for 200ms
        time.sleep(0.2)

    return(sequences_with_geolcation)

def save_json():
    """ save json - unused """
    with open('suillus_processed.json', 'w') as fp:
        json.dump(sequences_with_geolcation, fp)

def process_to_fas(sequences, sequences_with_geolcation):
    sequences_formatted_as_fas = []

    for s in range(len(sequences)):
        try:
            # getting the right sequence data from two different lists
            original = sequences[s+1]
            processed = sequences_with_geolcation[s]
            
            # finding the data we need
            actual_sequence_dirty = original.split('\n',1)[1:]
            actual_sequence = ''.join(actual_sequence_dirty) # this makes a list into a string
            name = processed['name']
            assession = processed['assession']
            country = processed.get('country')
            #print(">",assession,name,country,"\n",actual_sequence)
            
            # adding it quickly to a list
            sequence_formatted = "> ",assession, " ", name, " ",country,"\n",actual_sequence
            sequences_formatted_as_fas.append(sequence_formatted)
        except:
            continue

    # will figure this out another day
    #try:
        #lines = sequence.split('\n',1)[1:]
        #assession_regex = re.search(r'([A-Z]+\d+)', sequence)
        #assession = assession_regex.group()
        #full = sequences_with_geolcation[sequence]
        #if len(lines) < 1:
        #    continue
            #print(len(lines))
            #words = sequence.split(' ')
            #print(words)
            #for string in words:
            #    print(len(string))
        #print(full)
    #except:
        #continue
    return(sequences_formatted_as_fas)

def save_to_fas(sequences_formatted_as_fas):
    output = open('suillus_processed.fas', 'w')

    for seq in sequences_formatted_as_fas:
        try:
            s = ''.join(seq)
            output.write(s)
        except:
            pass

    output.close()


if __name__ == '__main__':
    print("\033[1m" + "\nBio geolocation" + "\033[0m")
    print("---------------")
    sequences = load_file()
    print("extracting data from {} sequences".format(len(sequences)))
    sequences_processed = extract_name_id(sequences)
    print("getting geolocation data (this takes a while)")
    sequences_with_geolcation = get_geolocation(sequences_processed)
    print("saving into a FASTA file")
    sequences_formatted_as_fas = process_to_fas(sequences, sequences_with_geolcation)
    save_to_fas(sequences_formatted_as_fas)
