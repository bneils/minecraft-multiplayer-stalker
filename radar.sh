#!/bin/bash
while :
do
	num_online=$(./oneshot.py)
	# 0 online - 20 sec delay
	# 2-4 online - 10 sec delay
	# 5-> online - 5
	if [ $num_online -eq 0 ] ; then
		delay=20
	fi
	if [ $num_online -ge 2 ] && [ $num_online -le 4 ] ; then
		delay=10
	fi
	if [ $num_online -ge 5 ] ; then
		delay=5
	fi
	sleep ${delay}s
done
