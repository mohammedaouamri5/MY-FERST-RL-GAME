
from agent import LR, Agent
from game import Game
from helper import plot


def train_Q_tab():

    plot_scores = [0]
    plot_mean_scores = [0]
    total_score = 0
    record = 0
    agent = Agent()
    game = Game()
    
    normalization_time:int = 0 
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        action = agent.get_action(state_old,game)

        # perform move and get new state
        reward, done, score = game.play_step(action)
        state_new = agent.get_state(game)

        if normalization_time%1e3 == 0 :
            agent.Q_tab.normalize()
        normalization_time=(normalization_time+1)%1e3
        # print(agent.Q_tab.max_aQ__s_a__(state_new) )
        
        agent.Q_tab[(state_old , action)] = agent.Q_tab[(state_old , action)]  + LR*(reward + agent.gamma * agent.Q_tab.max_aQ__s_a__(state_new) - agent.Q_tab[(state_old , action)]) # UP date  


        if done:
            game.reset()
            agent.n_games += 1

            if score > record:
                record = score
                agent.Q_tab.save()

            agent.gamma*=agent.gamma
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)

        plot(plot_scores, plot_mean_scores,agent.Q_tab.table)




if __name__ == "__main__":
    train_Q_tab()
