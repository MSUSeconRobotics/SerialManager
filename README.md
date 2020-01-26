# SerialManager
A process that runs in the background to handle the sending and receiving of USB data between a Raspberry Pi and an Arduino. Build to be independent of it's consumers, SerialManager uses a ReDis publish-subscribe structure so that any other process may request to send data.

This process was originally from a Mississippi State CSE Senior Project.

## How to set up

## How to use

## Structure
The Manager is listening to a dedicated requests channel. Whenever a process sends somethng to that channel, it will be added to the Manager's volatile queue. Processes will form their request with plain strings with no newline at the end. The format is `<Reply channel>:<Message>`  
Examples:
```
PiMon sensor data:Get sensors
motor_control:motors forward 255
.:raise flag
```
The Manager will send the message then publish the replied data from the Arduino to the provided reply channel name. There is a timeout, so if no reply is heard the Manager will continue.  

Please note that the Manager can **never guarantee** the sending of the message or returning any data. Make sure that processes can handle the failure case of the Arduino not being available or the Manager never returning any reply data.  

Below is a diagram of this structure:
![Block and arrow diagram depicting the Serial Manager's structure](/Pictures/SerialManagerDiagram.png)
