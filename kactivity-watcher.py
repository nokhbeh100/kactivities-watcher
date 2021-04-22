#!/usr/bin/env python3

from time import sleep
from datetime import datetime, timedelta, timezone

from aw_core.models import Event
from aw_client import ActivityWatchClient

import os

kactivityCommand = "kactivities-cli --current-activity"
def getCurrentKdeActivity():
	currentActivity = os.popen(kactivityCommand).read()
	status, actid, name, _ = currentActivity.split()
	#print( name )
	return name

client = ActivityWatchClient("aw-kactivities")

bucket_id = "{}_{}".format("aw-kactivities", client.client_hostname)
event_type = "KDE activitiy change"

client.create_bucket(bucket_id, event_type="ActivityChange")

with client:
	sleeptime = 1
	while(True):
		# Create a sample event to send as heartbeat
		act = getCurrentKdeActivity()
		heartbeat_data = {"title": act}
		now = datetime.now(timezone.utc)
		heartbeat_event = Event(timestamp=now, data=heartbeat_data)

		client.heartbeat(bucket_id, heartbeat_event, pulsetime=sleeptime+1, queued=True, commit_interval=4.0)

		# Sleep a second until next heartbeat
		sleep(sleeptime)
