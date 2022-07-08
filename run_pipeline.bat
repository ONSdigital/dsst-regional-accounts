@ECHO off
setlocal ENABLEDELAYEDEXPANSION
:: Import user specified variables

:: git related setup - repo will be created if it doesn't already exist
:: Note that none of these need to be set if running from inside the repo already
set local-repo-location=D:\Test_Repos&::enter the path to your repo here
set remote-repo-url=https://github.com/ONSdigital/easy_pipeline_run.git&::enter the URL of your repo here
set repo-name=easy_pipeline_run&::set the repo name. This should be exactly the name of the repo folder.

:: virtual env setup - virtual environment will be created if it doesn't exist already
set python-scripts-location=C:\Python36\Scripts&::enter the path of the scripts folder in the base installation of Python
set python-version=3.6.9&::enter the version of Python you are using, e.g. 3.6.8
set virtual-env-name=epr-369&::name your virutual environment e.g. my_proj_env

:: Choose the config file - should exist in the config folder witin the repo
:: Note that if none is set default_config.ini will be used
set config_file=default_config.ini

:: Location of the pip config file - this shouldn't need to be changed
set pip-config-location=%appdata%\pip

:: Check if .bat script is currently inside a git repo
IF EXIST ".git\" (
    set in_git_repo=1
) ELSE (
    set in_git_repo=0
)

ECHO In git repo value: %in_git_repo%
:: cd into correct location if not already in the repo
IF %in_git_repo%==0 (
    cd /d %local-repo-location% || ECHO ERROR - terminating script && pause && EXIT /b
)

:: Creating condarc file if it doesn't exist
IF NOT EXIST "%USERPROFILE%\.condarc" (
ECHO .condarc file does not exist, please supply artifactory login details.
set /P artifactory-username= "Enter artifactory username:"
set /P artifactory-encrypted-password= "Enter artifactory encrypted password:"
ECHO Creating .condarc file
(
    ECHO channels:
    ECHO   - http://!artifactory-username!:!artifactory-encrypted-password!@art-p-01/artifactory/list/RR_conda_main
    ECHO default_channels:
    ECHO   - http://!artifactory-username!:!artifactory-encrypted-password!@art-p-01/artifactory/list/RR_conda_main
    ECHO ssl_verify: true 
)>%USERPROFILE%\.condarc
)

:: Checking if python scripts folder exists (if file is outside a repo)
IF %in_git_repo%==0 (
IF NOT EXIST "%python-scripts-location%" (
    ECHO python-scripts-folder=%python-scripts-location% does not exist, please change to correct location in set variables.
    pause
    EXIT /b
)
)

:: Check if python scripts folder is in path variable
ECHO Checking if scripts folder is in the path

ECHO.;%PATH%; | find /C /I ";%python-scripts-location%;"
IF %ERRORLEVEL% EQU 0 (
    ECHO %python-scripts-location% already present in PATH env variable
) ELSE (
    IF EXIST "%python-scripts-location%" (
        ECHO %python-scripts-location% not present in PATH env variable, adding it now
        set "PATH=%python-scripts-location%;%PATH%"
        set ERRORLEVEL=0
    )
)

:: Check if pip (config) exists
IF NOT EXIST "%pip-config-location%\pip.ini" (
    ECHO %pip-config-location% does not exist
    :: Set artifactory variables if not done already
    IF NOT DEFINED artifactory-username (
        ECHO Please supply artifactory details for pip config
        set /p artifactory-username="Enter artifactory username:"
        set /p artifactory-encrypted-password="Enter artifactory encrypted password:"
    )
    ECHO %artifactory-username%, %artifactory-encrypted-password%
    IF NOT EXIST "%pip-config-location%" (
        ECHO Creating %pip-config-location% folder
        mkdir "%pip-config-location%"
    )
    :: Create pip config file
    ECHO creating pip config file
    (
    ECHO [global]
    ECHO trusted-host = art-p-01
    ECHO index-url = http://!artifactory-username!:!artifactory-encrypted-password!@art-p-01/artifactory/api/pypi/yr-python/simple
    )>"%pip-config-location%\pip.ini" || ECHO ERROR - likely that the pip folder does not exist - terminating script && pause && EXIT /b
)

:: Check if we are already inside a repo
IF %in_git_repo%==0 ( 
    :: Check if local repo location (folder) exists and create if not
    IF NOT EXIST "%local-repo-location%\%repo-name%" (
        ECHO Local repository not found. Creating it now.
        :: Clone git repo from user specified version
        git clone %remote-repo-url% || ECHO ERROR - terminating script && pause && EXIT /b
        ECHO repo cloned version %code-version-number% into %local-repo-location%\%repo-name%
    )
)

:: Check if environment exists by piping output of conda env list to variable and check (regex) if user specified environment name is in variable.
conda env list| findstr /c:%virtual-env-name%

IF %ERRORLEVEL% EQU 0 (
    ECHO Found existing %virtual-env-name% environment
    set check_env=found
) ELSE (
    ECHO Did not find the %virtual-env-name% environment - creating it now
    set check_env=not_found
    set ERRORLEVEL=0
)


:: If exists activate environment, else create a new one
IF NOT "%check_env%"=="found" (
    ECHO Creating environment %virtual-env-name%
    conda create -n %virtual-env-name% python=%python-version% -y || ECHO ERROR - terminating script && pause && EXIT /b
) 


:: Activate environment. Run pipeline.py in local repo from virtual env.
:activate
ECHO Activating environment, installing requirements, running pipeline
CALL activate %virtual-env-name%
:: Only checkout the version specified if the bat script is outside of a git repo
IF %in_git_repo%==0 (
    cd %repo-name% || ECHO ERROR - terminating script && pause && EXIT /b
)
pip install -r requirements.txt
python pipeline.py --config-file=%config_file%

CALL conda deactivate

ECHO End of batch script, press any button to exit.
pause
