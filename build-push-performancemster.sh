

#!/bin/bash

DO="cloudmrhub/performancemaster"

if [ "$#" -ne 1 ]

then
echo "decide if dev (d), stable (s), test (t) or to not sync on dockerhub (no)"

exit 1
else
PUSH='y'
if [ $1 = "s" ]; then
T=":stable"
elif [ $1 = "d" ] || [ $1 = "dev" ]; then
T=":v0.0v"
elif [ $1 = "test" ] || [ $1 = "t" ]; then
T=":test"
elif [ $1 = "no" ]; then
PUSH='no'
DO="localperformancemaster"
T=''
fi
fi


theTAG=$DO$T
docker build -t $theTAG .

if [ $PUSH != "no" ]; then
read -p "We are going to push $theTAG, is it correct? press y to agree (read this!!!!!!!): " userInput && \

if [ $userInput = "y" ]; then

docker push $theTAG
else
echo nt synced
fi
fi