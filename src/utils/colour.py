from functools import partial
import math


def normalize_values(i, max_log_value, min_log_value):
    i=(math.log(i))*256.0/max_log_value
    val = int(i % 256)
    colour_ranges = [
        (val,0,0),
        (255,val,0),
        (255,255,val),
    ]
    category = int((i % 256*len(colour_ranges))/256)
    return colour_ranges[category]

def get_colour_function(flows):
    max_log_value = max([math.log(i) for i in flows])
    min_log_value = min([math.log(i) for i in flows])
    print(f"Max flow: {max(flows)}")
    print(f"Max log(flow): {max_log_value}")
    print(f"Min log(flow): {min_log_value}")
    return partial(normalize_values, max_log_value=max_log_value, min_log_value=min_log_value)
