import os, random , optparse
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

def encrypt(key, filename):
    chunksize = 64*1024
    outputFile = filename
    filesize = str(os.path.getsize(filename)).zfill(16)
    IV = ""
    for i in range(16):
        IV += chr(random.randint(0,0xFF))
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    with open(filename, 'rb') as infile:
        with open(outputFile, 'wb') as outfile:
            outfile.write(filesize)
            outfile.write(IV)

            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - (len(chunk) % 16))
                outfile.write(encryptor.encrypt(chunk))
def decrypt(key, filename):
    chunksize = 64*1024
    outputFile = filename[11:]

    with open(filename, 'rb') as infile:
        filesize = long(infile.read(16))
        IV = infile.read(16)

        decryptor = AES.new(key, AES.MODE_CBC, IV)

        with open(outputFile, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break

                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(filesize)

def getKey(password):
    hasher = SHA256.new(password)
    return hasher.digest()


def Main():
    parser = optparse.OptionParser('''
    welcome -e for encryped -d for decryped''')
    parser
    parser.add_option('-e', dest='encryped', type="string", help="Ecryped Filed")
    parser.add_option('-d', dest='decryped',type="string",help="decryped files")
    options, args = parser.parse_args()
    if options.encryped:
        os.system("clear")
        filename = raw_input("File to encrypt: ")
        password = raw_input("Password: ")
        
        encrypt(getKey(password), filename)
        print "Done"
        prevName = filename
        newName = 'Encryped.bat'
        os.rename(prevName,newName)
    elif options.decryped:
        os.system("clear")
        filename = raw_input("File to Decrypt: ")
        password = raw_input("Password: ")
        decrypt(getKey(password), filename)
        
        print "Done"

    

        

        

    
if __name__ == '__main__':
    Main()