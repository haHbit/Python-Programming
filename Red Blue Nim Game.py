
class RBNGame:

    def __init__(self, num_red = 7, num_blue = 7, version = 0, first_player =0, depth=0):
        self.num_red = num_red
        self.num_blue = num_blue
        self.version = version                  #0 for standard 1 for misere
        self.first_player = first_player        #0 for human 1 for computer
        self.depth = depth
        self.score = 0
        self.current_player = first_player      #0 for human 1 for computer

    def current_state(self):
        print(f"Red marbels = {self.num_red} and Blue marbels = {self.num_blue}")

    def get_version(self):
        print("Which version you wanna play")
        print("Press 0 for standard and 1 for misere")
        while True:
            try:
                ver_user = int(input())
                if ver_user not in [0,1]:
                    raise ValueError
                else:
                    self.version = ver_user
            except ValueError:
                print("Invalid Entry. Please Press 0 or 1 only!")
                ver_user= 0
                continue
            break


    def start_game(self):
        print("RED BLUE NIM GAME!!")
        self.get_version()
        self.current_state()
    
    def change_turn(self):
        self.current_player += 1
        self.current_player %= 2

    def human_move(self):
        
        #Input and error handling 
        keep_going = True
        while(keep_going == True):
            print("Which marble you want to remove (red/blue)")
            color_marble = str.lower(input())

            if color_marble not in ["red", "blue"]:
                print("Invalid color. Please use red or blue only!")
                keep_going = True
                continue

            move = 0
            while(move == 0):   
                print("How many marbles you wanna remove (1 or 2)")
                try:
                    move = int(input())
                    if move not in [1,2]:
                        raise ValueError
                except ValueError:
                        print("Invalid Move. Please use 1 or 2 only!")
                        move= 0
                        continue
                
                if (color_marble == "red" and self.num_red < move) or (color_marble == "blue" and self.num_blue < move):        #error
                    print("You cannot remove more marbles than there are in the tile")
                    move = 0
                
            #removing the marbles           
            if(color_marble == "red"):
                self.num_red -= move
            elif(color_marble == "blue"):
                self.num_blue -= move

            print(f"Player {self.current_player+1} removed {move} marbels from {color_marble} stack ")
            self.change_turn()
            break


    def score_calc(self):
        self.score = self.num_red*2 + self.num_blue*3

    
    def gamenotover(self):  
        if (self.num_red==0 or self.num_blue==0):
            return False
        else: 
            return True

    def winner(self):
        
        #standard version
        if(self.version == 0):  
            if(self.current_player == 0):
                print("Computer Wins!")
            else:
                print("Player Wins!")

        #misere version
        else:                   
            if(self.current_player == 0):
                print("Player Wins!")
            else:
                print("Computer Wins!")

        self.score_calc()
        print(f"Score: {self.score}")


    ################## HEURISTIC-BASED ALGORITHM FOR COMPUTER MOVE ##################

    def heu_calc(self, num_marb):
        return num_marb % 3 
    
    def computer_move(self):
        mod_red = self.heu_calc(self.num_red)
        mod_blue = self.heu_calc(self.num_blue)
        
        #Both mods are non zero
        if mod_red != 0 and mod_blue != 0:
            if self.num_red >= self.num_blue:
                self.num_red -= mod_red
                print(f"Computer removed {mod_red} from red")
            else:
                self.num_blue -= mod_blue
                print(f"Computer removed {mod_blue} from blue")
        #One mod is zero
        elif mod_red>0:
            self.num_red -= mod_red
            print(f"Computer removed {mod_red} from red")
        elif mod_blue>0:
            self.num_blue -= mod_blue
            print(f"Computer removed {mod_blue} from blue")
    
        #Both mods are zero
        elif self.num_red >= self.num_blue:
            self.num_red -= 1
            print(f"Computer removed 1 from red")
        else:
            self.num_blue -= 1
            print(f"Computer removed 1 from blue")

        self.change_turn()


    def run_game(self):
        self.start_game()
        while self.gamenotover():
            if(self.current_player==0):
                self.human_move()
                self.current_state()
            else:
                self.computer_move()     
                self.current_state()
        
        print(self.current_player)
        self.winner()


def main():
    game = RBNGame()
    game.run_game()

if __name__ == "__main__":
    main()




    
