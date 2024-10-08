import numpy as np

# Defining A Class "Shape" which will store the amount of times the pieces move
# as well as the rotation that the user will eventually input.
class Shape:

    def __init__(self, rotations):
        self.rotations = rotations
        self.rot_Count = len(rotations)

    def get_Matrix_And_Offset(self, rotation, offset):
        return offset + self.rotations[rotation]

# A function which defines a blocks rotational movement during play
def generating_Blocks():

    # Block Shape [I]
    block_I_Rotation1 = np.array([[1, 0],[1, 1],[1, 2],[1, 3]], np.int32)
    block_I_Rotation2 = np.array([[0, 1],[1, 1],[2, 1],[3, 1]], np.int32)
    block_I = Shape(np.array([block_I_Rotation1,
                              block_I_Rotation2]))

    # Block Shape [L]
    block_L_Rotation1 = np.array([[1, 0],[1, 1],[1, 2],[2, 2]], np.int32)
    block_L_Rotation2 = np.array([[0 ,2],[1, 2],[2, 2],[2, 1]], np.int32)
    block_L_Rotation3 = np.array([[1, 0], [2, 0], [2, 1], [2, 2]], np.int32)
    block_L_Rotation4 = np.array([[0, 3], [0, 2], [1, 2], [2, 2]], np.int32)
    block_L = Shape([block_L_Rotation1,
                     block_L_Rotation2,
                     block_L_Rotation3,
                     block_L_Rotation4])

    # Block Shape [J]
    block_J_Rotation1 = np.array([[2, 0], [2, 1], [2, 2], [1, 2]], np.int32)
    block_J_Rotation2 = np.array([[0, 1], [1, 1], [2, 1], [2, 2]], np.int32)
    block_J_Rotation3 = np.array([[3, 0], [2, 0], [2, 1], [2, 2]], np.int32)
    block_J_Rotation4 = np.array([[0, 1], [0, 2], [1, 2], [2, 2]], np.int32)
    block_J = Shape(np.array([block_J_Rotation1,
                     block_J_Rotation2,
                     block_J_Rotation3,
                     block_J_Rotation4]))

    # Block Shape [S]
    block_S_Rotation1 = np.array([[0, 2], [1, 2], [1, 1], [2, 1]], np.int32)
    block_S_Rotation2 = np.array([[1, 0], [1, 1], [2, 1], [2, 2]], np.int32)
    block_S = Shape(np.array([block_S_Rotation1,
                              block_S_Rotation2]))

    # Block Shape [Z]
    block_Z_Rotation1 = np.array([[0, 1], [1, 1], [1, 2], [2, 2]], np.int32)
    block_Z_Rotation2 = np.array([[2, 0], [2, 1], [1, 1], [1, 2]], np.int32)
    block_Z = Shape(np.array([block_Z_Rotation1,
                              block_Z_Rotation2]))

    # Block Shape [T]
    block_T_Rotation1 = np.array([[0, 2], [1, 2], [2, 2], [1, 1]], np.int32)
    block_T_Rotation2 = np.array([[2, 0], [2, 1], [2, 2], [1, 1]], np.int32)
    block_T_Rotation3 = np.array([[0, 1], [1, 1], [2, 1], [1, 2]], np.int32)
    block_T_Rotation4 = np.array([[1, 0], [1, 1], [1, 2], [2, 1]], np.int32)
    block_T = Shape(np.array([block_T_Rotation1,
                     block_T_Rotation2,
                     block_T_Rotation3,
                     block_T_Rotation4]))

    # Block Shape [O]
    block_O_Rotation1 = np.array([[1, 1], [1, 2], [2, 1], [2, 2]], np.int32)
    block_O = Shape(np.array([block_O_Rotation1]))

    ## We are going to return a list of all shape rotations to be playable in Pytris.
    ## There should be 7 in total
    a_List_Of_all_Block_Rotations = list([block_I, block_L, block_J, block_S,
                                                   block_Z, block_T, block_O])

    return a_List_Of_all_Block_Rotations

# A function which defines the colors of the blocks
# Returns an entire list of the colors.
def block_Colors():

    RED    = [255, 0, 0]
    GREEN  = [0, 255, 0]
    BLUE   = [0 ,0, 255]
    OLIVE  = [128, 128, 0]
    ORANGE = [255, 165, 0]
    YELLOW = [204, 204, 0]
    WHITE  = [125, 125, 125]

    a_List_Of_All_Colors = list([RED, GREEN, YELLOW, BLUE, OLIVE, ORANGE, WHITE])

    return a_List_Of_All_Colors