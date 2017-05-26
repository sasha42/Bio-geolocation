# Bio location
Looks up the location of sequences in genbank and adds it to a FASTA file. In this repo there is a demo jupyter notebook as well as unprocessed and processed files as an example.


## Setup
You will need python3 and pip as a prerequisite. Virtualenv is highly recommended to keep these packages away from messing around with your other packages.

```
pip install jupyter
jupyter notebook
```
open browser and go to `Bio geolocation.ipynb`

## Workflow
You will need to sequence the genome and get an output from your lab. For example: [Mushroom Observer observation with DNA sequence of a new species of Suillus.](http://mushroomobserver.org/243577)

Then [BLAST](https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastn&PAGE_TYPE=BlastSearch&LINK_LOC=blasthome) is used to find closely related sequences. These are downloaded and then fed into the [GenBank database](https://www.ncbi.nlm.nih.gov/nuccore/JQ711926) to get the country.

All of this data is then used to [generate phylogenetic trees](http://www.phylogeny.fr/simple_phylogeny.cgi)

### Next steps
Probably write a server that accepts `.fas` files as uploads, and then renders it on a map.