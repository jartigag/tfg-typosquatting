import os

files = []
doms = []
for f in os.listdir(os.getcwd()+'/csv'):
	files.append(f)
for file in files:
	with open('csv/'+file) as f:
		doms.append(f.read().splitlines())

for d in doms:
	pos = doms.index(d)
	for i in range(pos+1,len(doms)):
		if set(d) & set(doms[i]):
			print("duplicated domain(s) in %s and %s" % (files[pos],files[i]))
			print(set(d) & set(doms[i]),'\n')

#duplicated domains has been removed from .dat files 
# (IBER_-_IBER_COR_-_Dominios.dat)
#
#invalid domains has been removed from .dat files
# (VIVO,MERC,AMA,MAFH,DGP,TEF_ES_-_Domains.dat)
#
#duplicates has been removed from .dat files
# (TEF_CORP,TEF_XX-_-Domains)
