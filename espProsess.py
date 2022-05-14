import subprocess, shlex
import threading

portLock = threading.Lock()

def erase_flash(port:str, chip="auto", stdout=None):
    command_line = f"esptool.exe --chip {chip} --port {port} --connect-attempts 3 erase_flash"
    args = shlex.split(command_line)
    thr = threading.Thread(target=process_loop, args=(args, stdout))
    thr.start()
    # process_loop(args, stdout)

def write_flash(port, file, chip="auto", stdout=None):
    command_line = f"esptool.exe --chip {chip} --port {port} --baud 460800 \
                        --connect-attempts 3 write_flash -z 0x1000 {file}"
    args = shlex.split(command_line)
    thr = threading.Thread(target=process_loop, args=(args, stdout))
    thr.start()
    # process_loop(args, stdout)

def process_loop(args, stdout=None):
    """进程循环"""
    portLock.acquire()
    proc = subprocess.Popen(args,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="gbk")
    if stdout:
        stdout(1)
    while True:
        line = proc.stdout.read(1)
        if line:
            # print("STDOUT:"+line)
            if stdout:
                stdout(line)
        try:
            proc.wait(0.1)
            if not line:
                proc.terminate()
                break
        except BaseException as e:
            pass
    stdout(-1)
    portLock.release()
