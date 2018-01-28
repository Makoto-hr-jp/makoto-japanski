@echo off
for /r %%i in (*.pdf) do del %%i
for /r %%i in (*.synctex.gz) do del %%i