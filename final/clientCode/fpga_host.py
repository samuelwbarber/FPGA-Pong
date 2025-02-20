import subprocess
import sys
import pexpect
# import asyncio
# import websockets

NIOS_CMD_SHELL_BAT = "C:/intelFPGA_lite/18.1/nios2eds/Nios II Command Shell.bat"

def send_on_jtag(cmd):
    # check if atleast one character is being sent down
    assert (len(cmd) >= 1), "Please make the cmd a single character"

    # create a subprocess which will run the nios2-terminal
    process = subprocess.Popen(
        NIOS_CMD_SHELL_BAT,
        shell=True,
        bufsize=1,
        universal_newlines=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )

    # send the cmd string to the nios2-terminal, read the output and terminate the process
    try:
        process.stdin.write("nios2-terminal <<< {}".format(cmd))
        process.stdin.flush()

        while True:
            # print('TEST')
            vals = process.stdout.readline()
            if process.poll() is not None:
                break
            # for line in iter(process.stdout.readline, b''):
            #     print(">>> " + line)
            # vals = vals.decode("utf-8")
            # if not vals:
            #     print('broken')
            print (vals)
        # vals, err = process.communicate(
        #     bytes("nios2-terminal <<< {}".format(cmd), "utf-8")
        # )
    except subprocess.TimeoutExpired:
        vals = "Failed"
        process.terminate()

    # start = vals.find(bytes('vals:', "utf-8"))
    # end = vals.find(bytes('nios2-terminal: exiting', "utf-8"))
    # vals = vals[start:end]
    # vals = vals.replace(bytes('\r\n', "utf-8"), bytes(' ', "utf-8"))

    return vals

def perform_computation():
    res = send_on_jtag("test")
    # you can process the output here
    # ie send accelerometer data
    print(res)


def main():
    perform_computation()


if __name__ == "__main__":
    main()
