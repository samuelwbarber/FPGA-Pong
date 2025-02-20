# import subprocess
import sys
import intel_jtag_uart
import time
# import asyncio
# import websockets

def send_on_jtag(cmd):
    assert len(cmd) >= 1, "Please make the cmd a single character"

    try:
        ju = intel_jtag_uart.intel_jtag_uart()

    except Exception as e:
        print(e)
        sys.exit(0)

    ju.write(b'0')
    i = 0

    while True:
        vals = (ju.read()).replace(bytes('\n', "utf-8"), bytes(' ', "utf-8"))
        vals = (vals[-4:-2]).decode("utf-8")

        print(vals)
        ju.flush()
        # time.sleep(0.1)
        ju.write(b'a')
        # input = str(i)
        # ju.write(bytes(input, "utf-8"))
        # i = i + 1
        # print("i: " + input)
        # if i == 4:
        #     ju.write(b'w')
        # elif i == 5:
        #     ju.write(b'l')
        #     i = 0

def perform_computation():
    send_on_jtag("test")


def main():
    perform_computation()


if __name__ == "__main__":
    main()
