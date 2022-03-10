from cryptography.fernet import Fernet


def decrypt1(date, cipher_key):  # 进行解密
    if date[:2]=='b\'':
        print('123')
        date=date[2:]
        date=date[:-1]
        print(date)
    date = bytes(date, encoding='utf-8')
    print(date)
    print(cipher_key)
    decrypted_text='123'
    try:
     decrypted_text = Fernet(cipher_key).decrypt(date)
     decrypted_text = str(decrypted_text, encoding='utf-8')
    except:

     print(decrypted_text)
    return decrypted_text

print(decrypt1('gAAAAABiIyrX7NvXDWGoMlzgZnpP3QIlMGByNSNP_ZVcpRzMbt58cfx2ufocpEHwO92dVRrWoFn0K3MvQEaRg9cRF_wJkW309hfA_FAvb0X5ePs67TJj93tOXzzDSS5HdnhuKS15RqUn', '2IVu_AJrza19RuzIGBObXCXbh-0H3Fio4wonF36iebY='))