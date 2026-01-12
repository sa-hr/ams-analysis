# AMS Analysis in Croatia

Data used is publicly available in https://porezna.gov.hr/RpoProvjeriObveznikaPdvWeb/upit/visestruko

Steps for generating the sqlite database:
1. Run `transform.py` on the CSV to get the data into a new table
2. Run `runall.py` and wait for data to be populated
