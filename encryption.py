'''
to run: start python in terminal in parent dir, then run 'from password_converter import*'

things to do:

convert string of text to a decimal number, encrypt, then return
it's important to add a unpredictiable number to each number, 
    otherwise a common factor can be found, 
    (this takes the first 2 digits and uses it as a index of pi)
'''
from mpmath import mp
from itertools import chain, islice
import hashlib, tqdm, math, os
from b64 import b64

mp.dps = 100
pi = mp.pi
pi_digits = [*str(pi)]
pi_digits.remove('.')

def piecewise(iterable, n):
    iterable = iter(iterable)
    while True:
        try:
            yield chain([next(iterable)], islice(iterable, n-1))
        except StopIteration:
            print('done')
            return


def encrypt_chunk(full_string, master_password):
    full_string = full_string.strip()
    master_password = str(master_password)

    binary = '0b'+''.join(format(ord(i), '08b') for i in full_string) 
    base10 = int(binary, base = 0)

    #multiply by hash 
    m_hash = int(hashlib.md5(bytes(master_password, 'UTF-8')).hexdigest(), 16)
    hashed = base10 * m_hash

    #add 'salt' so passwords don't have a common factor
    salt = ( pi_digits[int(''.join([*str(hashed)][0:2]))] )
    salted = int(str(hashed)) + int(salt)
    #print(salted)
    text_encypted = b64(b10_value=salted).encode()
    return(text_encypted)
def decrypt_chunk(full_string, master_password):
    if full_string == '':
        return
    b10 = b64(b64_value = full_string).decode()
    master_password = str(master_password)

    salt = int( pi_digits[int(''.join([*str(b10)][0:2]))] )
    desalted = int(b10 - salt)

    m_hash = int(hashlib.md5(bytes(master_password, 'UTF-8')).hexdigest(), 16)
    #m_hash = int(''.join([*str(m_hash)][0:5]))
    dehashed = int(desalted // m_hash)
    #print(f'm_hash {m_hash} , dehashed {dehashed}')

    binary = bin(int(dehashed))
    binary = binary[2:]
    cut_spaces = ''.join(['0' for x in range(0,8-(len([*str(binary)]) % 8))])
    binary = cut_spaces + binary
    binary_list = [binary[x:x+8] for x in range(0, len(binary)-1) if x % 8 == 0]
    string = ''.join([chr(int(x, base = 2)) for x in binary_list])
    return(string)

def encrypt_str(input_string, key):
    split_str = [input_string[i:i+100] for i, x in enumerate(input_string) if (i % 100 == 0)]
    encrypted_chunks = []
    for chunk in tqdm.tqdm(split_str, desc='str chunks'):
        encrypted_chunks.append(encrypt_chunk(chunk, key))
    return(encrypted_chunks)
def decrypt_str(encrypted_chunks, key):
    decrypted_chunks = []
    for chunk in tqdm.tqdm(encrypted_chunks, desc='str chunks'):
        decrypted_chunk = decrypt_chunk(chunk, key)
        if decrypted_chunk != None:
            decrypted_chunks.append(decrypted_chunk)
    full_string = ''.join(decrypted_chunks)
    return(full_string)
    
def encrypt_file():
    input_filename = input('file to encrypt: ')
    master_pass = input('passkey: ')
    new_filename = input_filename + '.blnk'
    print('')

    if os.path.exists(new_filename):
        override = input('file already exists, overwrite? y/n ')
        if override == 'n':
            return
        elif override == 'y':
            os.remove(new_filename)
        else:
            raise TypeError('invalid input')

    if '.blnk' in input_filename:
        raise TypeError('inccorect file type')
    
    with open(input_filename, 'rb') as bigfile:
        for i, lines in enumerate(piecewise(bigfile, 2**16)):

            raw_data = list(lines)
            data_string = ''
            for line in raw_data:
                data_string += '*'.join([str(x) for x in line]) + '*'#this expects a single byte array
            data_string = data_string[:-1]
            encrypted = encrypt_str(data_string, master_pass)
            encrypted = str('\n'.join(encrypted))
            constant = 'i\'m makin\' love to the angel of death \n catchin feelings, never stumple, retracing my steps'
            check_str = str(int(bytes(master_pass, "UTF-8"), 16)*int(bytes(constant, "UTF-8"), 16))
            check_str = str(hashlib.md5(bytes(check_str, "UTF-8")).hexdigest())
            print(check_str)
            with open(new_filename, 'w') as f:
                f.write(check_str)#always 32 bytes
                f.write('0000000000000000')
                f.write(encrypted)

            print(f'wrote part {i}/{os.path.getsize(input_filename)//(2**16)} to {new_filename}')
def decrypt_file(): 
    input_filename = input('file to decrypt: ')
    master_pass = input('passkey: ')
    new_filename = input_filename.split('.')[0] + '.decrypted.' + input_filename.split('.')[1]
    print('')
    if '.blnk' not in input_filename:
        raise TypeError('inccorect file type')
    
    if os.path.exists(new_filename):
        override = input('file already exists, overwrite? y/n ')
        if override == 'n':
            return
        elif override == 'y':
            os.remove(new_filename)
        else:
            raise TypeError('invalid input')
        
    with open(input_filename, 'r') as bigfile:
        header = bigfile.read(32)
        constant = 'i\'m makin\' love to the angel of death \n catchin feelings, never stumple, retracing my steps'
        check_str = str(int(bytes(master_pass, "UTF-8"), 16)*int(bytes(constant, "UTF-8"), 16))
        check_str = str(hashlib.md5(bytes(check_str, "UTF-8")).hexdigest())
        if header != check_str:
            #print(f'given passkey: {check_str} \n header: {header}')
            raise TypeError('incorrect passkey')

        for i, lines in enumerate(piecewise(bigfile, 2**16)):
            encrypted_lines = (''.join([str(x) for x in lines])).split('\n')
            decrypted_str = decrypt_str(encrypted_lines, master_pass).strip('*')
            data = [int(x).to_bytes(1, byteorder='little') for x in decrypted_str.split('*')]
            with open(new_filename, 'ab') as f:
                for byte in data:
                    f.write(byte)
            print(f'wrote part {i}/{os.path.getsize(input_filename)//(2**16)} to {new_filename}')

if __name__ == '__main__':
    func_to_call = input('e to encrypt, d to decrypt: ')
    if func_to_call == 'e':
        encrypt_file()
    elif func_to_call == 'd':
        decrypt_file()
    else:
        raise TypeError('invalid input')