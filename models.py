import nn

class PerceptronModel(object):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        "*** YOUR CODE HERE ***"

    def get_prediction(self, x):
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        "*** YOUR CODE HERE ***"

    def train(self, dataset):
        """
        Train the perceptron until convergence.
        """
        "*** YOUR CODE HERE ***"

class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        
        # self.w = nn.Parameter(1, dimensions)
        self.w1 = nn.Parameter(1, 512)  # 1st weight layer: input dim 1, output dim 512
        self.b1 = nn.Parameter(1, 512) 
        self.w2 = nn.Parameter(512, 1)  # 2nd weight layer: input dim 512, output dim 1
        self.b2 = nn.Parameter(1, 1)    
        
        # Other parameters given
        self.learning_rate = 0.05 # Param update size/iter
        self.batch_size = 100 # Samples taken before update, 
                              # 200 was too high, this quick turnaround yields better results

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        "*** YOUR CODE HERE ***"
        # Rectified Linear unit activation 
        lyr = nn.Linear(x, self.w1) # Input transformation from 1d to 512d
        lyr = nn.AddBias(lyr, self.b1) # Applies the bias
        lyr = nn.ReLU(lyr) # Replaces all neg nums with 0, introduces Non-linearity

        # Output formatting
        result = nn.Linear(lyr, self.w2) # Transformation back to 1d
        result = nn.AddBias(result, self.b2) # adds the 2nd bias to the result

        return result

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        # Get predictions for loss calculation
        predicted = self.run(x) # model esitmations

        result = nn.SquareLoss(predicted, y) # compare to true nodes

        return result # returns scaler representing total error

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        # Until convergence continue training
        converged = False

        while not converged:

            # Track the loss across for this session
            total_loss = 0
            total_batches = 0

            for input, target in dataset.iterate_once(self.batch_size):
                
                current_loss = self.get_loss(input, target) # loss calculation

                # Gradients 
                grads = nn.gradients(current_loss, [self.w1, self.b1, self.w2, self.b2])
                grad_w1, grad_b1, grad_w2, grad_b2 = grads  # unpack into separate variables
                
                # Param update
                # parameter = parameter - learning_rate * gradients 
                self.w1.update(grad_w1, -self.learning_rate) # -self.learning_rate to minimize loss
                self.b1.update(grad_b1, -self.learning_rate)
                self.w2.update(grad_w2, -self.learning_rate)
                self.b2.update(grad_b2, -self.learning_rate)

                # Track Loss
                total_loss += nn.as_scalar(current_loss)
                total_batches += 1

            # Calculate loss
            average_loss = total_loss / total_batches

            # Convergence Flag
            if average_loss < 0.02: # Given convergence ideals
                converged = True


class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.w1 = nn.Parameter(784, 200) # Input to hidden layer weights
        self.b1 = nn.Parameter(1,200) # Hidden lyaer bias
        self.w2 = nn.Parameter(200, 10) # Hidden layer to digit classes
        self.b2 = nn.Parameter(1, 10) # Digit class bias

        # Given hyperparameters
        self.learning_rate = 0.5
        self.batch_size = 100 


    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        # Run linear transformation
        # First Layer Transformation done with ReLU
        lyr = nn.Linear(x, self.w1) # Apply weight to reggression
        lyr = nn.AddBias(lyr, self.b1) # Bias translation
        lyr = nn.ReLU(lyr) # Activation


        #Transform second without ReLU
        result = nn.Linear(lyr, self.w2)

        return nn.AddBias(result, self.b2)

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"

        # Run batch and compute loss
        return nn.SoftmaxLoss(self.run(x), y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        # Set accuracy target

        target_accuracy = .975 # a bit higher than 97 for grading consistency

        while dataset.get_validation_accuracy() < target_accuracy:
            # Process batches
            for x, y in dataset.iterate_once(self.batch_size):
                # Get loss
                loss = self.get_loss(x,y)

                gradient_calcs = nn.gradients(loss, [self.w1, self.b1, self.w2, self.b2])

                # Update weights and bias with gradients
                self.w1.update(gradient_calcs[0], -self.learning_rate)
                self.b1.update(gradient_calcs[1], -self.learning_rate)
                self.w2.update(gradient_calcs[2], -self.learning_rate)
                self.b2.update(gradient_calcs[3], -self.learning_rate)

class LanguageIDModel(object):
    """
    A model for language identification at a single-word granularity.

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Our dataset contains words from five different languages, and the
        # combined alphabets of the five languages contain a total of 47 unique
        # characters.
        # You can refer to self.num_chars or len(self.languages) in your code
        self.num_chars = 47
        self.languages = ["English", "Spanish", "Finnish", "Dutch", "Polish"]

        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"

    def run(self, xs):
        """
        Runs the model for a batch of examples.

        Although words have different lengths, our data processing guarantees
        that within a single batch, all words will be of the same length (L).

        Here `xs` will be a list of length L. Each element of `xs` will be a
        node with shape (batch_size x self.num_chars), where every row in the
        array is a one-hot vector encoding of a character. For example, if we
        have a batch of 8 three-letter words where the last word is "cat", then
        xs[1] will be a node that contains a 1 at position (7, 0). Here the
        index 7 reflects the fact that "cat" is the last word in the batch, and
        the index 0 reflects the fact that the letter "a" is the inital (0th)
        letter of our combined alphabet for this task.

        Your model should use a Recurrent Neural Network to summarize the list
        `xs` into a single node of shape (batch_size x hidden_size), for your
        choice of hidden_size. It should then calculate a node of shape
        (batch_size x 5) containing scores, where higher scores correspond to
        greater probability of the word originating from a particular language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
        Returns:
            A node with shape (batch_size x 5) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"

    def get_loss(self, xs, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 5). Each row is a one-hot vector encoding the correct
        language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
            y: a node with shape (batch_size x 5)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
