import Poirot



"""In this example we compute the SNR using the field data
1. E Field
    1. Field 
    1. Conductivity
1. H Field
    1. Field
1. EHField
    1. E Field
    1. H Field
"""

p=Poirot.EField('./testdata/EM_E.nii.gz')
p.setConductivity('./testdata/_EM_REGISTERED_SIGMA.nii.gz')

q=Poirot.HField('./testdata/EM_H.nii.gz')

F=Poirot.EHFields(E=p,H=q)
L=F.getSNR()
L.writeImageAs('./testdata/_FieldSNR.nii.gz')
L.writeImageAs('./testdata/_FieldSNR.mha')

