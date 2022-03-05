import Poirot


from myPy import im
"""In this Test we set the necessary field to compute a Noise covariance matrix using the Electric field
1. Instantiate the EField Class witht the name of the file containing the Data
1. Set the conductivity
1. request the Noise Covariance Matrix
"""

p=Poirot.EField('/data/PROJECTS/POIROT/python/testdata/EM_E.nii.gz')
p.setConductivity('/data/PROJECTS/POIROT/python/testdata/_EM_REGISTERED_SIGMA.nii.gz')
print(p.getNoiseCovarianceMatrix())
