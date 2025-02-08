'''
runs test on methods in coding_methods.py
'''
import time, random, tqdm, numpy as np, matplotlib.pyplot as plt
import coding_methods

char_list = [chr(x) for x in range(32, 127)]

def test_method(method_name):
    test_num = 500
    test_speeds = []
    test_size_ratios = []

    for i in tqdm.tqdm(range(test_num)):
        test_string = (''.join([char_list[random.randint(0, len(char_list)-1)] for x in range(100)])).strip()
        test_password = (''.join([char_list[random.randint(0, len(char_list)-1)] for x in range(25)])).strip()

        start_time = time.time()
        for i in range(50): # test 25 times to get a more accurate time
            encrypted = getattr(coding_methods, method_name).encrypt_chunk(test_string, test_password)
            decrypted = getattr(coding_methods, method_name).decrypt_chunk(encrypted, test_password)
        test_time = (time.time() - start_time)/50

        test_speeds.append(len(test_string)//test_time)
        test_size_ratios.append(len(encrypted)/len(test_string))
        try:
            assert decrypted == test_string # test that the method is reversible
        except:
            print(f'{method_name} failed test, {decrypted} != {test_string}')
            raise AssertionError

    return(test_speeds, test_size_ratios)

if __name__ == '__main__':
    test_speeds, test_size_ratios = test_method(input('method name: '))
    
    print(f'median speed: {np.median(test_speeds)} characters per second')
    print(f'median size ratio: {np.median(test_size_ratios)}')
    plt.subplot(1, 2, 1)
    plt.boxplot(test_speeds)
    plt.title('speed')

    plt.subplot(1, 2, 2)
    plt.boxplot(test_size_ratios)
    plt.title('size ratios')
    plt.show()

