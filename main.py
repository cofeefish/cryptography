'''
to run: start python in terminal in parent dir, then run 'from password_converter import*'

things to do:

convert string of text to a decimal number, encrypt, then return
it's important to add a unpredictiable number to each number, 
    otherwise a common factor can be found, 
    (this takes the first 2 digits and uses it as a index of pi)
'''
from itertools import chain, islice
import hashlib, tqdm, os, sys
import coding_methods

check_salt = 301883

#file handling
def piecewise(iterable, n):
    iterable = iter(iterable)
    while True:
        try:
            yield chain([next(iterable)], islice(iterable, n-1))
        except StopIteration:
            print('done')
            return
def file_exists(filename):
    if os.path.exists(filename):
        override = input('file already exists, overwrite? y/n ')
        if override == 'n':
            sys.exit()
        elif override == 'y':
            os.remove(filename)
        else:
            raise TypeError('invalid input')
    return

#file encryption
def encrypt_file(input_filename, master_pass, coding_method):
    global check_salt
    new_filename = input_filename + '.blnk'
    file_exists(new_filename)
    
    with open(input_filename, 'rb') as bigfile:
        print('encrypting...')
        for i, lines in enumerate(piecewise(bigfile, 2**16)):

            raw_data = list(lines)
            data_string = ''
            for line in raw_data:
                data_string += '*'.join([str(x) for x in line]) + '*'#this expects a single byte array
            data_string = data_string[:-1]
            split_str = [data_string[i:i+100] for i, x in enumerate(data_string) if (i % 100 == 0)]
            encrypted_chunks = []
            for chunk in tqdm.tqdm(split_str, desc='str chunks'):
                encrypted_chunk = getattr(coding_methods, coding_method).encrypt_chunk(chunk, master_pass)
                encrypted_chunks.append(encrypted_chunk)
            encrypted = str('\n'.join(encrypted_chunks))


            check_str = str(int(bytes(master_pass, "UTF-8"), 16)*check_salt)
            check_str = str(hashlib.md5(bytes(check_str, "UTF-8")).hexdigest())
            print(check_str)
            with open(new_filename, 'w') as f:
                f.write(check_str)#always 32 bytes
                f.write('0000000000000000')
                f.write(encrypted)
def decrypt_file(input_filename, master_pass, coding_method): 
    global pi_digits, check_salt
    new_filename = input_filename.split('.')[0] + '.decrypted.' + input_filename.split('.')[1]
    file_exists(new_filename)

    with open(input_filename, 'r') as bigfile:
        header = bigfile.read(32)
        check_str = str(int(bytes(master_pass, "UTF-8"), 16)*check_salt)
        check_str = str(hashlib.md5(bytes(check_str, "UTF-8")).hexdigest())
        if header != check_str:
            raise TypeError('incorrect passkey')
        
        print('decrypting...')
        for i, lines in enumerate(piecewise(bigfile, 2**16)):
            encrypted_lines = (''.join([str(x) for x in lines])).split('\n')
            decrypted_chunks = []
            for chunk in tqdm.tqdm(encrypted_lines, desc='str chunks'):
                decrypted_chunk = getattr(coding_methods, coding_method).decrypt_chunk(chunk, master_pass)
                if decrypted_chunk != None:
                    decrypted_chunks.append(decrypted_chunk)
                    full_string = ''.join(decrypted_chunks)
            decrypted_str = full_string.strip('*')

            data = [int(x).to_bytes(1, byteorder='little') for x in decrypted_str.split('*')]
            with open(new_filename, 'ab') as f:
                for byte in data:
                    f.write(byte)

if __name__ == '__main__':
    input_filename = input('filepath: ').strip('"')
    master_pass = input('passkey: ')
    coding_method = input('coding method: ')
    print('')
    file_extension = input_filename.split('.')[-1]
    if file_extension == 'blnk':
        decrypt_file(input_filename, master_pass, coding_method)
    else:
        encrypt_file(input_filename, master_pass, coding_method)