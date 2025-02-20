import subprocess
import sys
import asyncio
import websockets
import intel_jtag_uart
import time

def send_on_jtag():
    try:
        ju = intel_jtag_uart.intel_jtag_uart()

    except Exception as e:
        print(e)
        sys.exit(0)

    return ju

async def play(CLIENT="0"):
    uri = "ws://ec2-18-134-74-28.eu-west-2.compute.amazonaws.com:6789"
    message = 0

    async with websockets.connect(uri) as websocket:
        ju = send_on_jtag()
        ju.write(b'r')
        time.sleep(0.3)

        while True:
            vals = (ju.read()).replace(bytes('\n', "utf-8"), bytes(' ', "utf-8"))
            
            vals = (vals[-12:-8]).decode("utf-8")

            ju.flush()
            time.sleep(0.15)
            
            await websocket.send("VALUE: " + vals)    #sending value
            
            response = await websocket.recv()
            
            if response.startswith("SCORE:"): 
                score = response[6:]
                print("SCORE: " + score)
            else:
                print("Score not received")
asyncio.get_event_loop().run_until_complete(play())
asyncio.get_event_loop().run_forever()
