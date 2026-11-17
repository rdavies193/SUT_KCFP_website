import os
import glob
import shutil
os.chdir('/Users/ecarli/OneDrive - Swinburne University/Work/Swinburne_Postdoc/Keck_STACK/Secretary/2027A/Evaluations')

def move_with_standard_name(src_path, dest_dir, proposal, role, index):
    """
    Moves a file to a destination directory using a standardized name format:
    {proposal}_{role}{index}{original_extension}

    Args:
        src_path (str): The full path to the source file.
        dest_dir (str): The path to the destination directory.
        proposal (str): The proposal ID (e.g. W322).
        role (str): The assessor role label (Reader, Member, TA).
        index (int): Sequential number within this proposal/role.
    """
    if not os.path.isfile(src_path):
        raise FileNotFoundError(f"Source file not found: {src_path}")
    
    if not os.path.isdir(dest_dir):
        raise NotADirectoryError(f"Destination directory not found: {dest_dir}")
        
    _, extension = os.path.splitext(os.path.basename(src_path)) #.pdf extension, basename is file name with extension.
    dest_path = os.path.join(dest_dir, f"{proposal}_{role}{index}{extension}")

    if os.path.exists(dest_path):
        raise FileExistsError(f"Destination file already exists: {dest_path}")
    
    shutil.move(src_path, dest_path)

#2027A
proposals = ['W229','W250', 'W268','W101','W259','W249','W002','W230','W030','W224']

#make a dictionary of people and their conflicts (from Google form)
readers = {'Ned Taylor': [], #no conflicts
           'Alister Graham': [], #no conflicts
           'Ivo Labbe': [],#no conflicts
           'Alma Sebastian': []} #no conflicts

members = {'Jesse van de Sande': [], #no conflicts, leads W230
          'Adam Deller': [], #no conflicts, leads W259, W249
          'Duncan Forbes': ['W030','W002'], #leads W229, W250
          'Karl Glazebrook': ['W249','W250','W268'], #leads W030, W224
          'Ashley Stock': [] ,#no conflicts #leads W101
          'Jeff Cooke': ['W229','W230'] #leads W268, W002
          } 

technical_assessors = { 
                       'Jeff TA': ['W229','W230'], #THESE ARE CONFLICTS !
                        'Deanne TA': ['W101','W259'],} #THESE ARE CONFLICTS !

# #run this without any files (stop code later)
# for reader in readers:
#     os.makedirs(reader, exist_ok=True)

# for member in members:
#     os.makedirs(member, exist_ok=True)

# for ta in technical_assessors:
#     os.makedirs(ta, exist_ok=True)

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

#STOP CODE HERE AND MANUALLY MOVE EVALUATIONS IN EACH PERSON'S FOLDER, THEN RESTART CODE BELOW
# CHeck that none of them put their names inside form!

#Now make a folder for each proposal
# for proposal in proposals:
#     os.makedirs(proposal, exist_ok=True)

#Now move everyone's proposal assessments into the proposal folder
for reader_idx, (reader, conflicts) in enumerate(readers.items(), start=1):
    for proposal in proposals:
        if proposal not in conflicts:
            assessment = glob.glob(f'./{reader}/*{proposal}*')
            if assessment!=[]:
                for filepath in sorted(assessment):
                    move_with_standard_name(
                        filepath,
                        f'./{proposal}/',
                        proposal,
                        'Reader',
                        reader_idx
                    )
            else:
                print(f'No assessments found for proposal {proposal} by reader {reader}')
            if len(assessment)>1:
                print(f'Multiple assessments found for proposal {proposal} by reader {reader}')

for member_idx, (member, conflicts) in enumerate(members.items(), start=1):
    for proposal in proposals:
        if proposal not in conflicts:
            assessment = glob.glob(f'./{member}/*{proposal}*')
            if assessment!=[]:
                for filepath in sorted(assessment):
                    move_with_standard_name(
                        filepath,
                        f'./{proposal}/',
                        proposal,
                        'Member',
                        member_idx
                    )
            else:
                print(f'No assessments found for proposal {proposal} by member {member}')
            if len(assessment)>1:
                print(f'Multiple assessments found for proposal {proposal} by member {member}')

for ta_idx, (ta, conflicts) in enumerate(technical_assessors.items(), start=1):
    for proposal in proposals:
        if proposal not in conflicts:
            assessment = glob.glob(f'./{ta}/*{proposal}*')
            if assessment!=[]:
                for filepath in sorted(assessment):
                    move_with_standard_name(
                        filepath,
                        f'./{proposal}/',
                        proposal,
                        'TA',
                        ta_idx
                    )
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

