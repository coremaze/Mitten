import sys
import struct
def main():
    PORT_LOCATION = 0x27C10
    if len(sys.argv) != 2:
        print('USAGE: ServerPortSwitcher.py <Server.exe>')
        fileName = input('Enter server path: ')
    else:
        fileName = sys.argv[1]
    with open(fileName, 'r+b') as f:
        if len(f.read()) != 1718784:
            print("Incorrect server verson.")
            return
        f.seek(PORT_LOCATION)
        originalPort, = struct.unpack('<I', f.read(4))
        print(f'Original port is {originalPort}.')
        newPort = int(input("Enter new port: "))
        f.seek(PORT_LOCATION)
        f.write(struct.pack('<I', newPort))
    
if __name__ == '__main__':
    main()
