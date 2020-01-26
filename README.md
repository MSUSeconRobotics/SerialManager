# SerialManager
A process that runs in the background to handle the sending and receiving of USB data between a Raspberry Pi and an Arduino. Build to be independent of it's consumers, SerialManager uses a ReDis publish-subscribe structure so that any other process may request to send data.

#### Benefits:
- Prevent collisions between processes accessing Pi's serial port
- Ensure well formed data sending
- Queueing of requests
- Automatically establishes serial communication with recovery mechanisms

#### Items of note:
- Run-on-startup procedure is difficult to set up
- No serial operations are 'safe', cannot ensure transmission or reply
- Some manual configuration is necessary
  *  Baudrate
  *  Request channel name
  *  Timeout duration
- Port recovery may not currently work

This process was originally from a Mississippi State CSE Senior Project.

## How to set up
1) Clone this repository, or at least the .py file, into ~/SerialManager. If another location is preferred that is fine as long as you replace global references to your preferred location.  
2) Navigate to /etc/init.d  
3) As root, create a file similar to that in the SetupExamples folder. Please note the lack of file extension.
4) Whatever is under the 'start' command will be run at startup.
5) As root in a terminal, execute `update-rc.d <FileName> defaults` where \<FileName> is replaced by your file's name without the < >.
6) Test it! Run the service manually with `sudo /etc/init.d/<FileName start` and stop the service manually with `sudo /etc/init.d/<FileName> stop`  

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

Red names: Independent processes or threads
Rounded squares: USB ports
Sky blue ReDis components:
- Solid arrow: Publishing
- Dashed arrow: Reading from subscriptions
- Circles: Individual channels