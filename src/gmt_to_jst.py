

# Function to convert "created at" in GMT to JST

class GMTToJST(object):
	"""docstring for GMTToJST"""
	def __init__(self, arg):
		super(GMTToJST, self).__init__()
		self.arg = arg
		
	def YmdHMS(created_at):
	    time_utc = time.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
	    unix_time = calendar.timegm(time_utc)
	    time_local = time.localtime(unix_time)
	    return str(time.strftime("%Y-%m-%d %H:%M:%S", time_local))

	def HMS(created_at):
	    time_utc = time.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
	    unix_time = calendar.timegm(time_utc)
	    time_local = time.localtime(unix_time)
	    return str(time.strftime("%H:%M:%S", time_local))