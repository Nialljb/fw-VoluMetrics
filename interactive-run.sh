#!/usr/bin/env bash 

GEAR=fw-volumetrics
IMAGE=flywheel/volumetrics:$1
LOG=volumetrics-$1-$2

echo $IMAGE $LOG

# Command:
docker run -it --rm --entrypoint bash\
	-v /Users/hajer/Documents/unity/fw-gears/${GEAR}/app/:/flywheel/v0/app\
	-v /Users/hajer/Documents/unity/fw-gears/${GEAR}/utils:/flywheel/v0/utils\
	-v /Users/hajer/Documents/unity/fw-gears/${GEAR}/run.py:/flywheel/v0/run.py\
	-v /Users/hajer/Documents/unity/fw-gears/${GEAR}/${LOG}/input:/flywheel/v0/input\
	-v /Users/hajer/Documents/unity/fw-gears/${GEAR}/${LOG}/output:/flywheel/v0/output\
	-v /Users/hajer/Documents/unity/fw-gears/${GEAR}/${LOG}/work:/flywheel/v0/work\
	-v /Users/hajer/Documents/unity/fw-gears/${GEAR}/${LOG}/config.json:/flywheel/v0/config.json\
	$IMAGE
