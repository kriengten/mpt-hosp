import pyqrcode

def qrcode():
    q = pyqrcode.create('kriengsak ten')
    q.png('kriqrcode.png',scale=6)
    print('qrcode generate')

if __name__ == '__main__':
    qrcode()