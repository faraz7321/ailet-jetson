from datetime import datetime

def get_timestamp():
    # Get the current time
    now = datetime.now()
    
    # Format the timestamp as photo_ddmmyy_hhmmss
    timestamp = now.strftime("%d%m%y_%H%M%S")
    
    return timestamp