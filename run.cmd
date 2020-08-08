@echo off
for %%i in (*.csv) do (
	python ReaperTimecodeExport.py "%%i" --nolog
	echo processed %%i
	)
@echo on