# Hackathon Evaluation Scripts 
This repository contains the scripts used to evaluate the submissions
for the Hackathon accompanying the 2025 Spring School on *Physics Informed Machine Learning for Medical Sciences*.

## How to submit
To submit your solution for the hackathon task:
-  send the link to your **GitHub repository** that should be used for evaluation to the email address [magnet4cardiac7t@uni-wuerzburg.de](magnet4cardiac7t@uni-wuerzburg.de).

- Include the **name of your group** in your submission and the **names** of all participants.

- Make sure that your github repository is set to **public** so it can be cloned by the evaluation script (see below).

- Both your submission email as well as your last commit should be made on **Thursday, April 10th 6:30pm** at the latest 

## How to use
To run the evaluation clone this repository, make the `evaluation.sh` executable by running

> chmod +x evaluation.sh

After which you can run the evaluation by calling:

> ./evaluation.sh `URL_OF_YOUR_GITHUB_REPO`

e.g. `./evaluation.sh https://github.com/MAGNET4Cardiac7T/hackathon`

Remember to set your repository to public before the submission.

### What happens? 
The script will clone your repository, create a new virtual environment with the packages specified in your `requirements.txt` file in your repository and then run your optimization algorithm for each of the cost functions specified in `cost_list.txt` and all simulations listed in `data_list.txt` (which at evaluation time will contain unseen simulations).

The script calls the `run` method from the `main.py` script in your repository and expects a return value of type `CoilConfig`. 

The solution found by your algorithm(s) will then be evaluated using the reference code in this repository and compared against the default configuration (all phases 0 and all amplitudes 1).

## Scoring
For each combination of cost function and simulation, the submissions will be ranked based on the cost achieved using their respective solutions.
The overall rank of the submissions will be calculated based on the average rank over all dataset/cost function combinations.

## Disclaimer
This script only runs on Unix-based operating systems (probably).
To make sure that your algorithm evaluates correctly you should test your github repository using the provided evaluation scripts