![](https://i.ibb.co/ypC5ZVv/aunnl.png)
___

AUNNL is another unnecessary neural network library for Python 3.x. It is intended to help create and train basic neural networks very easily.

## Getting Started

### Installation

It is recommended you install via pip for Python 3:

```
pip install aunnl
```

After this, you can import it into your python program with:

```
import aunnl
```

### Basic Example

The following example trains a neural network to classify handwritten digits from the MNIST dataset. The dataset is loaded using the `mnist_web` module, which is not packaged with AUNNL. Download and install it with the command `pip install mnist_web`.

```
import aunnl

from mnist_web import mnist
data, labels, _, _ = mnist(path="dataset")

model = aunnl.NeuralNetwork([784, 256, 10], ["relu", "sigmoid"])

epochs, lr, batch_size = 1, 0.1, 64

model.fit(data, labels, epochs, batch_size, lr, aunnl.losses.MSE)
model.save("mnist.aunn")
```

In the above example, a neural network with a hidden layer of 256 neurons is trained - its activation being ReLU and the output layer activation being sigmoid. The model, which is an `aunnl.NeuralNetwork` object, is then saved to the file `mnist.aunn`. The model can be loaded from the file with `aunnl.loadModel('mnist.aunn')`.

To use the model, simply pass the image in the form of a flat numpy array (denoted here as `img_arr`) to the model with `model.feedForward(img_arr)`. The `feedForward` function returns a list of the values outputted by the model.
