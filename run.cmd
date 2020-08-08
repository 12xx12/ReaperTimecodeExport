@echo off
for %%i in (*.csv) do (python ReaperTimecodeExport.py "%%i" --nolog)
@echo Now copy the two folders onto the gma2 folder on your USB-drive or internal storage and import the macro and run it
@echo on