import math, tqdm

class b64:
    def __init__ (self, b10_value = None, b64_value = None):
        self.b10_value = b10_value
        self.b64_value = b64_value

    def encode(self):
        b64_digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '.', '!']
        b10 = int(self.b10_value)
        
        total_places = int(math.log(b10, 64)//1)+1 
        digit_list = []
        value_list = []
        while b10 > 0:   
            place = (math.log(b10, 64)//1)
            val = int(b10 // 64 ** place )
            b10 -= int(val * (64 ** place ))
            digit_list.append(place)
            value_list.append(b64_digits[val])
            #print(f'place : {place}, val : {val} remaining b10 : {b10}')
        #print(f"digit_list = {digit_list} value_list = {value_list}, remaining = {b10}")
        value = []
        i = 0
        for digit in range(0, total_places):
            digit = total_places - (digit+1)
            if digit in digit_list:
                value.append(value_list[i])
                i += 1
            else:
                value.append(0)
        #print(f'first conversion {value}, left over base {b10}')
        #converts from a list to a string, then turns it to scientific notation significand|exponent (base is always 64)
        value = ''.join([str(x) for x in value])
        #print(f'after str conversion {value}')
        exponent = len(value)-len(value.strip('0')) 
        value = value.strip('0')
        value = f"{value}|{str(exponent)}"
        b64_value = value
        return(value)

    def decode(self):
        b64_digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '.', '!']
        b64 = self.b64_value
        b64, exponent = b64.split('|')
        b64 = f"{b64}{''.join(['0' for x in range(0, int(exponent))])}"
        #print(f'value after expansion    {b64}')
        split_b64 = [*b64]
        value = sum([(b64_digits.index(x)*(64**(len(split_b64)-(i+1)))) for i, x in enumerate(split_b64)])
        self.b10_value = value
        return(value) 
    
#'''
x = 1152921504606846978
a = b64(b10_value=x).encode()
b = b64(b64_value=a).decode()
print(f'error at x, {a} {b}, distance = {x - b}')
#'''

'''
start = int(input('start value: '))
end = int(input('end value: '))

x=0
errors = []
for x in tqdm.tqdm(range(start, end)):
    x += 1
    a = b64(b10_value=x).encode()
    b = b64(b64_value=a).decode()
    if x != b:
        print()
        print(f'error at {x}, {a} {b} , distance = {x - b}')
        errors.append(x)
#'''
