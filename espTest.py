"""调用线程进行烧录，并重定向输出信息"""
import esptool
import threading
import sys
portLock = threading.Lock()

def _erase_flash(port:str, chip:str="auto"):
    command = ['--chip', chip, '--baud', '460800', '--port', port, '--connect-attempts', '3', 'erase_flash']
    print('Using command %s' % ' '.join(command))
    esptool.main(command)

def _burn_file(port:str, file:str, chip:str="auto", start='0x1000'):
    command = ['--chip', chip, '--baud', '460800', '--port', port, '--connect-attempts', '3', 'write_flash', '-z', start, file]
    print('Using command %s' % ' '.join(command))
    esptool.main(command)

def erase_flash(port:str, chip:str="auto", stdout=None):
    '''清空内存'''
    def func():
        portLock.acquire()
        if stdout:
            old_stdout = sys.stdout
            sys.stdout = stdout
            stdout.write(1)
        _erase_flash(port, chip)
        if stdout:
            stdout.write(-1)
            sys.stdout = old_stdout
        portLock.release()
    threading.Thread(target=func).start()

def write_flash(port:str, file:str, chip:str="auto", stdout=None, start='0x1000'):
    """烧录文件"""
    def func():
        portLock.acquire()
        if stdout:
            old_stdout = sys.stdout
            sys.stdout = stdout
            stdout.write(1)
        _burn_file(port, file, chip, start)
        if stdout:
            stdout.write(-1)
            sys.stdout = old_stdout
        portLock.release()
    threading.Thread(target=func).start()


if __name__ == "__main__":
    erase_flash("COM5")
    