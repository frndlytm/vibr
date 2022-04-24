# multilayer perceptron for mood classification

## Running the model 

Train the model with name mlp-model, 8 layers, 4000 units, with learning rate of 4e-4 for 100 epochs, and plot results after training

```sh
$ python cli.py train mlp-model --layers 8 --units 4000 --lr=4e-4 --epochs=100 --plot-result
```
Alternatively, we can train the model with gpu on the discovery cluster by changing the above parameters in `run.sh`.
```sh
$ sbatch run.sh
```