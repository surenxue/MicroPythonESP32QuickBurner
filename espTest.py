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
    msg = ''
    def func():
        portLock.acquire()
        if stdout:
            old_stdout = sys.stdout
            sys.stdout = stdout
            stdout.write(1)
        try:
            _erase_flash(port, chip)
        except Exception as e:
            msg = str(e)
        if stdout:
            stdout.write(msg)
            stdout.write(-1)
            sys.stdout = old_stdout
        portLock.release()
    threading.Thread(target=func).start()

def write_flash(port:str, file:str, chip:str="auto", stdout=None, start='0x1000'):
    """烧录文件"""
    def func():
        msg = ''
        portLock.acquire()
        if stdout:
            old_stdout = sys.stdout
            sys.stdout = stdout
            stdout.write(1)
        try:    
            _burn_file(port, file, chip, start)
        except Exception as e:
            msg = str(e)
            msg += '烧录失败,请检查是否进入下载模式\n'
        if stdout:
            stdout.write(msg)
            stdout.write(-1)
            sys.stdout = old_stdout
        portLock.release()
    threading.Thread(target=func).start()


if __name__ == "__main__":
    erase_flash("COM5")
    