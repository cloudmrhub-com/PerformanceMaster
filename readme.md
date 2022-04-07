# Performance Master v0.0v

## Installation
1. clone [Performance master](https://github.com/cloudmrhub-com/PerformanceMaster) 
    ```
    git clone https://github.com/cloudmrhub-com/PerformanceMaster.git
    ```

1. clone [erosmontin](https://github.com/erosmontin)'s [ Image Library ](https://github.com/erosmontin/myPy) and install the environment *em*
    ```
    git clone https://github.com/erosmontin/myPy.git && \
    conda env create -f myPy/environment.yml
    ```
1. extend the Image library environment for Poirot
    ```
    conda create --name poirot --clone me
    conda activate poirot
    pip install -r requirements.txt --user
    ```
## use case 1:

inputs:
1. type: SNR or TXE
1. ultimate
1. ultimate mask
1. metric
1. metric mask

## usecase 2:
1. type: SNR or TXE
1. ultimate
1. ultimate mask
1. metric mask
1. calculate SNR/TXE
	1. Efield
	1. Hfield
	1. Conductivity

## usecase 3:
1. type: SNR or TXE
1. ultimate
1. ultimate mask
1. metric mask
1. calculate SNR/TXE
	1. Efield
	1. Hfield
	1. Conductivity comes from ultimate



## Requirents
- conda
- 8GB RAM


[Eros Montin, PhD](me.biodimensional.com)
**Forty-six and two are just ahead of me**
