def enum(**named_values):
    return type('Enum', (), named_values)

Tools = enum(drawing = 0, zoom = 1, recip = 2, ruler = 3)