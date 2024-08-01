import numpy as np
import random
import pickle

class BattleshipEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = np.full((10, 10), -1)  # -1 represents empty water
        self.ship_positions = []  # List to keep track of ship positions
        self.place_ships() #places ships in environment
        self.hits = 0  # Tracks the number of hits
        return self.get_state()    # gets the state

    def place_ships(self):
        # Place all ships in a normal game
        self.add_ship(2)
        self.add_ship(3)
        self.add_ship(4)
        self.add_ship(4)
        self.add_ship(5)
    #function to add ships to the board
    def add_ship(self, length):
        placed = False
        while not placed:
            row = random.randint(0, 9)
            col = random.randint(0, 9)
            horizontal = random.choice([True, False])
            if self.can_place_ship(row, col, length, horizontal):
                self.place_ship(row, col, length, horizontal)
                placed = True
    #function to check if the ship can be placed 
    def can_place_ship(self, row, col, length, horizontal):
        if horizontal:
            if col + length > 10:
                return False
            for i in range(col, col + length):
                if self.board[row, i] != -1:
                    return False
        else:
            if row + length > 10:
                return False
            for i in range(row, row + length):
                if self.board[i, col] != -1:
                    return False
        return True
    #function to access the board and actually add the ships
    def place_ship(self, row, col, length, horizontal):
        for i in range(length):
            if horizontal:
                self.board[row, col + i] = 1
            else:
                self.board[row + i, col] = 1
        self.ship_positions.append((row, col, length, horizontal))
    
    def get_state(self):
        return self.board.copy()
    #function to run a step in the game
    def step(self, action):
        row, col = action
        if row < 0 or row >= 10 or col < 0 or col >= 10:
            raise IndexError(f"Action {action} is out of bounds.")
        if self.board[row, col] == 1:
            self.board[row, col] = 2  # 2 represents a hit
            self.hits += 1
            reward = 1
        else:
            self.board[row, col] = 0  # 0 represents a miss
            reward = -1

        done = self.hits == 18  # End the game when all ships are sunk 
        return self.get_state(), reward, done
    #renders the board
    def render(self):
        for row in self.board:
            print(' '.join(['.' if x == -1 else 'O' if x == 0 else 'X' if x == 2 else '#' for x in row]))
#Q Learning Ai class
class QLearningAI:
    def __init__(self, learning_rate=0.1, discount_factor=0.95, exploration_rate=1.0, exploration_decay=0.995):
        self.q_table = np.zeros((10, 10, 10, 10))  # state-action pairs here
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
    #gets an action
    def get_action(self, state):
        if random.uniform(0, 1) < self.exploration_rate:
            return random.choice([(i, j) for i in range(10) for j in range(10)])
        else:
            return self.best_action(state)
    #gets the best action for the AI
    def best_action(self, state):
        flat_index = np.argmax(self.q_table[state[0], state[1], :, :])
        row, col = divmod(flat_index, 10)
        return row, col
    #function to update the q table
    def update_q_table(self, state, action, reward, next_state):
        best_next_action = self.best_action(next_state)
        td_target = reward + self.discount_factor * self.q_table[next_state[0], next_state[1], best_next_action[0], best_next_action[1]]
        td_error = td_target - self.q_table[state[0], state[1], action[0], action[1]]
        self.q_table[state[0], state[1], action[0], action[1]] += self.learning_rate * td_error
        self.exploration_rate *= self.exploration_decay

# Training the AI
#establishing the environment
env = BattleshipEnv()
#establishes the AI
ai = QLearningAI()

#training length decreased due to lack of computing resources
for episode in range(100):  # Number of training episodes
    print(episode)
    state = env.reset()
    done = False

    while not done:
        #while the game is being played get actions and update the q-table
        action = ai.get_action(state)
        try:
            next_state, reward, done = env.step(action)
            ai.update_q_table(state, action, reward, next_state)
            state = next_state
        except IndexError:
            # Handle out of bounds action by ignoring it and continuing the loop
            continue

print("Training complete. AI is ready to play.")
#AI is trained by now
with open('trained_q_table.pkl', 'rb') as file:
    q_table=pickle.load(file)
    #pickles the q_table values
#if code is separated it could read the file
with open('trained_q_table.pkl', 'wb') as file:
    q_table=pickle.dump(q_table,file)
# Main game loop
env = BattleshipEnv()
user_turn = True

print("Welcome to Battleship!")

def get_user_action():
    while True:
        try:
            row = int(input("Enter row (0-9): "))
            col = int(input("Enter column (0-9): "))
            if 0 <= row < 10 and 0 <= col < 10:
                return (row, col)
            else:
                print("Invalid input. Please enter values between 0 and 9.")
        except ValueError:
            print("Invalid input. Please enter numeric values.")

state = env.reset()

while True:
    env.render()
    if user_turn:
        print("Your turn!")
        action = get_user_action()
    else:
        print("AI's turn!")
        action = ai.get_action(state)
        print("AI chose: {action}")

    try:
        state, reward, done = env.step(action)
    except IndexError:
        print("Invalid action chosen by AI. Skipping turn.")
        reward, done = -1, False  # Invalid actions must be skipped

    if reward == 1:
        print("Hit!")
    else:
        print("Miss!")

    if done == True:
        print("Game over!")
        if user_turn:
            print("You win!")
        else:
            print("AI wins!")
        break

    user_turn = not user_turn
