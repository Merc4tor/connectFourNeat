import neat
from connect_four import ConnectFourGame
import os
from multiprocessing import Pool, cpu_count

def get_index_list(my_list: list):
    list_tmp = my_list.copy()
    list_sorted = my_list.copy()
    list_sorted.sort()

    list_index = []
    for x in list_sorted:
        list_index.insert(0,list_tmp.index(x))
        list_tmp[list_tmp.index(x)] = -1
    
    return list_index

def train_ai(game: ConnectFourGame, genome1, genome2, config):
    net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
    net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
    
    run = True
    while run:
        board_full = game.check_board_full()
        if (board_full):
            genome1.fitness += 1
            genome2.fitness += 1
            run = False
            break        

        data = game.nn_data
        
        if (game.current_player == 1):
            player = 1
            data = [player] + data         

            output = net1.activate(data)
        else:
            player = 2
            data = [player] + data         
            output = net2.activate(data)

        output_index = get_index_list(output)

        not_placed = True
        i = 0
        while not_placed:
            index = output_index[i]
            not_placed = not game.place(index + 1)
            i += 1
            try:
                round_result = game.check_win(player)
            except:
                round_result = False
        
        if (round_result):
            if (player == 1):
                genome1.fitness += 3
                genome2.fitness -= 3
            else:
                genome1.fitness -= 3
                genome2.fitness += 3
            run = False
            break
    
        

        
    # print('finished game')

def train_ai_from_pool(x):
    train_ai(x[0], x[1], x[2], x[3])


def eval_genomes(genomes, config):
    games = []
    for i, (genome_id1, genome1) in enumerate(genomes):
        if i == len(genomes) - 1:
            break
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i+1:]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            game = ConnectFourGame()
            games.append((game, genome1, genome2, config))
            # train_ai(game, genome1, genome2, config)    
    
    processes_num = max(1, cpu_count() - 1)
    with Pool(processes_num) as p:
        p.map(train_ai_from_pool, games)
    
    print(genomes[0][1].fitness)
    
            


def run_neat (config):
    # p = neat.Checkpointer.restore_checkpoint('xxneat-checkpoint-27')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1, filename_prefix="xxneat-checkpoint"))
    
    winner = p.run(eval_genomes, 50)
    print(dict(winner))
    
    
    

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    
    run_neat(config)