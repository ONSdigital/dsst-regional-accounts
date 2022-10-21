# DSST - Regional Accounts Project 
Project completed by Chloe Murrell (August 2022) using Python 3.8.3.

This project aimed to build a Python script to automate manual processing of data within excel which was carried out by the regional account team (P1 and P2 spreadsheets). 

# Developer guide
### Relevant Spreadsheets
The spreadsheets which have been used for this project are stored on the DSST confluence page [Regional Accounts - DSST Confluence Page](https://confluence.ons.gov.uk/pages/viewpage.action?spaceKey=DDSST&title=Regional+Accounts+Pythonising+Spreadsheets). 

**Input P1 AND P2.xlsx** – This is the input tax data for P1 and P2 which is produced by the public sector and sent to the regional accounts team.

**Calculations P1 AND P2.xlsx** – This spreadsheet contains the manual calculations which were carried out (this is all now automated through the Python script). 

**Output P1_P2_RA_BB21.xlsx** – This is the processed spreadsheet and is now the output file of the script. 

### GitHub page
The development for this project has been completed on this GitHub page. 

### Batch script 
A batch script (run_pipeline.bat) has been set up to make it easier for the business area to run the pipeline. 

### Python script
The Python script takes the input file performs the necessary calculations (aggregates (sum) the data based on SIC code) and then produces the output file. 
Within the repository there is a folder called [dsst_regional_accounts](https://github.com/ONSdigital/dsst-regional-accounts/tree/main/dsst_regional_accounts) which contains the two main Python file scripts. 

**pipline.py** – This file contains the run function which runs all necessary functions to produce the output file. This script although contains the processing functions to manipulate and calculate the data.  

**data_import.py** – This script contains the functions to load the config file, read in the input data (excel file) and export the output data back to an excel file. 

There is also a separate config folder which contains a config yaml. This has been included to make it easier for the business area to edit necessary variables.  


# User guide
This section contains the instructions for producing the final output spreadsheet for P1 and P2 regional accounts using the pipeline created in Python.  

### Install Anaconda and git 
Before being able to run or interact with the pipeline, you will need to download Anaconda (with Python included) to enable running of the code and git to assist with management of the codebase (and development). On an ONS machine this needs to be installed via a service desk request. 
Details on how to do this can be found [here](http://np2rvlapxx507/BPI/coding-getting-started-guide/-/wikis/Service-desk-requests#software-install) (just the Software install section).

### Artifactory 
If you haven’t already set up a .condarc file when running the script for the first time you will need to enter your artifactory username and encrypted password. Therefore, before attempting to run the script ensure you have this to hand. Instructions on how to find this information are below.
This is the link for [ONS Artifactory](http://art-p-01/artifactory/webapp/#/login). You can log in using your window credentials. To find your encrypted password follow these steps:
1.	Click on your username in the top right-hand corner. 
2.	Type in your windows password to the ‘Current Password’ box. 
3.	Click Unlock to view your encrypted password. 
4.	This can be copied and pasted into the batch script when required.  
 a.	Windows username  
 b. Artefactory excrypted password

### GitHub
The repository for this project is stored on GitHub. Therefore, if you don’t already have an account you will need to set one up [GitHub](https://github.com/).
Once you have an account you will need your username and personal access token. If you do not already have a personal access token, you will need to create one by following the steps below:
1.	Click on profile icon in the top right-hand corner.
2.	Go to ‘Settings’ – second from the bottom.
3.	Scroll to the bottom of the page and click ‘Developer settings’ on the left-hand side.
4.	Go to ‘Personal access tokens’.
5.	‘Generate new token’
6.	Choose an expiration date 
7.	In the ‘Select scope’ section tick ‘repo’ and ‘user’.
8.	This will then produce a token which you must copy and save somewhere as you won’t be able to see it again and you will need to use it later. 

## Setting up the repository for the first time
### Create folder
Within your C drive, create a folder where you would like to keep the repository and files. In this folder save the batch script which you should have received. 

### Edit batch script 
Before the batch script can be run there are a few file paths which need changing. In order to edit the batch script click on the file, then right click and edit (opening in Notebook is the easiest format). 

Step 1: Change the local-repo-location
This needs the be the file path to the folder you have just created with the batch script in it. To find the file path go to the file explorer and into the folder. Left click in the file path box. Copy and paste this into the batch script for the ‘local-repo-location’ (see screenshot below). 

![image](https://user-images.githubusercontent.com/97117990/186367714-082b4e96-eb53-42b7-88a3-b1c13347b408.png)

Step 2: Change the file path of your python-script-location
This probably won’t need to be changed. If C:\Python36\Scripts exists on your local machine nothing will need changing. If this doesn’t exist when running the batch script, the following error will be raised.

![image](https://user-images.githubusercontent.com/97117990/186367748-3e4f5a00-12af-482f-b004-3a7db4122531.png)
 
If this error occurs, you will need to find where your Python/Anaconda installation is and set your python-script-location variable to the corresponding Scripts folder. Another common location is C:\Users\<username>\Anaconda\Scripts. Alternatively, you can run the following in Anaconda prompt to find the Python installation and then navigate to the Scripts folder. 

```python
where python 
```

### Batch script 
The pipeline can be run by simply double clicking on the batch script. 
When running for the first time you may be prompted to enter your artifactory and GitHub details. Instructions on finding these details are explained above in the respective sections. 
 
![image](https://user-images.githubusercontent.com/97117990/186367829-f04a7e07-4a97-4ae1-b455-e0262eb9ccac.png)

If this occurs enter you artifactory username and then your encrypted password.

![image](https://user-images.githubusercontent.com/97117990/186367858-c0480be4-57d3-43ce-8dea-7509fe519735.png)
 
If prompted for your GitHub details enter your username and when asked for your password, paste in your personal access token. Note that when you paste it won’t show anything so be careful to only paste once.
You will then get the error below which is expected as there is currently no data in the specified file paths. This means the repository has been successfully cloned. This local repository can now be used to return the output data. To produce the output data, follow the instructions below.   

![image](https://user-images.githubusercontent.com/97117990/186367898-b5528bf7-283d-4c38-981d-c0bed585df57.png)

## Running the script to get the output data
### Input data
In the folder which you have created, there should now also be a folder called dsst-regional-accounts. Within this folder, there is an input_data folder which you should store the input file for the pipeline. 

### Config file 
The last thing which needs editing is the config.yaml file which can be found in the repository (dsst-regional-accounts), ‘config’ folder. To edit the file, click on the file and then right click -> edit -> open in Notebook. The file should look like the screenshot below.
These variables have all been put in the config file to make them easy to change. 

![image](https://user-images.githubusercontent.com/97117990/186367987-6346addd-afc1-4ab2-afca-f59a1cce76f0.png)

**input_path** – If the input data has been saved correctly in the input_data folder only the second part of this variable will need changing to the name of the input file. Eg. input_data\File_Name.xlsx
**P1_delete_top_rows** – This should be equal to the number of rows before the years row in the input folder. This is currently set to 6 as there are 6 rows before the data rows (see screenshot).

![image](https://user-images.githubusercontent.com/97117990/186368275-da78049d-bbcf-41ce-9d8b-c27a8acc980a.png)

**P2_delete_top_rows** – This is similar the variable above but for the P2 sheet within the input_data. This is currently set to 0 but if the input data changes format this will need to be changed. 
**start_year** – This should be the earliest year required in the output data.
**end_year** – This should be the most recent year required in the output data.
**output_path** – Only the second part of this needs changing to be the name you would like the output file to be called. 
**sheet_1_name** – This should be the name of the sheet in the output excel file for the data relating to P1.
**sheet_2_name** - This should be the name of the sheet in the output excel file for the data relating to P2.

After the variables have been edited make sure you save the changes. 

### Running the batch script
You should now be able to double click on the batch script and once it has run the output file should be in the output_data folder. To ensure this is the up-to-date file check the date and time the file was created. This can be copied and pasted to a new location if required.

![image](https://user-images.githubusercontent.com/97117990/186368706-b1c7932e-c96c-423c-bd91-7ce2933f4d8f.png)

When repeating this process each year the new input data from public sector can be saved in the input_folder, as long as the variables are changed in the config file this process can be repeated multiple times and each output file will be save in the output folder. 

### Troubleshooting  

**Environment issues**  
Possible issue with conda setup file
 -Backup the following file (e.g. change the file name to '.condarc_old'):  
   C:\Users\<username>\.condarc  
   
**Error at pandas pip install stage**  
Error codes:  
•	401 Credentials error  
•	Cannot import pd  

Possible issue with pip.ini artefactory username and password.
1.	Open the “Run” box in windows  
a.	Win key + R
2.	Open ‘Pip’ folder
3.	WARNING: This can mess with previous manually setup entries, check the file first  
a.	Backup the existing file pip.ini  (e.g. change the file name to 'pip_old.ini')

