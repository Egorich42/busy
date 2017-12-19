def sec_counter (sec):
	min = sec/60
	hours = sec/3600
	return (sec, min, hours)

def sec_calc(sec, min, hours):
	result = sum(sec, min/60, hours/3600)
	return result