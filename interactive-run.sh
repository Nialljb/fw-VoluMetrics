#!/usr/bin/env bash 

GEAR=fw-VoluMetrics
IMAGE=flywheel/volumetrics:$1
LOG=volumetrics-$1-$2

echo $IMAGE $LOG

# Command:
docker run -it --rm \
	-v /home/hajerkr/unity/fw-gears/${GEAR}/app/:/flywheel/v0/app\
	-v /home/hajerkr/unity/fw-gears/${GEAR}/utils:/flywheel/v0/utils\
	-v /home/hajerkr/unity/fw-gears/${GEAR}/run.py:/flywheel/v0/run.py\
	-v /home/hajerkr/unity/fw-gears/${GEAR}/${LOG}/input:/flywheel/v0/input\
	-v /home/hajerkr/unity/fw-gears/${GEAR}/${LOG}/output:/flywheel/v0/output\
	-v /home/hajerkr/unity/fw-gears/${GEAR}/${LOG}/work:/flywheel/v0/work\
	-v /home/hajerkr/unity/fw-gears/${GEAR}/${LOG}/config.json:/flywheel/v0/config.json\
	$IMAGE
