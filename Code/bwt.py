def bwt(s):
    """Apply Burrows-Wheeler transform to input string."""

    # Add start and end of text marker
    s = "\002" + s + "\003"
    # Table of rotations of string
    table = sorted(s[i:] + s[:i] for i in range(len(s)))
    # Last characters of each row
    last_column = [row[-1:] for row in table]  
    return "".join(last_column)


def ibwt(r):
    """Apply inverse Burrows-Wheeler transform."""

    # Make empty table
    table = [""] * len(r)  
    for i in range(len(r)):
        # Add a column of r
        table = sorted(r[i] + table[i] for i in range(len(r)))
        
    # Find the correct row (ending in ETX)
    s = [row for row in table if row.endswith("\003")][0]  
    return s.rstrip("\003").strip("\002") 
