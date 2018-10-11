from Common.auxillary_functions import *

event_types = ('offsite', 'recording', 'redirected', 'multiple', 'none')
event_types_extended = ('Calls Handled by Workers at Other Sites', \
						'Callers Hear Recording to Call Back Later', \
						'Calls Redirected and Staff Moves to Alternate site', \
						'Multiple', \
						'None')

def get_site_events(sites):
	events = {event:[0 for _ in range(7)] for event in event_types}
	for site in sites:
		event = get_event(site)
		events[event][site.site_size] += 1
	events = {event_types_extended[i]:events[event_types[i]] for i in range(len(event_types))}
	return events
