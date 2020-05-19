
import chess
import numpy as np

def encodePosition( board ):
    """
    Encodes a chess position as a vector. The first 12 planes represent
    the different pieces. The next 4 represent castling rights.
    Args:
        board (chess.Board) the position to be encoded.
    """
    planes = np.zeros( (16, 8, 8), dtype=np.float32 )

    #white pawns
    wPawns = board.pieces( chess.PAWN, chess.WHITE )
    wPawns = [ (chess.square_rank( sq ), chess.square_file( sq ) ) for sq in wPawns ]
    for r, f in wPawns:
        planes[ 0, r, f ] = 1.
    
    #black pawns
    bPawns = board.pieces( chess.PAWN, chess.BLACK )
    bPawns = [ (chess.square_rank( sq ), chess.square_file( sq ) ) for sq in bPawns ]
    for r, f in bPawns:
        planes[ 1, r, f ] = 1.
    
    #white rooks
    wRooks = board.pieces( chess.ROOK, chess.WHITE )
    wRooks = [ (chess.square_rank( sq ), chess.square_file( sq ) ) for sq in wRooks ]
    for r, f in wRooks:
        planes[ 2, r, f ] = 1.
    
    #black rooks
    bRooks = board.pieces( chess.ROOK, chess.BLACK )
    bRooks = [ (chess.square_rank( sq ), chess.square_file( sq ) ) for sq in bRooks ]
    for r, f in bRooks:
        planes[ 3, r, f ] = 1.
    
    #white bishops
    wBishops = board.pieces( chess.BISHOP, chess.WHITE )
    wBishops = [ (chess.square_rank( sq ), chess.square_file( sq ) ) for sq in wBishops ]
    for r, f in wBishops:
        planes[ 4, r, f ] = 1.
    
    #black bishops
    bBishops = board.pieces( chess.BISHOP, chess.BLACK )
    bBishops = [ (chess.square_rank( sq ), chess.square_file( sq ) ) for sq in bBishops ]
    for r, f in bBishops:
        planes[ 5, r, f ] = 1.
    
    #white knights
    wKnights = board.pieces( chess.KNIGHT, chess.WHITE )
    wKnights = [ (chess.square_rank( sq ), chess.square_file( sq ) ) for sq in wKnights ]
    for r, f in wKnights:
        planes[ 6, r, f ] = 1.
    
    #black knights
    bKnights = board.pieces( chess.KNIGHT, chess.BLACK )
    bKnights = [ (chess.square_rank( sq ), chess.square_file( sq ) ) for sq in bKnights ]
    for r, f in bKnights:
        planes[ 7, r, f ] = 1.
    
    #white queens
    wQueens = board.pieces( chess.QUEEN, chess.WHITE )
    wQueens = [ (chess.square_rank( sq ), chess.square_file( sq ) ) for sq in wQueens ]
    for r, f in wQueens:
        planes[ 8, r, f ] = 1.
    
    #black queens
    bQueens = board.pieces( chess.QUEEN, chess.BLACK )
    bQueens = [ (chess.square_rank( sq ), chess.square_file( sq ) ) for sq in bQueens ]
    for r, f in bQueens:
        planes[ 9, r, f ] = 1.
    
    #white kings
    wKings = board.pieces( chess.KING, chess.WHITE )
    wKings = [ (chess.square_rank( sq ), chess.square_file( sq ) ) for sq in wKings ]
    for r, f in wKings:
        planes[ 10, r, f ] = 1.
    
    #black kings
    bKings = board.pieces( chess.KING, chess.BLACK )
    bKings = [ (chess.square_rank( sq ), chess.square_file( sq ) ) for sq in bKings ]
    for r, f in bKings:
        planes[ 11, r, f ] = 1.

    #white can kingside castle
    if board.has_kingside_castling_rights( chess.WHITE ):
        planes[ 12, :, : ] = 1.
   
    #black can kingside castle
    if board.has_kingside_castling_rights( chess.BLACK ):
        planes[ 13, :, : ] = 1.
    
    #white can queenside castle
    if board.has_queenside_castling_rights( chess.WHITE ):
        planes[ 14, :, : ] = 1.
   
    #black can queenside castle
    if board.has_queenside_castling_rights( chess.BLACK ):
        planes[ 15, :, : ] = 1.

    return planes

def moveToIdx( move ):
    """
    Maps a legal move to an index in ( 72, 8, 8)
    Each of the 72 planes represents a different direction
    and distance: rook and bishop directions with distance (64 planes)
    and 8 horse directions.
    The location in the plane specifies the start square.
    Args:
        move (chess.Move) the move to be encoded.
    """

    from_rank = chess.square_rank( move.from_square )
    from_file = chess.square_file( move.from_square )
    
    to_rank = chess.square_rank( move.to_square )
    to_file = chess.square_file( move.to_square )

    if from_rank == to_rank and from_file < to_file:
        directionPlane = 0
        distance = to_file - from_file
        directionAndDistancePlane = directionPlane + distance
    elif from_rank == to_rank and from_file > to_file:
        directionPlane = 8
        distance = from_file - to_file
        directionAndDistancePlane = directionPlane + distance
    elif from_file == to_file and from_rank < to_rank:
        directionPlane = 16
        distance = to_rank - from_rank
        directionAndDistancePlane = directionPlane + distance
    elif from_file == to_file and from_rank > to_rank:
        directionPlane = 24
        distance = from_rank - to_rank
        directionAndDistancePlane = directionPlane + distance
    elif to_file - from_file == to_rank - from_rank and to_file - from_file > 0:
        directionPlane = 32
        distance = to_rank - from_rank
        directionAndDistancePlane = directionPlane + distance
    elif to_file - from_file == to_rank - from_rank and to_file - from_file < 0:
        directionPlane = 40
        distance = from_rank - to_rank
        directionAndDistancePlane = directionPlane + distance
    elif to_file - from_file == -(to_rank - from_rank) and to_file - from_file > 0:
        directionPlane = 48
        distance = to_file - from_file
        directionAndDistancePlane = directionPlane + distance
    elif to_file - from_file == -(to_rank - from_rank) and to_file - from_file < 0:
        directionPlane = 56
        distance = from_file - to_file
        directionAndDistancePlane = directionPlane + distance
    elif to_file - from_file == 1 and to_rank - from_rank == 2:
        directionAndDistancePlane = 64
    elif to_file - from_file == 2 and to_rank - from_rank == 1:
        directionAndDistancePlane = 65
    elif to_file - from_file == 2 and to_rank - from_rank == -1:
        directionAndDistancePlane = 66
    elif to_file - from_file == 1 and to_rank - from_rank == -2:
        directionAndDistancePlane = 67
    elif to_file - from_file == -1 and to_rank - from_rank == 2:
        directionAndDistancePlane = 68
    elif to_file - from_file == -2 and to_rank - from_rank == 1:
        directionAndDistancePlane = 69
    elif to_file - from_file == -2 and to_rank - from_rank == -1:
        directionAndDistancePlane = 70
    elif to_file - from_file == -1 and to_rank - from_rank == -2:
        directionAndDistancePlane = 71

    return directionAndDistancePlane, from_rank, from_file

def getLegalMoveMask( board ):
    """
    Returns a mask encoding the legal moves.
    Args:
        board (chess.Board) the chess position.
    """
    mask = np.zeros( (72, 8, 8), dtype=np.int32 )
    
    for move in board.legal_moves:
        planeIdx, rankIdx, fileIdx = moveToIdx( move )
        mask[ planeIdx, rankIdx, fileIdx ] = 1

    return mask

def mirrorMove( move ):
    """
    Mirrors a move vertically.
    Args:
        move (chess.Move) the move to be flipped
    """

    from_square = move.from_square
    to_square = move.to_square

    new_from_square = chess.square_mirror( from_square )
    
    new_to_square = chess.square_mirror( to_square )

    return chess.Move( new_from_square, new_to_square )

def encodeTrainingPoint( board, bestMove, winner ):
    """
    Encodes a position, move, and winner as vectors.
    Args:
        board (chess.Board) the chess position.
        bestMove (chess.Move) the best move from this position
        winner (int) the winner of the game. -1 means black won,
            0 means draw, 1 means white won.
    """

    #Flip everything if black's turn
    if not board.turn:
        board = board.mirror()
        winner *= -1
        bestMove = mirrorMove( bestMove )

    positionPlanes = encodePosition( board )

    planeIdx, rankIdx, fileIdx = moveToIdx( bestMove )

    bestMoveIdx = planeIdx * 64 + rankIdx * 8 + fileIdx

    return positionPlanes, bestMoveIdx, float( winner )
