call cd ..
call conda env create -f environment.yml
call conda activate GenArt
call ipython kernel install --user --name=GenArt
pause