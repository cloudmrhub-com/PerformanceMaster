import Poirot


from myPy import im

a=im.Imaginable(inputFileName='/data/PROJECTS/POIROT/python/testdata/T0/EM_REGISTERED_SIGMA.nii.gz')
p=Poirot.EField('/data/PROJECTS/POIROT/python/testdata/T0/EM_E.nii.gz')
p.setConductivity('/data/PROJECTS/POIROT/python/testdata/T0/EM_REGISTERED_SIGMA.nii.gz')
print(p.getNoiseCovarianceMatrix(operator="n",solver='pwc'))
