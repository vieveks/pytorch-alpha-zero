import chess.pgn
import os

def reformat_games(file_names, new_dir):
    file_name_idx = 0

    for file_name in file_names:
        with open(file_name) as pgn_fh:
            while True:
                game = chess.pgn.read_game(pgn_fh)
                if not game:
                    break

                new_file_path = os.path.join(new_dir, '{}.pgn'.format(file_name_idx))
                with open(new_file_path, 'w') as new_pgn_fh:
                    print(game, file=new_pgn_fh, end='\n\n')

                file_name_idx += 1

                if file_name_idx % 1000 == 0:
                    print('Wrote {} train pgns'.format(file_name_idx))

# Proceeding to printing the directory
input('Proceeding to printing the directory, proceed?')

# Get all PGNs
current_directory = os.getcwd()
ccrl_dir = os.path.join(current_directory, 'cclr', 'train')
all_file_names = [os.path.join(ccrl_dir, file_name) for file_name in os.listdir(ccrl_dir)]

# The new directory
reformat_dir = os.path.join(current_directory, 'cclr', 'reformatted')

# Process files sequentially
reformat_games(all_file_names, reformat_dir)
