# Experimental downsync tool for SIIS 
**Author**: Frederic Pietowski \
**Version**: 1

This tool will temporarily disable ALL database triggers on the locally deployed SQLITE database, download all data from the central postgres database and save it in the local database. Once completed, the local trigger is re-enabled.

## Config
Configuration of the tool is done by **renaming** the supplied file ```config.default.ini``` to ```config.ini``` and providing the correct parameters. 
There are three section parameters, organized per component:
**POSTGRESQL**
* username: *The account name used to remotely access the POSTGRESQL database (remote view permission is required.)*
* password: *The password associated to the provided username*
* host: *The host name/ip address of the remote POSTGRESQL database*
* port: *The port number of the remote POSTGRESQL database*
* database: *The name of the remote POSTGRESQL database where the data for SIIS is aggregated.*
**SIIS**
* path = *The absolute path to the root directory where SIIS is installed. Recommended installation directory for SIIS is `C:\Workdir\MyApps\SIIS`*
* make_backup = *Boolean (True/False) flag. When set to ```True``` the program will create a backup of the entire data-folder and store a zipped copy referencing the machine-name and datetime. As long as the tool is in an experimental phase it's best to keep this setting to ```True```.*
**APPLICATION**
* verbose_warnings = *Boolean (True/False) flag. When set to ```True``` the program will halt execution before syncing alerting the user of some best practices.*

## Installation
After configuring the ```config.ini``` file the downsync tool can be deployed to all machines running SIIS. The downsync tool requires additional python modules which need to be installed in a virtual environment. 
* Make sure you have Python 3.12 installed, it should be available for all users and needs to be added to the system path for ease of use. On managed computers Python should be installed in ```C:\Workdir\MyApps\python``` by a user with local admin-rights. 
* Download and deploy this GitHub repository (e.g.: ```C:\Workdir\MyApps\python_venvs\downsync```).
* Open PowerShell as a Local Administrator and navigate to the folder where you deployed this repository. Type: ```python -m venv .```. Activate this environment by going to ```Scripts\activate```.
* When activated the name of the virtual environment should be shown in front of the path in your PowerShell Window. Install the required modules: ```pip install -r requirements.txt```

## Usage
The application should always be ran by using the virtual environment. There are two options of doing this:
### Option1: 
* Open a PowerShell window
* Navigate to the deployment location and activate the virtual environment as described above.
* Type ```python downsync.py``` to launch the program, follow the on-screen prompts. 

### Option2:
* This repo comes bundled with two ```.bat``` scripts which launch the environment by itself and run the application. All you need to do is double click the scripts. 
To initiate the downsync procedure, double click ```downsync_launcher.bat```

## Troubleshooting
The code is still in an experimental phase due to a limited amount of sync-events. The application completed its cycle if it shows ```Press enter to exit the application``` at the end of the Downsync process, any other message indicates a fault and should be remedied.
1) **Immediately halt downsyncing on all machines**. 
2) Revert to the backup which was made at the start of the downsync process. This backup is stored in the folder ```/backup/```. You should choose the most recent file. 
    - Unzip the backup file
    - Copy the content to the SIIS-data directory and override the files which are there.
