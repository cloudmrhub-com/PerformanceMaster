from os import umask

from sklearn import metrics
import Poirot
import SimpleITK as sitk
from myPy import im

sfromUX=True
RMASKOUT='/data/PROJECTS/POIROT/python/testdata/T0/__recUISNR_MASK.nii.gz'
fieldsSNRfilename='/data/PROJECTS/POIROT/python/testdata/T0/__fieldSNR.nii.gz'

UXMASK='/data/PROJECTS/POIROT/python/testdata/T0/UISNR_MASK.nii.gz'
UXSNR='/data/PROJECTS/POIROT/python/testdata/T0/UISNR.nii.gz'
UXSIGMA='/data/PROJECTS/POIROT/python/testdata/T0/UISNR_SIGMA.nii.gz'



metricMASK='/data/PROJECTS/POIROT/python/testdata/T0/EM_MASK.nii.gz'
FAKESIGMA='/data/PROJECTS/POIROT/python/testdata/T0/EM_REGISTERED_SIGMA.nii.gz'
SFieldfn=None

HF='./testdata/EM_H.nii.gz'
EF='./testdata/EM_E.nii.gz'

OF='./testdata/T0/_resultsPerf.nii.gz'

#mask registration
mMask=im.Imaginable()
mMask.setInputFileName(metricMASK)

uxMask=im.Imaginable()
uxMask.setInputFileName(UXMASK)

r=Poirot.MaskRegistration(mMask,uxMask)

# initT=r.transformInitializerGuessRotation()
r.register(fn=RMASKOUT)
T=r.getTransform()



#electric field
e=Poirot.EField(EF)
#check if the conductivity is from the Ux or from the fields and resample
if sfromUX:
    sigma=im.Imaginable()
    sigma.setInputFileName(UXSIGMA)
    sigma.transformAndreshapeOverImage(mMask,T)
    e.setConductivity(sigma)
    if SFieldfn is not None:
        sigma.writeImageAs(SFieldfn)
else:
    e.setConductivity(FAKESIGMA) #pretend it is a conductivity

#magnetic field
h=Poirot.HField(HF)

#SNR from fields
eh=Poirot.EHFields(E=e,H=h)
fieldsSNR=eh.getSNR()
if fieldsSNRfilename is not None:
    fieldsSNR.writeImageAs(fieldsSNRfilename)




p=Poirot.Poirot("SNR")

p.setMetric(fieldsSNR)
p.setUX(UXSNR)
p.setTransform(T)
O=p.getOutput()
O.writeImageAs(OF)

