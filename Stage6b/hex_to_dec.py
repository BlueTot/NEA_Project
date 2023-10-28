digits = {"a": 10, "b": 11, "c": 12, "d": 13, "e": 14, "f":15}

def hex_to_dec(hex):
    digit1 = digits[d] if (d := hex[0].lower()) in digits else int(d)
    digit2 = digits[d] if (d := hex[1].lower()) in digits else int(d)
    return digit1 * 16 + digit2

def to_translucent(colour_code):
    return (hex_to_dec(colour_code[1:3]), hex_to_dec(colour_code[3:5]),
            hex_to_dec(colour_code[5:]), 150)