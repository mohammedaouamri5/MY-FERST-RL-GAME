import matplotlib.pyplot as plt
from IPython import display
import seaborn as sns
import matplotlib.pyplot as plt


state_dic = {
        0:"is_on_right",
        1:"is_inside",
        2:"is_on_left",
}
action_dic = {
    0: "left",
    1: "stay",
    2: "right",
}

plt.ion()
 
def plot(scores, mean_scores, matrix):
    plt.clf()

    # Extract labels from dictionaries
    state_labels = [state_dic[i] for i in range(matrix.shape[0])]
    action_labels = [action_dic[i] for i in range(matrix.shape[1])]

    # Create a heatmap using Seaborn
    sns.heatmap(matrix, cmap='viridis', annot=True, xticklabels=action_labels, yticklabels=state_labels)

    plt.title('Matrix')
    plt.xlabel('Action')
    plt.ylabel('State')

    plt.tight_layout()
    plt.show(block=False)
    plt.pause(.1)


if __name__ == "__main__":
        
    # Example usage
    scores = [10, 20, 30, 40]
    mean_scores = [15, 25, 35, 45]
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    plot(scores, mean_scores, matrix)
