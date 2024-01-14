digits = {"a": 10, "b": 11, "c": 12, "d": 13, "e": 14, "f":15} # Hexadecimal - decimal key-value pairs for 10-15

def hex_to_dec(hex): # Function to convert 2-digit hexadecimal number to decimal number
    digit1 = digits[d] if (d := hex[0].lower()) in digits else int(d) # convert first digit
    digit2 = digits[d] if (d := hex[1].lower()) in digits else int(d) # convert second digit
    return digit1 * 16 + digit2 # calculate the result

def to_translucent(colour_code): # Function to get translucent version of colour code in RGBA format
    return (hex_to_dec(colour_code[1:3]), hex_to_dec(colour_code[3:5]),
            hex_to_dec(colour_code[5:]), 150) # Convert each 2-digit pair into decimal and add 150 which signifies the transparency