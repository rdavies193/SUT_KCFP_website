import os
import glob
import shutil
os.chdir('/Users/ecarli/OneDrive - Swinburne University/Work/Swinburne_Postdoc/Keck_STACK/Secretary/2026A/Assessments')

def copy_and_rename(src_path, dest_dir):
    """
    Copies a file to a destination directory, automatically renaming it if a
    file with the same name already exists by adding a counter (e.g., file(1).txt).

    Args:
        src_path (str): The full path to the source file.
        dest_dir (str): The path to the destination directory.
    """
    if not os.path.isfile(src_path):
        raise FileNotFoundError(f"Source file not found: {src_path}")
    
    if not os.path.isdir(dest_dir):
        raise NotADirectoryError(f"Destination directory not found: {dest_dir}")
        
    filename = os.path.basename(src_path)
    base, extension = os.path.splitext(filename)
    dest_path = os.path.join(dest_dir, filename)
    counter = 1

    while os.path.exists(dest_path):
        dest_path = os.path.join(dest_dir, f"{base}({counter}){extension}")
        counter += 1
        print(f"File exists. Trying new name: {dest_path}")
    
    shutil.move(src_path, dest_path)
    #print(f"Copied '{src_path}' to '{dest_path}'")

#2026A
proposals = ['W323','W418','W347','W350','W047','W031','W225','W421']
#make a dictionary of readers and their conflicts (from Google form)
readers = {'Alister': ['W031'],
           'Jeff': ['W347','W350'],
           'Themiya': ['W421'],
           'Ashley': []} #Ashley has no conflicts
#TODO next year add student member - need to ask them for their conflicts 

members = {'Jesse': [], #Jesse has no conflicts #I'm giving Jesse two proposals to lead W031 and W421
          'Ivo': [], #gave him W225
          'Darren': ['W347','W350'], #gave him W418
          'Karl': ['W225','W421'], #I randomly gave Karl two proposals to lead W323 and W350
          'Duncan': ['W418','W031'], #gave him W347
          'Agne': []} #Agne has no conflicts #I'm giving Agne one proposal to lead W047

technical_assessors = { 'Deanne': ['W047'],
                       'Jonah': ['W323','W418','W347','W350','W031','W225','W421']} #Jonah is doing TA for Deanne's only conflict W047 so I've put him as conflicted for all the rest


#First make directory for everyone and then I will manually put their evaluations in their folders
#CHeck that none of them put their names on!
#Make a copy of all this in a separate folder before moving files around
for reader in readers:
    os.makedirs(reader, exist_ok=True)

for member in members:
    os.makedirs(member, exist_ok=True)

for ta in technical_assessors:
    os.makedirs(ta, exist_ok=True)

#Check everyone's conflicts exist in the proposal list
for reader, conflicts in readers.items():
    for conflict in conflicts:
        assert conflict in proposals, f"Conflict {conflict} for reader {reader} not in proposal list"

for member, conflicts in members.items():
    for conflict in conflicts:
        assert conflict in proposals, f"Conflict {conflict} for member {member} not in proposal list"

for ta, conflicts in technical_assessors.items():
    for conflict in conflicts:
        assert conflict in proposals, f"Conflict {conflict} for technical assessor {ta} not in proposal list"


#Now make a folder for each proposal
for proposal in proposals:
    os.makedirs(proposal, exist_ok=True)

#Now move everyone's proposal assessments into the proposal folder
for reader, conflicts in readers.items():
    for proposal in proposals:
        if proposal not in conflicts:
            assessment = glob.glob(f'./{reader}/*{proposal}*')
            if assessment!=[]: 
                copy_and_rename(f'{assessment[0]}', f'./{proposal}/')
            else:
                print(f'No assessments found for proposal {proposal} by reader {reader}')
            if len(assessment)>1:
                print(f'Multiple assessments found for proposal {proposal} by reader {reader}')

for member, conflicts in members.items():
    for proposal in proposals:
        if proposal not in conflicts:
            assessment = glob.glob(f'./{member}/*{proposal}*')
            if assessment!=[]: 
                copy_and_rename(f'{assessment[0]}', f'./{proposal}/')
            else:
                print(f'No assessments found for proposal {proposal} by member {member}')
            if len(assessment)>1:
                print(f'Multiple assessments found for proposal {proposal} by member {member}')

for ta, conflicts in technical_assessors.items():
    for proposal in proposals:
        if proposal not in conflicts:
            assessment = glob.glob(f'./{ta}/*{proposal}*')
            if assessment!=[]: 
                copy_and_rename(f'{assessment[0]}', f'./{proposal}/')
            else:
                print(f'No assessments found for proposal {proposal} by technical assessor {ta}')
            if len(assessment)>1:
                print(f'Multiple assessments found for proposal {proposal} by technical assessor {ta}')

print('Check every assessors folder is empty')
print('Check each proposal folder looks OK and has a TA')

#Now we are going to give  a proposal discussion to  lead to each  member
#go back to the top and just attribute randomly, some will get more than 1
#make sure they are not conflicted 
#just state in the e-mail which ones they are leading
print(f'There are {len(proposals)/len(members)} proposals per each member')

#Now let's prepare packages for each member
for member, conflicts in members.items():
    os.makedirs(f'{member}_evaluation_package', exist_ok=True)
    for proposal in proposals:
        if proposal not in conflicts:
            src_dir = f'./{proposal}/'
            dest_dir = f'./{member}_evaluation_package/{proposal}/'
            shutil.copytree(src_dir, dest_dir, dirs_exist_ok=True)

print('Zip up evaluation packages.')

