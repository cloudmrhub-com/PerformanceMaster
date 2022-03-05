import Poirot
import SimpleITK as sitk

"""Poirot test with fake data
1. Instantiate Poirot SNR
1. Set the metric reference in this case a fake SNR
1. set the ultimate SNR
1. set the transform between the two spaces (here is faked)
1. request the output
"""


metricMASK='/data/PROJECTS/POIROT/python/testdata/EM_MASK.nii.gz'
metric='/data/PROJECTS/POIROT/python/testdata/_FieldSNR.nii.gz'

UXMASK='/data/PROJECTS/POIROT/python/testdata/UISNR_MASK.nii.gz'
UX='/data/PROJECTS/POIROT/python/testdata/UISNR.nii.gz'

from myPy import im

#mask registration
mMask=im.Imaginable()
mMask.setInputFileName(metricMASK)

uxMask=im.Imaginable()
uxMask.setInputFileName(UXMASK)

r=Poirot.MaskRegistration(mMask,uxMask)

# initT=r.transformInitializerGuessRotation()
r.register()
T=r.getTransform()



p=Poirot.PoirotSNR()
p.setMetric(metric)
p.setUX(UX)
dimension = 3
p.setTransform(T)
O=p.getOutput()
O.writeImageAs('./testdata/Perf.nii.gz')
O.writeImageAs('./testdata/Perf.mha')

