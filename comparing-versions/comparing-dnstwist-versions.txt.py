Python 3.5.3 (default, Jan 19 2017, 14:11:04) 
[GCC 6.3.0 20170118] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import json
>>> dataGenABI = open('outputDnstwistGenABI.json').read().splitlines()
>>> len(dataGenABI)
373
>>> dataDnstwist = json.load(open('outputDnstwist.json'))
>>> len(dataDnstwist)
408
>>> dataDnstwist0623 = json.load(open('outputDnstwist0623.json'))
>>> len(dataDnstwist0623)
5338
>>> 
>>> ###
>>> 
>>> dataDomsDnstwist = []
>>> for d in dataDnstwist:
...     dataDomsDnstwist.append(d['domain-name'])
...
>>> dataDomsDnstwist0623 = []
>>> for d in dataDnstwist0623:
...     dataDomsDnstwist0623.append(d['domain-name'])
...
>>> 
>>> ###
>>> 
>>> for d in dataGenABI:
...     if d not in dataDomsDnstwist:
...             print(d)
... 
elevenp4ths.com
3l3venpaths.com
el3v3npaths.com
elevenpath5.com
3l3v3npaths.com
eleuenpaths.com
elevenpaths.it
elevenpaths.es
elevenpaths.uk
elevenpaths.net
elevenpaths.co
elevenpaths.edu
elevenpaths.org
elevenpaths.int
elevenpaths.se
elevenpaths.de
elevenpaths.fr
elevenpaths.gov
elevenpaths.mil
wwelevenpaths.com
wwwelevenpaths.com
www-elevenpaths.com
>>> ### 22 lines
>>> for d in dataDomsDnstwist:       
...     if d not in dataGenABI:      
...             print(d)             
... 
xn--elvnpaths-1ibb.com
xn--elevenaths-1eb.com
xn--elevenpats-sml.com
xn--elevenpaths-7lg.com
xn--elevenpths-kj3e.com
xn--elevenpths-f2d.com
xn--lvenpaths-93ib.com
xn--levenpaths-9zj.com
xn--elevenaths-j8h.com
xn--elevenpths-ngb.com
xn--elvenpaths-yq3e.com
xn--elevepaths-00b.com
xn--elevenaths-p4c.com
xn--elevenpath-e8b.com
xn--levenpaths-bnh.com
xn--lvnpaths-4ebbb.com
xn--elevenpahs-ubc.com
xn--elvenpaths-fnb.com
xn--elevnpaths-hnb.com
xn--elvnpaths-mjbb.com
xn--elevnpaths-3nb.com
xn--elevenpths-e7j.com
xn--eleenpaths-wph.com
xn--levenpaths-dnb.com
xn--lvnpaths-9ghbb.com
xn--elvenpaths-dnh.com
xn--elevenpths-g9c.com
xn--lvenpaths-uf7db.com
xn--elvenpaths-c0j.com
xn--elvenpaths-1nb.com
xn--elvnpaths-wygb.com
xn--elevnpaths-0q3e.com
xn--lvenpaths-kjbb.com
xn--lvnpaths-97hbb.com
xn--lvenpaths-98hb.com
xn--elevnpaths-e2i.com
xn--elvenpaths-c2i.com
xn--levenpaths-91i.com
xn--elevenpath-v2i.com
xn--levenpaths-znb.com
xn--levenpaths-wq3e.com
xn--lvnpaths-ebgbb.com
xn--elevenpahs-uwi.com
xn--lvnpaths-s30dbb.com
xn--elevenpats-bvi.com
xn--elevenpats-yj8b.com
xn--elevnpaths-fnh.com
xn--elevenpath-3ve.com
xn--lvenpaths-uygb.com
xn--elvnpaths-wf7db.com
xn--lvenpaths-zibb.com
xn--elvnpaths-c4ib.com
xn--eevenpaths-9zb.com
xn--elevnpaths-e0j.com
xn--eevenpaths-moe.com
xn--elvnpaths-c9hb.com
xn--lvnpaths-mebbb.com
>>> ### 57 lines
>>> ###
>>> ### en la función homoglyph de dnstwistGenABI se simplificaron las listas de cada char
>>> ### y se añadieron l33t chars (e=3, a=4, etc.). además, se añadieron 13 tlds.
>>> ### en el dnstwist original las listas de la función homoglyph son más largas.
>>> ###
>>> for d in dataDomsDnstwist:           
...     if d not in dataDomsDnstwist0623:
...             print(d)
...             c+=1
... 
xn--elevenaths-8qh.com
xn--elevenaths-1eb.com
xn--elevenpats-sml.com
xn--elevenpaths-7lg.com
xn--elevenpths-kj3e.com
xn--elevenpths-f2d.com
xn--elevenpths-w5a.com
xn--levenpaths-9zj.com
xn--elevenaths-j8h.com
xn--elevenpths-ngb.com
xn--levenpaths-96a.com
xn--elevenpths-mge.com
xn--elvenpaths-yq3e.com
xn--elvenpaths-y7a.com
xn--elevepaths-00b.com
xn--elevnpaths-llb.com
xn--elevnpaths-nsi.com
xn--elevenaths-p4c.com
xn--elevenpath-e8b.com
xn--levenpaths-3lb.com
xn--levenpaths-bnh.com
xn--elvenpaths-smb.com
xn--levenpaths-w7a.com
xn--elevenpats-wzj.com
xn--elevnpaths-p7a.com
xn--levenpaths-jsi.com
xn--elevenpahs-ubc.com
xn--elvenpaths-fnb.com
xn--elevnpaths-hnb.com
xn--elevnpaths-3nb.com
xn--elvenpaths-5lb.com
xn--elevenpths-e7j.com
xn--elevenpths-5qi.com
xn--levenpaths-qmb.com
xn--elevenpths-y4a.com
xn--elevenpths-l5a.com
xn--eleenpaths-wph.com
xn--elvenpaths-lsi.com
xn--levenpaths-dnb.com
xn--elevenpath-jr8b.com
xn--elevenpths-n4a.com
xn--elvenpaths-jlb.com
xn--levenpaths-l7a.com
eleverpaths.com
xn--elevenpths-75a.com
xn--elvenpaths-dnh.com
xn--elevenpths-g9c.com
xn--elevnpaths-umb.com
xn--eleenpaths-qdj.com
xn--elvenpaths-c0j.com
xn--elvenpaths-1nb.com
xn--elevnpaths-e7a.com
xn--elevnpaths-7lb.com
xn--elevnpaths-07a.com
xn--elevnpaths-0q3e.com
xn--elevnpaths-e2i.com
xn--elvenpaths-c2i.com
xn--elevenaths-5vi.com
xn--levenpaths-91i.com
xn--elevenpath-v2i.com
xn--elvenpaths-c7a.com
xn--levenpaths-znb.com
xn--elevenpath-0t6h.com
xn--levenpaths-wq3e.com
xn--elevenpahs-uwi.com
xn--elevenpats-bvi.com
xn--elevenpats-yj8b.com
xn--elevnpaths-fnh.com
xn--elevenpath-3ve.com
xn--elevenpths-94a.com
xn--levenpaths-hlb.com
eievenpaths.com
xn--elvenpaths-n7a.com
xn--eevenpaths-9zb.com
xn--elevnpaths-e0j.com
xn--eevenpaths-moe.com
xn--elevenpahs-8rh.com
>>> ### 77 lines
>>> res = []
>>> for d in dataDomsDnstwist0623:
...     if d not in dataDomsDnstwist:
...             res.append(d)
... 
>>> len(res)
5007
>>> ###
>>> ### dnstwist.py (v1.04b) elevenpaths.com: Processing 408 domain variants, 4 hits
>>> ### 	elevenpaths.com, eleven-paths.com, elevenpath.com, elvenpaths.com
>>> ### dnstwist.py (v20180623) elevenpaths.com: Processing 5338 domain variants, 7 hits (subdomains)
>>> ### 	elevenpaths.com, eleven-paths.com, elevenpath.com, elvenpaths.com,
>>> ### 	eleven.paths.com, elevenp.aths.com, elevenpat.hs.com
>>> ###
