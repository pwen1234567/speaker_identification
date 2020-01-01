import zipfile
import os
import itertools
import random
import shutil

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 50, fill = '#', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd, flush=True)
    # Print New Line on Complete
    if iteration == total: 
        print(flush=True)
        
def unzip(file_name, destination):
    with zipfile.ZipFile(file_name) as zip_file:
        members = zip_file.infolist()
        for i, member in enumerate(members):
            full_dest_member_path = os.path.join(destination, member.filename)
            """
            Prevent unzipping a member which is already unzipped
            """
            if not os.path.isfile(full_dest_member_path):
                zip_file.extract(member, destination)
            if i % 2000 ==0:
                printProgressBar(iteration=i, total=len(members))
        printProgressBar(iteration=len(members), total=len(members))
"""
Return a list containing full paths of all files under directory
"""
def get_files(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list
 
if __name__ == "__main__":
    if not os.path.isfile("VCTK-Corpus.zip"):
        raise ValueError("Cannot find VCTK-Corpus.zip. Please download VCTK-Corpus.zip from https://datashare.is.ed.ac.uk/handle/10283/2651")
    print("Unzip VCTK-Corpus.zip to VCTK-Corpus...", flush=True)
    unzip(file_name="VCTK-Corpus.zip", destination=".")
    
    """
    Grouping by folders
    """
    ratio = 0.75 ## Ratio of the training set
    print("Copy .wav files...", flush=True)
    for folder, file_list in itertools.groupby(get_files(directory="VCTK-Corpus"), lambda x: os.path.dirname(x)):
        
        """
        file_list returned by itertools.groupby() is a generatator. Turn it into a list
        """
        file_list = list(file_list)
        
        """
        Keep files with .wav extension
        """
        file_list = [x for x in file_list if os.path.splitext(x)[1]==".wav"] 
        
        """
        If file_list doesn't contain any .wav, then skip
        """
        if len(file_list) == 0:
            continue
        print(folder, flush=True)
        
        for_train = set(random.sample(file_list, k = int( len(file_list) * ratio)))
        for_test  = set(file_list) - set(for_train)
        
        for src in for_train:
            dst = os.path.join("train_data", src)
            try:
                shutil.copyfile(src=src, dst=dst)
            except IOError as io_err:
                os.makedirs(os.path.dirname(dst))
                shutil.copyfile(src=src, dst=dst)
            
            
        for src in for_test:
            dst = os.path.join("eval_data", src)
            try:
                shutil.copyfile(src=src, dst=dst)
            except IOError as io_err:
                os.makedirs(os.path.dirname(dst))
                shutil.copyfile(src=src, dst=dst)   
            

        
