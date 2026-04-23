import os
import glob
import shutil
os.chdir('/Users/ecarli/OneDrive - Swinburne University/Work/Swinburne_Postdoc/Keck_STACK/Secretary/2026B/Assessments')

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

#2026B
proposals = ['W322','W353','W354','W355','W231','W323','W325','W196','W317','W333']

#make a dictionary of people and their conflicts (from Google form)
readers = {'Ned Taylor': [], #no conflicts 
           'Alister Graham': [], #no conflicts 
           'Ivo Labbe': [],#no conflicts
           'Michael Murphy': ['W196'],
           'Jeff Cooke' : ['W353','W354','W355'],
           'Ashley Stock': []} #no conflicts

members = {'Jesse van de Sande': [], #no conflicts, leads W322, W325
          'Adam Deller': [], #no conflicts, leads W353
          'Warrick Couch': ['W322','W323','W325'], #leads W354, W196
          'Karl Glazebrook': ['W196','W317'], #leads W355, W317
          'Agne Semenaite': [] ,#no conflicts #leads W323
          'Daniel Reardon': [],} #leads W231, W333

technical_assessors = { 
                       'Jeff TA': ['W353','W354','W355'], #THESE ARE CONFLICTS !
                        'Deanne TA': ['W231'],} #THESE ARE CONFLICTS !


# First make directory for everyone and then I will manually put their evaluations in their folders
# CHeck that none of them put their names on!
# Make a copy of all this in a separate folder before moving files around
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

