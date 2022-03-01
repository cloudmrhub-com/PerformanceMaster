import Poirot





p=Poirot.EField('./testdata/EM_E.nii.gz')
p.setConductivity('./testdata/EM_MASK.nii.gz')

q=Poirot.HField('./testdata/EM_H.nii.gz')

F=Poirot.EHFields(E=p,H=q)
L=F.getSNR()
L.writeImageAs('./testdata/_fakesnrfield.nii.gz')

