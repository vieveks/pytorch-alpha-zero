
import chess.pgn
import os
from threading import Thread
import time

#re-writes all the files into the new directory, using a unique thread id and an index for a new name
def reformat_games( file_names, new_dir, thread_idx ):
    file_name_idx = 0
    #Iterate over all file names
    while len( file_names ) > 0:
        pgn_fh = open( file_names.pop() )
        #iterate over all games in file
        while True:
            game = chess.pgn.read_game( pgn_fh )
            if not game:
                break
            print( game, file=open( os.path.join( new_dir, '{}_{}.pgn'.format( thread_idx, file_name_idx ) ), 'w' ), end='\n\n' )
            file_name_idx += 1
            if file_name_idx % 1000 == 0:
                print( 'Thread {} wrote {} train pngs'.format( thread_idx, file_name_idx ) )


input('proceeding to printing the directory, proceed ?')
#get all pgns
current_directory = os.getcwd()

# Construct the path to the 'cclr/train' directory using a relative path
ccrl_dir = os.path.join(current_directory, 'cclr', 'train')
# ccrl_dir = '../train'
# ccrl_dir = '..\\cclr\\train'
print(ccrl_dir)
all_file_names = os.listdir(ccrl_dir)
print(all_file_names)
for i in range( len( all_file_names ) ):
    all_file_names[ i ] = os.path.join( ccrl_dir, all_file_names[ i ] ) 
    print(all_file_names[i])

#the new dir
#reformat_dir = '../reformatted'
reformat_dir = os.path.join(current_directory, 'cclr', 'reformatted')

#launch some threads
threads = []
num_threads = 50
for i in range( num_threads ):
    files_per_thread = int( len( all_file_names ) / num_threads )
    threads.append( Thread( target=reformat_games,
        args=( all_file_names[ i * files_per_thread : (i + 1) * files_per_thread ],
            reformat_dir, i ) ) )
    threads[ i ].start()
    time.sleep( 0.0001 )

for i in range( num_threads ):
    threads[ i ].join()


