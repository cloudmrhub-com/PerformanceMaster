import Poirot
import SimpleITK as sitk
p=Poirot.Poirot()




p.setMetric('./testdata/Metric.nii.gz')



p.setUX('./testdata/UX.nii.gz')
dimension = 3
offset = [2]*dimension # use a Python trick to create the offset list based on the dimension
T = sitk.TranslationTransform(dimension, offset)
p.setTransform(T)
O=p.getOutput()
O.writeImageAs('./testdata/Perf.nii.gz')

