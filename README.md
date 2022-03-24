
There are many different scripts in here that need to be run in a specific order to work.

The msin plotting ones are in the root directory, but we first need to run the preprocessing ones in the `data/` folder.
Depending on if you ran your traces on a machine with GPUs, which logging library was used, how many worker processes were run, etc., you may not need to run some of them or create new ones. 
git