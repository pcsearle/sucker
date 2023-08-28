#! /usr/bin/env python3

import sys
import pandas as pd
import numpy as np

inFile = sys.argv[1]
outFile = sys.argv[2]

with open(inFile) as input, open(outFile, "w") as output:
    df = pd.read_csv(input, sep="\t")
    df = df.rename(columns={"id": "id1"}) # rename id column 
    df[['transcript', 'species', 'gene']] = df['id1'].astype('string').str.split('_', expand=True) # split id column into transcript, species, and gene column
    df[['clstr_iden', 'clstr_cov']] = df[['clstr_iden', 'clstr_cov']].replace(r'%', '', regex=True).apply(pd.to_numeric) # remove % from and convert clstr_iden and clstr_cov columns to numeric 
    df.query('clstr_iden >= 97', inplace=True) # filter out rows with clstr_iden < 97%
    df = df.groupby('clstr').filter(lambda x : len(x)>=3) # filter out clusters with less than 3 rows
    df = df.groupby('clstr').filter(lambda x: x['species'].nunique() >= 3) # filter out clusters that don't have all three species represented
    df = df.loc[df.groupby(['clstr', 'species'])['clstr_iden'].idxmax()] # if a species has multiple sequences represented in a cluster, only keep the sequence with the highest clstr_iden
    df['new'] = 1 + np.arange(len(df))//3 # generate integer to give gene new name based off of which cluster the gene is in
    df['id2']=df['id1'] + '_' + df['new'].astype(str) # create new name
    df.to_csv(output, columns = ['id1', 'id2'], header=False, index=False, sep='\t')
