import zipfile
import os


# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 50, fill = '█', printEnd = "\r"):
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
    print(get_files(directory="VCTK-Corpus"))