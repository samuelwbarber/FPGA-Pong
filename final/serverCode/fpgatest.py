import asyncio
import websockets

async def echo(websocket, path):
	async for message in websocket:
		print(f"Received message: {message}")
		if message.startswith("VALUE:"):  # Check if stop message is received
			values = message[6:]
			accelerometer_values = values.split()
			print(accelerometer_values)
		else: 
			await websocket.send("Unable to decode message")

start_server = websockets.serve(echo, "0.0.0.0", 6789)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


