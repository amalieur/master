#Code from ChatGPT

import timeit
import subprocess
import os, shutil

import global_variables

def measure_time_used_to_run_notebook(path_to_notebook, output_path):
    #Starting with deleting all existing files to make time usage fair
    FOLDERS_TO_EMPTY = [f"data/bus_data", f"data/chosen_data/{global_variables.CHOSEN_SUBSET_NAME}", f"data/hashed_data/{global_variables.CHOSEN_SUBSET_NAME}", f"code/experiments/results/{global_variables.CHOSEN_SUBSET_NAME}/lists", f"code/experiments/results/{global_variables.CHOSEN_SUBSET_NAME}/plots"]
    for folder_path in FOLDERS_TO_EMPTY:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print("Failed to remove %s. Reason: %s" % (file_path, e))

    command = f"jupyter nbconvert --to notebook --execute {path_to_notebook}"
    execution_time = timeit.timeit(lambda: subprocess.run(command, shell=True), number=1)
    with open(output_path, 'w') as file:
        file.write("Time spent to run notebook: " + str(execution_time) + " seconds.")
        file.write("\nName of dataset: " + str(global_variables.CHOSEN_SUBSET_DATAFILE))
        file.write("\nSize of dataset: " + str(global_variables.CHOSEN_SUBSET_SIZE))
        file.write("\nFrechet threshold distance: " + str(global_variables.FRECHET_THRESHOLD_DISTANCE))
        file.write("\nFrechet threshold number of trajectories in cluster: " + str(global_variables.THRESHOLD_NUMBER_OF_TRAJECTORIES))
        file.write("\nFrechet percentage of match between trajectories: " + str(global_variables.THRESHOLD_PERCENTAGE_OF_TRAJECTORY))
        file.close()

    #Ending with deleting the files used to prevent overload of files when susbet size is high
    FOLDERS_TO_EMPTY = [f"data/chosen_data/{global_variables.CHOSEN_SUBSET_NAME}", f"data/hashed_data/{global_variables.CHOSEN_SUBSET_NAME}"]
    for folder_path in FOLDERS_TO_EMPTY:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print("Failed to remove %s. Reason: %s" % (file_path, e))

if __name__=="__main__":
    path_to_notebook = "code/taxi-similarity.ipynb"
    output_path = "code/experiments/timing/"
    #change this name depending on what type of run is done
    output_file_name = "datset-7500-with-LSH.txt"
    measure_time_used_to_run_notebook(path_to_notebook, output_path+output_file_name)
