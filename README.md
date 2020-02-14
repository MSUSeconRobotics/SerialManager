# SerialManager
A process that runs in the background to handle the sending and receiving of USB data between a Raspberry Pi and an Arduino. Build to be independent of it's consumers, SerialManager uses a Redis publish-subscribe structure so that any other process may request to send data.

#### Benefits:
- Prevent collisions between processes accessing Pi's serial port
- Ensure well formed data sending
- Queueing of requests
- Automatically establishes serial communication with recovery mechanisms

#### Items of note:
- Run-on-startup procedure is difficult to set up
- No serial operations are 'safe', cannot ensure transmission or reply
- Permissions can be finicky, check for root vs. user permissions
- Some manual configuration is necessary
  *  Baudrate
  *  Request channel name
  *  Timeout duration
- Port recovery may not currently work

This process was originally from a Mississippi State CSE Senior Project.

## How to set up
Prior to this, it may require a similar process to establish the Redis server. I do not know.

Install Pipenv onto the Pi:
1) Ensure pip is using python3 with `pip --version`
2) Install pipenv with `sudo -H pip install -U pipenv`

Install the Repository:
1) Clone this repository by running `git clone https://github.com/MSUSeconRobotics/SerialManager.git` Note this file's location so that you can execute the python script.  
2) In the script's directory, run `sudo pipenv install --dev`  
3) Navigate to /etc/init.d  
4) As root, create a file similar to that in the SetupExamples folder. Please note the lack of file extension.
5) Whatever is under the 'start' command will be run at startup.
6) As root in a terminal, execute `sudo update-rc.d <FileName> defaults` where \<FileName> is replaced by your file's name without the < >.
7) Test it! Run the service manually with `sudo /etc/init.d/<FileName start` and stop the service manually with `sudo /etc/init.d/<FileName> stop`  

## How to use
### init.d
The set up should automatically run the file in /etc/init.d and /etc/rc2.d on startup. Run the service manually with `sudo /etc/init.d/<FileName start` and stop the service manually with `sudo /etc/init.d/<FileName> stop`  
Currently untested, but additional cases might be adle to be added to the /etc/init.d file for more custom commands such as restarting.

### Pipenv
To run the python script, run it using pipenv. This creates a veritual environment that automatically has the packages described in the pipfile. The advantage is that the Pi only needs pipenv installed, and pipenv will handle any other library needed.  

To run the python script with pipenv, navigate to the directory, call `pipenv run <terminal command>`, an example is `pipenv run python app.py`.  
Alternatively, you can run `pipenv shell` and have access to a terminal in the pipenv virtual environment.

---

## Maintenance
Below will describe how the system works and how to expand upon it.

### How to Develop
If a new library or external service is added, it must be added to the pipfile. This is done by navigating to the directory, running `pipenv shell`, then running `pipenv install <library name>`
Once all the needed libraries have been installed, run `pipenv lock` to solidify the changes.

### Structure
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
Sky blue Redis components:
- Solid arrow: Publishing
- Dashed arrow: Reading from subscriptions
- Circles: Individual channels