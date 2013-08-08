import mpd

def mpd_status(request):
	client = mpd.MPDClient()
	client.connect("localhost", 6600)
	status = client.status()
	client.disconnect()
	return {'mpd_status': status}
