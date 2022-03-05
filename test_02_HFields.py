import Poirot

"""HField allows user to calculate B1+ and b1 minus
1. instantiate the class
1. set the filename [x,y,z,v,C]
"""
p=Poirot.HField('./testdata/EM_H.nii.gz')
O=p.getB1minus()
O.writeImageAs('./testdata/H-.mha')

O=p.getB1plus()
O.writeImageAs('./testdata/H+.mha')

