:: Check for Python Installation
python --version 2>NUL
if errorlevel 1 goto errorNoPython

:: Reaching here means Python is installed.
:: Ensure all dependencies are installed
pip3 install -r requirements.txt

echo Setup complete! 

:: Ending
PAUSE

:: Once done, exit the batch file -- skips executing the errorNoPython section
goto:eof

:errorNoPython
echo Error^: Python not installed. Install Python at https://www.python.org/downloads/

:: Ending
PAUSE