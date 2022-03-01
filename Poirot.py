
from myPy import mything,im

import scipy.constants as cnt
import SimpleITK as sitk
import numpy as np


   

class Poirot():
    """Poirot is an applciation that allow user to measure ultimate metrics like SNR and TTX against the ones obtained from simulations.
    In order to calculate the performance metric user need to set the UX metric and the Fields. The reference system of the UX and the field need t be oriented in the same way
    this means that x,y,z are defined as the nema standard (z is the B0 direction).
    Of course there will be  trnsformation between the two spaces and can be set using the set transform
    """    
    def __init__(self,pType=""):
        self.Log=mything.Log("Poirot")
        self.UX = im.Imaginable()
        # self.UXTTX = im.Imaginable()
        self.UXMask = im.Imaginable()
        self.Metric = im.Imaginable()
        self.MetricMask = im.Imaginable()
        self.Transform = None
        self.Performance = im.Imaginable()
        self.PerformanceType=pType

    def getOutput(self):
        """get the metric performance agauinst the UX

        Returns:
            _type_: im.Imaginable class with the result of your calculation
        """        
        o=self.getPerformance()
        if o.isImageSet():
            return o
        else:
            o=self.__calculate__()
            if o:
                return self.getOutput()
            else:
                return None

    def setPerformance(self,s):
        self.Performance=s

    def getPerformance(self):
        return self.Performance


    def setPerformanceType(self,s="SNR"):
        self.PerformanceType=s

    def getPerformanceType(self,s=""):
        return s+ self.PerformanceType

    def __calculate__(self):
        self.Log.append("start calculate " + self.getPerformanceType(),"pre")
        try:
            ABS=sitk.ComplexToModulusImageFilter()
            Metric=self.getMetric()
            m=Metric.getImage()            
            perf = 100*ABS.Execute(m)
            UX=self.getUX()
            #if eye then
            mUX=UX.getImage() #metric in the space of the metric
            smUX=ABS.Execute(mUX)
            transform=self.getTransform()
            
            UX.setImage(smUX)
            UX.transformAndreshapeOverImage(Metric,transform)
            amUX=UX.getImage()
            perf=perf/amUX            
            self.Performance.setImage(np.nan_to_num(perf, copy=False, nan=0.0, posinf=0.0, neginf=0.0))
            return True
        except:
            return False
    def getTransform(self):
        if self.Transform is None:
            o=self.__register__() #todo
            if o:
                return self.Transform
            else:
                return None
        else:
            return self.Transform

    def setTransform(self,t):

        self.Transform=t

    # def setUXMask(self,fixed):
       
    #     O=True
    #     if isinstance(fixed, str):
    #         self.UXMask.setImage(sitk.ReadImage(fixed,sitk.sitkFloat32))
    #     elif isinstance(fixed,sitk.Image):
    #         self.UXMask.setImage(fixed)
    #     else:
    #         O=False
        
    #     self.Log.append("Added UX Mask",O)
    #     return  O
    # def getUXMask(self):
    #     return self.UXMask

    # def setMetricMask(self,fixed):

    #     O=True
    #     if isinstance(fixed, str):
    #         self.FieldsMask.setImage(sitk.ReadImage(fixed,sitk.sitkFloat32))
    #     elif isinstance(fixed,sitk.Image):
    #         self.FieldsMask.setImage(fixed)
    #     else:
    #         O=False
        
    #     self.Log.append("Added Fields MASK",O)
    #     return  O
    
    # def getMetricMask(self):
    #     return self.FieldsMask
        
    def setMetric(self,fixed):

        O=True
        if isinstance(fixed, str):
            self.Metric.setInputFileName(fixed)
        elif isinstance(fixed,sitk.Image):
            self.Metric.setImage(fixed)
        elif isinstance(fixed,im.Imaginable):
            self.Metric=fixed
        else:
            O=False
        
        self.Log.append("Added Metric",O)
        return  O
    
    def getMetric(self):
        return self.Metric
    
    def setUX(self,fixed):

        O=True
        if isinstance(fixed, str):
            self.UX.setInputFileName(fixed)
        elif isinstance(fixed,sitk.Image):
            self.UX.setImage(fixed)
        elif isinstance(fixed,im.Imaginable):
            self.metric=fixed
        else:
            O=False
        
        self.Log.append("Added UX",O)
        return  O
    def getUX(self):
        return self.UX

class Field():
    #[x,y,z,V+JV,Coil]
    def __init__(self,F=None) -> None:
        self.F = im.Imaginable()
        if F is not None:
            self.setField(F)
    def setField(self,F):
        O=True
        if isinstance(F, str):
            self.F.setImage(sitk.ReadImage(F))
        elif isinstance(F,sitk.Image):
            self.F.setImage(F)
        elif isinstance(F,im.Imaginable):
            self.F=F
        else:
            O=False
        if (O):
            self.reset()
        return O

    def getField(self):
        return self.F
    
    def reset(self):
        pass



class HField(Field):
    def __init__(self,F=None):
        super(HField, self).__init__(F)
        self.B1plus =im.Imaginable()
        self.B1minus =im.Imaginable()

    def reset(self): #override
        #we want to recalculate the minus and plus in case H was changed 
        self.B1minus=im.Imaginable()
        self.B1plus=im.Imaginable()

    def setB1plus(self,F):
        self.B1plus=F


    def getB1plus(self):
        if self.B1plus.isImageSet():
            return self.B1plus
        else:
            b=self.__calcB1plusminus__(minus=False)
            self.setB1plus(b)
            return self.B1plus

    def __calcB1plusminus__(self,minus=True):
        """Calculate the B1 minus or plus 

        Args:
            minus (bool, optional): 
            - B1minus -> minus=True
            - B1plus -> minus=Flase

        Returns:
            _type_: im.Imaginable with b1 plus or minus
        """        
        H=self.getField()
        X,Y,Z,V,C=H.getImageSize()
        R=np.array(H.getImageSpacing())
        O=np.array(H.getImageOrigin())
        d=H.getImageDimension()
        D=np.reshape(np.array(H.getImageDirections()),[d, d])
        DO=D[0:4,0:4]
        #numpy is zyx while itk is xyz!!
        # IM=np.zeros((X,Y,Z,C),dtype=np.complex128)
        IM=np.zeros((C,Z,Y,X),dtype=np.complex128)
        A=H.getImageArray() #[C,V,Z,Y,X]
        if (minus):
            IM=cnt.mu_0*A[:,0,:,:,:]-A[:,1,:,:,:]*1j
        else:
            IM=cnt.mu_0*A[:,0,:,:,:]+A[:,1,:,:,:]*1j
        B1_SITK=im.createSITKImagefromArray(IM,R[np.r_[0,1,2,4]],O[np.r_[0,1,2,4]],DO.flatten())
        O=im.Imaginable()
        O.setImage(B1_SITK)
        return O


    def getB1minus(self):
        if self.B1minus.isImageSet():
            return self.B1minus
        else:  
            b=self.__calcB1plusminus__(minus=True)
            self.setB1minus(b)
            return self.B1minus

    def setB1minus(self,F):
        self.B1minus=F

class EField(Field):
    def __init__(self,F=None):
        super(EField, self).__init__(F)
        self.NoiseCovarianceMatrix =None
        self.Sigma=im.Imaginable() #conductivity
        self.operator="n"
        self.solver="pwc"
    def reset(self): #override
        #we want to recalculate the minus and plus in case H was changed 
        self.NoiseCovarianceMatrix=None

    def setNoiseCovarianceMatrix(self,NC):
        self.NoiseCovarianceMatrix=NC

    def getNoiseCovarianceMatrix(self):
        if self.NoiseCovarianceMatrix is not None:
            return self.NoiseCovarianceMatrix
        else:  
            self.setNoiseCovarianceMatrix(self.__calculateNCM__(self.operator,self.solver))
            return self.NoiseCovarianceMatrix
    
    def setConductivity(self,F):
        O=True
        if isinstance(F, str):
            self.Sigma.setInputFileName(F)
        elif isinstance(F,sitk.Image):
            self.Sigma.setImage(F)
        elif isinstance(F,im.Imaginable):
            self.Sigma=F
        else:
            O=False
        if (O):
            self.reset()
        return O

    def getConductivity(self):
        return self.Sigma


    def __calculateNCM__(self,operator="n",solver="pwc"):
        #first of all we need a field
        E=self.getField()
        vV=E.getVoxelVolume()
        if E.isImageSet():
            #then we need sigma
            S=self.getConductivity()
            if S.isImageSet():
                s=S.getImageArray() #[Z,Y,X]
                e=E.getImageArray() #[C,V,Z,Y,X]
                
                X,Y,Z,V,C=E.getImageSize()

                if((operator.lower()=="n") | (operator.lower()=="k") | (operator.lower=="n_conc_k")):
                    if (solver.lower()=="pwc"):
                #flattern components
                        Ex=np.matrix(np.zeros((X*Y*Z,C)),dtype=complex)
                        Ey=np.matrix(np.zeros((X*Y*Z,C)),dtype=complex)
                        Ez=np.matrix(np.zeros((X*Y*Z,C)),dtype=complex)
                        SS=np.matrix(np.zeros((X*Y*Z,C)),dtype=complex)
                        sf=np.matrix(s.flatten()).T
                        for c in range(C):
                            Ex[:,c]=np.matrix(e[c,0,:].flatten()).T
                            Ey[:,c]=np.matrix(e[c,1,:].flatten()).T
                            Ez[:,c]=np.matrix(e[c,2,:].flatten()).T
                            SS[:,c]=sf
                        
                        phi=(Ex.conj().T * np.multiply(Ex,SS))+ (Ey.conj().T * np.multiply(Ey,SS)) +(Ez.conj().T * np.multiply(Ez,SS))                                                   
                        return vV* phi.conj()
                    

                            
                        
                            # for x in range(X):
                            #     for y in range(Y):
                            #         for z in range(Z):
                            #             conductance=np.matrix(s[z,y,x])
                            #             for d in range(3): #trhee coordinate system [X,y,z]
                            #                 field=np.matrix(e[:,d,z,y,x])


                        # self.Log.append("Calculating Covariance Matrix as " + operator.lower() + " " solver.lower(),"ok")

                
                else:
                    return np.random.random([C,C])+np.random.random([C,C])*1j
                            
        else:
            # self.Log.append("Calculating Covariance Matrix","error")
            return None


class EHFields():
    """Fields class allows user to calcuate SNR and TTX, b1plus and minus
    """    
    def __init__(self,E,H) -> None:
        """_summary_

        Args:
            E (Efield): Electric Field -> we are getting the noise covariance matrix from here
            H (Hfield): Magnetic Field -> we are geting the b1 minus from here
        """        
        self.LOG=mything.Log('Field analysis')
        self.E = E
        self.H = H
        self.SNR =im.Imaginable()
    
    def getSNRScaling(self):
         return np.random.random(1)

    def getSNR(self):
        if self.SNR.isImageSet():
            return self.SNR
        else:
            NC=self.E.getNoiseCovarianceMatrix()
            invPsi = np.linalg.inv(NC)
            B=self.H.getB1minus()
            X,Y,Z,C=B.getImageSize()
            scaling_snr=self.getSNRScaling()
            SNR=np.zeros((Z,Y,X),dtype=np.complex128)
            A=B.getImageArray() #[C,Z,Y,X]
            # I know i hate this kind of loops, i miss itk and its iterator classes :(
            for x in range(X):
                for y in range(Y):
                    for z in range(Z):
                        Svox=np.matrix(A[:,z,y,x])
                        Svox=Svox.T
                        Spsiss=Svox.T*invPsi*Svox
                        SNR[z,y,x]=scaling_snr*np.sqrt(Spsiss)
            R=np.array(B.getImageSpacing())
            O=np.array(B.getImageOrigin())
            d=B.getImageDimension()
            D=np.reshape(np.array(B.getImageDirections()),[d, d])
            DO=D[0:3,0:3]
            SNR_SITK=im.createSITKImagefromArray(SNR,R[np.r_[0,1,2]],O[np.r_[0,1,2]],DO.flatten())
            O=im.Imaginable()
            O.setImage(SNR_SITK)
            self.EHSNR=O
            # self.Log.append("Calculating Fields SNR","ok")
            return O

# class PoirotSNR(Poirot):
#         self.Metric =im.Imaginable()
#         self.Sigma = im.Imaginable()
#         self.E = im.Imaginable()
#         self.H = im.Imaginable()

#         # self.constants={}
#         self.B1plus = im.Imaginable()
#         self.B1minus = im.Imaginable()
#         self.EHSNR = im.Imaginable()

#     def getInputDescription(self):
#         O={
#             #UX
#         "self.UX":"3D scalar image of complex type, x,y,z where z is the direction of the B0",
#         # "self.UXTTX":"3D scalar image of complex type, x,y,z, where z is the direction of the B0",
#         "self.UXMask":"3D scalar image of real type, x,y,z, where z is the direction of the B0",
#             #fields
#         "self.E":"3D Tensor image of complex type, x,y,z,V,channels, x,yz, where z is the direction of the B0",
#         "self.H":"3D Tensor image of complex type, x,y,z,V,channels, x,yz, where z is the direction of the B0",
#         "self.EHMask":"3D scalar image of real type, x,yz, where z is the direction of the B0",
#         "self.Sigma":"3D scalar image of real type, x,y,z, where z is the direction of the B0"
        
#         }
#         return O

    
#     def setSigmaFromUX(self,fixed):

#         if self.getTransform() is None:
#             m="Added Sigma from UX but the user didn't provide a trnasformation between the UX and the fields space"
#             print(m)
#             self.Log.append(m,'error')
#             return False
            
#         else:
#             O=True
#             S=im.Imaginable()
#             if isinstance(fixed, str):
#                 S.setImage(sitk.ReadImage(fixed,sitk.sitkFloat32))
#             elif isinstance(fixed,sitk.Image):
#                 S.setImage(fixed)
#             else:
#                 m="Sigma not filetype not recognized"
#                 print(m)
#                 self.Log.append(m,'error')
#                 return False

#             #apply transformation
#             S.transformAndreshapeOverImage(self.getUX(),self.getTransform())

#             self.setSigma(S)

#             self.Log.append("Added Sigma from UX",O)



#             return O


#     def setSigma(self,fixed):
        
#         O=True
#         if isinstance(fixed, str):
#             self.Sigma.setImage(sitk.ReadImage(fixed,sitk.sitkFloat32))
#         elif isinstance(fixed,sitk.Image):
#             self.Sigma.setImage(fixed)
#         elif isinstance(fixed,im.Imaginable):
#             self.Sigma=fixed
#         else:
#             O=False
#         self.Log.append("Added Sigma",O)
#         return O
#     def getSigma(self):
#         return self.getSigma()


#     def getPerformance(self):
#         #get the transformation between UXSNR and Field snr
#         # get ultimate
#         # get field snr
#         #
#         # calculate the performance
        
 
#         UXSNR=self.getUX()
#         # UXM=self.ge
#         FSNR=self.getEHSNR()

#         t=self.getTransform()
#         P=self.__calculate(UXSNR,FSNR,t)

#         return P

#     def __register(self):
#         UXMASK=self.getUXMask()
#         FMASK=self.getFieldMask()

#         a=RegistrationUX(UXMASK,FMASK)
#         t=a.register2()
#         return 1



class MaskRegistration(im.Registrationable):
    """_summary_

    Args:
        Registrationable (_type_): _description_
    """  
    def transformInitializerGuessRotation(self):
        
        fixed = self.FixedImaginable.getImage()
        moving = self.MovingImaginable.getImage()
        
        tx = sitk.CenteredTransformInitializer(fixed, moving,
                                    sitk.Euler3DTransform(),
                                    sitk.CenteredTransformInitializerFilter.MOMENTS)

        

        #find the best rotation
        n=np.deg2rad(90)
        R=((0,0,0),
           (0,0,n),
           (0,0,n*2),
           (0,0,n*3),
           (0,n,0),
           (0,n,n),
           (0,n,n*2),
           (0,n,n*3),
           (0,n*2,0),
           (0,n*2,n),
           (0,n*2,n*2),
           (0,n*2,n*3),
           (0,n*3,0),
           (0,n*3,n),
           (0,n*3,n*2),
           (0,n*3,n*3),
           (n,0,0),
           (n,0,n),
           (n,0,n*2),
           (n,0,n*3),
           (n,n,0),
           (n,n,n),
           (n,n,n*2),
           (n,n,n*3),
           (n,n*2,0),
           (n,n*2,n),
           (n,n*2,n*2),
           (n,n*2,n*3),
           (n,n*3,0),
           (n,n*3,n),
           (n,n*3,n*2),
           (n,n*3,n*3),
           (n*2,0,0),
           (n*2,0,n),
           (n*2,0,n*2),
           (n*2,0,n*3),
           (n*2,n,0),
           (n*2,n,n),
           (n*2,n,n*2),
           (n*2,n,n*3),
           (n*2,n*2,0),
           (n*2,n*2,n),
           (n*2,n*2,n*2),
           (n*2,n*2,n*3),
           (n*2,n*3,0),
           (n*2,n*3,n),
           (n*2,n*3,n*2),
           (n*2,n*3,n*3),
           (n*3,0,0),
           (n*3,0,n),
           (n*3,0,n*2),
           (n*3,0,n*3),
           (n*3,n,0),
           (n*3,n,n),
           (n*3,n,n*2),
           (n*3,n,n*3),
           (n*3,n*2,0),
           (n*3,n*2,n),
           (n*3,n*2,n*2),
           (n*3,n*2,n*3),
           (n*3,n*3,0),
           (n*3,n*3,n),
           (n*3,n*3,n*2),
           (n*3,n*3,n*3),
        )
           
        
        check=im.ROIable()
        check.setReference(self.FixedImaginable)
        check.setReferenceThreshold(1)
        c=0
        initial_transforms=[]
        similarity=[]
        for rr in R:
            P= [None] * 6
            t= tx.GetParameters()
            P[0:3]=rr #changing the rotation angles
            P[3:6]=t[3:6]
            tx.SetParameters(P)
            imm=self.MovingImaginable.getDuplicate()
            imm.transformAndreshapeOverImage(self.FixedImaginable,tx)
            #find a better transformation intializer with the rotated image
            tx2 = sitk.CenteredTransformInitializer(fixed, moving,
                            sitk.Euler3DTransform(),
                            sitk.CenteredTransformInitializerFilter.MOMENTS)
            t2= tx2.GetParameters()
            P[0:3]=rr #changing the rotation angles
            P[3:6]=t2[3:6]
            tx2.SetParameters(P)
            initial_transforms.append(tx2)
        #     imm2=self.MovingImaginable.getDuplicate()        
        #     imm2.transformAndreshapeOverImage(self.FixedImaginable,tx2,interpolator=sitk.sitkNearestNeighbor)
          
        #     check.setTest(imm2)
        #     check.setTestThreshold(1)
        #     similarity.append(check.getSimilarity())

        # out_transforms = []
        # for i in range(len(initial_transforms)):
        #     if similarity[i] == max(similarity):
        #         out_transforms.append(initial_transforms[i])

        # return out_transforms
        inds=im.getBestRegistrationAccuracyWithRegionOfInterest(self.getFixedImaginable(),self.getMovingImaginable(),initial_transforms,referenceThreshold=1,testThreshold=1)
        
        # return im.getiListIndexes(initial_transforms,inds)
        """_summary_

        Returns:
            _type_: _description_
            ..todo::
            -select tyhe best transform amnong the possible
        """        
        return initial_transforms[inds[0]]

        


    
    def register(self,fn=None):

        fixed = self.FixedImaginable.getImage()

        moving = self.MovingImaginable.getImage()

     
        tx=self.transformInitializerGuessRotation()
        
        R = sitk.ImageRegistrationMethod()

        R.SetMetricAsMeanSquares()
        R.SetMetricSamplingPercentage(0.9)

        R.SetOptimizerAsRegularStepGradientDescent(learningRate=1,
                                                minStep=1e-2,
                                                numberOfIterations=5000,
                                                gradientMagnitudeTolerance=1e-6)
        R.SetOptimizerScalesFromIndexShift()

        R.SetInitialTransform(tx)

        R.SetInterpolator(sitk.sitkNearestNeighbor)

        R.AddCommand(sitk.sitkIterationEvent, lambda: im.command_iteration(R))

        outTx = R.Execute(fixed, moving)

        print("-------")
        # print(outTx)
        print(f"Optimizer stop condition: {R.GetOptimizerStopConditionDescription()}")
        print(f" Iteration: {R.GetOptimizerIteration()}")
        print(f" Metric value: {R.GetMetricValue()}")

        # sitk.WriteTransform(outTx, fn)

        self.setTransform(outTx)

        if fn is not None:
            o=self.getMovingRegisteredImaginable()
            o.writeImageAs(fn)
        return True

                

      
# # https://simpleitk.readthedocs.io/en/master/link_ImageRegistrationMethod3_docs.html

   