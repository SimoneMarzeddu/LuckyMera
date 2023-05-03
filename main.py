import sys
import json
import time
import argparse
import gym
from modules import general_modules, reach_modules, secret_passage_modules
from core import Saver, GameWhisperer, DungeonWalker, main_logic
import training
from nle_language_wrapper import NLELanguageWrapper

def start_bot(env, saver, filename):
    with open('config.json', 'r') as f:
        config = json.load(f)

    print("\nJudy is looking for the Amulet of Yendor on the map ...\n")
    print("\nVersion: 1.1.9 Stairs\n")

    exec_mode = config['fast_mode']
    mode = False
    if exec_mode == "on":
        mode = True
        print("\nFast_Mode : ON")
    elif exec_mode == "off":
        print("\nFast_Mode : OFF")
    else:
        print("\nFast_Mode can only be \"on\" or \"off\" -> value set to default : OFF")
    time.sleep(0.5)

    games_number = 100
    try:
        games_number = int(config['attempts'])
        print("Attempts : ", games_number)
    except:
        print("Attempts must be an int value -> value set to default : ", games_number)
        games_number = 100
    time.sleep(0.5)

    game_interface = GameWhisperer(env, mode, saver, filename)
    walk_logic = DungeonWalker(game_interface)

    task_prio = config['task_prio_list']
    task_modules_map = {}
    for i in range(0, len(task_prio)):
        task_name = task_prio[i]
        
        if hasattr(general_modules, task_name): task_class = getattr(general_modules, task_name)
        elif hasattr(reach_modules, task_name): task_class = getattr(reach_modules, task_name)
        elif hasattr(secret_passage_modules, task_name): task_class = getattr(secret_passage_modules, task_name)
        else: sys.exit('task not found')

        task_modules_map[task_name] = task_class(walk_logic, game_interface, task_name)
        print(task_name)
        '''
        try:
            task_class = getattr(general_modules, task_name)
        except:
            try:
                task_class = getattr(reach_modules, task_name)
            except:
                try:
                    task_class = getattr(secret_passage_modules, task_name)
                except:
                   raise Exception('task not found')

        '''
        '''
        if task == "pray":
            task_modules_map[task] = Pray(walk_logic, game_interface, task)
        elif task == "take_a_break":
            task_modules_map[task] = Break(walk_logic, game_interface, task)
        elif task == "engrave_elbereth":
            task_modules_map[task] = Elbereth(walk_logic, game_interface, task)
        elif task == "run_for_your_life":
            task_modules_map[task] = Run(walk_logic, game_interface, task)
        elif task == "close_monster_fight":
            task_modules_map[task] = Fight(walk_logic, game_interface, task)
        elif task == "time_of_the_lunch":
            task_modules_map[task] = Eat(walk_logic, game_interface, task)
        elif task == "greed_of_gold":
            task_modules_map[task] = Gold(walk_logic, game_interface, task)
        elif task == "stairs_descent":
            task_modules_map[task] = StairsDescent(walk_logic, game_interface, task)
        elif task == "stairs_ascent":
            task_modules_map[task] = StairsAscent(walk_logic, game_interface, task)
        elif task == "reach_closest_explorable":
            task_modules_map[task] = ExploreClosest(walk_logic, game_interface, task)
        elif task == "reach_horizon":
            task_modules_map[task] = Horizon(walk_logic, game_interface, task)
        elif task == "search_hidden_room":
            task_modules_map[task] = HiddenRoom(walk_logic, game_interface, task)
        elif task == "explore_unseen":
            task_modules_map[task] = Unseen(walk_logic, game_interface, task)
        elif task == "search_hidden_corridor":
            task_modules_map[task] = HiddenCorridor(walk_logic, game_interface, task)
        elif task == "random_walk":
            task_modules_map[task] = RandomWalk(walk_logic, game_interface, task)
        print(task)
        '''
        time.sleep(0.2)

    print("\nJudy is ready for YASD ...")
    print("\n\n")
    time.sleep(1)

    return walk_logic, game_interface, task_prio, task_modules_map, games_number

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
    '--inference',
    dest='training',
    action='store_false',
    help='Use the framework to actually play the game'
    )
    parser.add_argument(
        '--observation_keys',
        dest='observation_keys',
        nargs='+',
        default=None,
        help='Specify the observation space of nle'
    )
    
    #### DATASET CREATION PARAMETERS ####
    dataset_creation_group = parser.add_argument_group('dataset creation')
    dataset_creation_group.add_argument(
        '--create_dataset',
        dest='create_dataset',
        action='store_true',
        help='Use the bot to generate a dataset of trajectories'
    )
    dataset_creation_group.add_argument(
        '--language_mode',
        dest='language_mode',
        action='store_true',
        help='Save trajectories in language mode, using the nle_language_wrapper'
    )
    dataset_creation_group.add_argument(
        '--keys_to_save',
        dest='keys_to_save',
        nargs='+',
        default=None,
        help='Specify the observation keys to save'
    )
    dataset_creation_group.add_argument(
        '--filename',
        type=str,
        default='saved_trajectories',
        help='The path where to save trajectories' 
    )

    #### TRAINING PARAMETERS ####
    training_group = parser.add_argument_group('training mode')
    training_group.add_argument(
        '--training',
        dest='training',
        action='store_true',
        help='Train a neural model'
    )
    training_group.add_argument(
        '--training_alg',
        type=str,
        default=None,
        help='Select the training algorithm to use'
    )
    training_group.add_argument(
        '--dataset',
        type=str,
        default='saved_trajectories.pkl',
        help='Path to the dataset for the training process'
    )
    training_group.add_argument(
        '--batch_size',
        type=int,
        default=32,
        help='Size of the batch in the training process'
    )
    training_group.add_argument(
        '--checkpoint',
        type=str,
        default='saved_model',
        help='Path to save the trained model'
    )
    training_group.add_argument(
        '--cuda',
        dest='cuda',
        action='store_true',
        help='Use cuda for training'
    )
    training_group.add_argument(
        '--no_cuda',
        dest='cuda',
        action='store_false',
        help='Do not use cuda for training'
    )
    parser.set_defaults(cuda=True)
    training_group.add_argument(
        '--seed',
        type=int,
        default=42,
        help='Random seed'
    )
    training_group.add_argument(
        '--learning_rate',
        type=float,
        default=1e-5,
        help='Learning rate of the training process'
    )
    training_group.add_argument(
        '--scheduler_gamma',
        type=float,
        default=0.7,
        help='The gamma parameter of the scheduler of the training process'
    )
    training_group.add_argument(
        '--epochs',
        type=int,
        default=5,
        help='Number of epochs'
    )
    parser.set_defaults(training=False)


    flags = parser.parse_args()
    create_dataset = flags.create_dataset
    language_mode = flags.language_mode
    keys_to_save = flags.keys_to_save
    filename = flags.filename
    training_mode = flags.training
    training_alg_name = flags.training_alg
    dataset = flags.dataset
    batch_size = flags.batch_size
    checkpoint = flags.checkpoint
    observation_keys = flags.observation_keys

    training_params = {}
    training_params['use_cuda'] = flags.cuda
    training_params['seed'] = flags.seed
    training_params['learning_rate'] = flags.learning_rate
    training_params['scheduler_gamma'] = flags.scheduler_gamma
    training_params['epochs'] = flags.epochs

    print(f'training mode: {training_mode}')
    print(f'obs_keys: {observation_keys}')

    env_name = 'NetHackChallenge-v0'
    if observation_keys:
        env = gym.make(env_name, observation_keys=observation_keys)
    #if no observation_keys are specified, all the keys are included
    else: env = gym.make(env_name)
    
    if training_mode:
        if not training_alg_name:
            raise SystemError('No training algorithm specified')
        if hasattr(training, training_alg_name):
            training_alg_class = getattr(training, training_alg_name)
            print(f'Using {training_alg_name} for training')
        else:
            raise SystemError(f'The training algorithm {training_alg_name} is not implemented in training.py')

        training_alg = training_alg_class(training_params, env, dataset, batch_size, checkpoint)
        training_alg.train()
    else:
        if create_dataset and not filename:
            raise SystemError('no filename to store trajectories')
        if language_mode and not create_dataset:
            raise SystemError('language mode selected, but create_dataset is false')
        if create_dataset and not keys_to_save:
            raise SystemError('keys_to_save equal to None - No keys to save')
        
        if language_mode: env = NLELanguageWrapper(env, use_language_action=False)
        if create_dataset: saver = Saver(keys_to_save, filename)
        else: saver = None

        dungeon_walker, game, logic, task_map, attempts = start_bot(env, saver, filename)
        main_logic(dungeon_walker, game, logic, task_map, attempts)

if __name__ == "__main__":
    main()
