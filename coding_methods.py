'''
this file contains the classes and functions used to encrypt and decrypt text
each class is a coding method, contaning two functions: encrypt_chunk and decrypt_chunk

each method should be benchmarked for speed and space efficiency
benchmarking should be done with a 100 character string and done 500 times
1 character is 0.4 bytes
'''


class hash_multiplication:
    '''
    this method multiplies turns the string into decimal, multiplies it by the hash of the master password, adds a salt value, and converts to base 64 for compression
    median speed: 260729.0 characters per second ; 9588 seconds per gigabyte
    median size ratio: 1.57 
    '''
    global pi_digits, b64, hashlib
    from b64 import b64
    import hashlib
    from mpmath import mp
    mp.dps = 100
    pi = mp.pi
    pi_digits = [*str(pi)]
    pi_digits.remove('.')
        
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
        text_encypted = b64(b10_value=salted).encode()
        return(text_encypted)
    def decrypt_chunk(full_string, master_password): 
        if full_string == '':
            return
        b10 = b64(b64_value = full_string).decode()
        master_password = str(master_password)
        salt = int(pi_digits[int(''.join([*str(b10)][0:2]))] )
        desalted = int(b10 - salt)
        m_hash = int(hashlib.md5(bytes(master_password, 'UTF-8')).hexdigest(), 16)
        dehashed = int(desalted // m_hash)

        binary = bin(int(dehashed))
        binary = binary[2:]
        cut_spaces = ''.join(['0' for x in range(0,8-(len([*str(binary)]) % 8))])
        binary = cut_spaces + binary
        binary_list = [binary[x:x+8] for x in range(0, len(binary)-1) if x % 8 == 0]
        string = ''.join([chr(int(x, base = 2)) for x in binary_list])
        return(string)
    
#