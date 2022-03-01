import Poirot


p=Poirot.HField('./testdata/EM_H.nii.gz')
O=p.getB1minus()
O.writeImageAs('./testdata/H-.nii.gz')

O=p.getB1plus()
O.writeImageAs('./testdata/H+.nii.gz')

