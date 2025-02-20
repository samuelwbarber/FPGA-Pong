# FPGA code
### This folder contains:
1. Top level code
2. sopcinfo for eclipse
3. Compiled quartus project

### Current functions:
- reads x-axis accelerometer data
- filters data and displays on leds
- scales data from -10 to 10
- sends data to local host in batches of 100

The local host code (fpga_host) then removes the unnecessary terminal output and returns the values.

Things to note:
- When generating BSP template, use Hello World (**not** Hello World Small)