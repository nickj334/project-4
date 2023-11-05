"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_acp.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

# Initializing global variables of each distance span with the following information included:
#   start_dist -> beginning of distance span
#   end_dist -> end of distance span
#   max_speed -> maximum speed a rider is allowed to bike within given span
#   min_speed -> minimum speed a rider is allowed to bike within given span
#   total_quickest_time -> amount of time it would take to ride span from front to end at max speed.
#       First value is hours, second value is minutes
#   total_slowest_time -> amount of time it would take to ride span from front to end at minimum speed.
#       First value is hours, second value is minutes
dist_span_1 = {'start_dist': 0, 'end_dist': 200, 'max_speed': 34, 'min_speed': 15, 'total_quickest_time': [5, 53], 'total_slowest_time': [13, 20]}
dist_span_2 = {'start_dist': 200, 'end_dist': 400, 'max_speed': 32, 'min_speed': 15, 'total_quickest_time': [6, 15], 'total_slowest_time': [13, 20]}
dist_span_3 = {'start_dist': 400, 'end_dist': 600, 'max_speed': 30, 'min_speed': 15, 'total_quickest_time': [6, 40], 'total_slowest_time': [13, 20]}
dist_span_4 = {'start_dist': 600, 'end_dist': 1000, 'max_speed': 28, 'min_speed': 11.428, 'total_quickest_time': [14, 17], 'total_slowest_time': [35, 0]}

# Initializing global variable of a list of all distance spans
dist_spans = [dist_span_1, dist_span_2, dist_span_3, dist_span_4]

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers // Spot of checkpoint
       brevet_dist_km: number, nominal distance of the brevet   // Overall distance of the race
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An arrow object                      // when the race starts
    Returns:
       An arrow object indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """

    # TODO if control_dist_km > (brevet_dist_km + (brevet_dist_km * 0.2)):

    log = ""
    
    # Set default control time to time at beginning of the race
    control_open_time = brevet_start_time

    # Running through each distance span in dist_spans
    for dist_span in dist_spans:
        # if the control checkpoint is within the selected distance span, then begin to calculate using information from dist_span
        if dist_span['start_dist'] < control_dist_km <= dist_span['end_dist']:
            log += "entering if with control_open_time = {}".format(control_open_time)
            # Calculates the time to checkpoint if rider is moving at max speed (aka the controls opening time):
            # First get distance of checkpoint from beginning of distance span to only account for this span, then divide that by max speed allowed
            fastest_time_to_control = (control_dist_km - dist_span['start_dist']) / dist_span['max_speed']

            # Seperating fastest_time_to_control into hours and minutes that it takes
            hour_shift = int(fastest_time_to_control)
            minute_shift = (fastest_time_to_control - hour_shift) * 60

            # Adjust return value with the time just found
            control_open_time = control_open_time.shift(hours=+hour_shift, minutes=+minute_shift)
            log += "exiting if with control open time = {}".format(control_open_time)

            # Got to the given checkpoint and can return overall time now
            break
        
        # If the control distance is not within this distance span, add the total_quickest_time of the span to account for distance, and then we can re-enter loop
        else:
            log += "entering else with control_open_time = {}".format(control_open_time)
            control_open_time = control_open_time.shift(hours=+dist_span['total_quickest_time'][0],
                                                    minutes=+dist_span['total_quickest_time'][1])
            log += "exiting else with control_open_time = {}".format(control_open_time)

    return control_open_time


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
          brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    
    control_close_time = brevet_start_time

    for dist_span in dist_spans:
        if dist_span['start_dist'] < control_dist_km <= dist_span['end_dist']:
            slowest_time_to_control = (control_dist_km - dist_span['start_dist']) / dist_span['min_speed']

            hour_shift = int(slowest_time_to_control)
            minute_shift = (slowest_time_to_control - hour_shift) * 60

            control_close_time = control_close_time.shift(hours=+hour_shift, minutes=+minute_shift)
            break
        else:
            control_close_time = control_close_time.shift(hours=+dist_span['total_slowest_time'][0], minutes=+dist_span['total_slowest_time'][1])





    return control_close_time
