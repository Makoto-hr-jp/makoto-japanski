@echo off
for /r %%i in (*.synctex.gz) do (
  echo removing %%i
  del %%i
)