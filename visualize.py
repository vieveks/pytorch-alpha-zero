
import argparse
import chess
import torch
import encoder
import numpy as np
import AlphaZeroNetwork

def main():

    parser = argparse.ArgumentParser(description='View a self play game using the network.')
    parser.add_argument( '--model', help='Path to model (.pt) file.' )
    parser = parser.parse_args()

    alphaZeroNet = AlphaZeroNetwork.AlphaZeroNet( 5, 64 )

    alphaZeroNet.load_state_dict( torch.load( parser.model ) )

    alphaZeroNet = alphaZeroNet.cuda()

    for param in alphaZeroNet.parameters():
        param.requires_grad = False

    alphaZeroNet.eval()

    board = chess.Board()

    while True:

        if board.is_game_over():
            print( 'Game over. Winner: {}'.format( board.result() ) )
            board.reset_board()
            c = input( 'Enter any key to continue ' )

        value, move_probabilities = encoder.callNeuralNetwork( board, alphaZeroNet )

        print( 'Whites turn: {}'.format( board.turn ) )
        print( 'Win probability: {}'.format( value ) )
        print( board )

        choice = np.argmax( move_probabilities )

        for idx, move in enumerate( board.legal_moves ):
            if idx == choice:
                board.push( move )
                break

        c = input( 'Enter any key to continue' )

if __name__=='__main__':
    main()