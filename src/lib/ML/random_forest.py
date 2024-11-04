import random
import math

class DecisionTree:
    def __init__(self, max_depth=10):
        self.max_depth = max_depth
        self.root = None

    class Node:
        def __init__(self):
            self.feature_index = None
            self.threshold = None
            self.left = None
            self.right = None
            self.value = None

    def fit(self, X, y):
        self.root = self._build_tree(X, y)

    def _calculate_variance(self, y):
        if not y:
            return 0
        mean = sum(y) / len(y)
        return sum((val - mean) ** 2 for val in y) / len(y)

    def _find_best_split(self, X, y):
        best_gain = float('-inf')
        best_feature = None
        best_threshold = None
        
        current_variance = self._calculate_variance(y)
        
        for feature in range(len(X[0])):
            values = sorted(set(row[feature] for row in X))
            
            for i in range(len(values) - 1):
                threshold = (values[i] + values[i + 1]) / 2
                
                left_y = [y[j] for j in range(len(X)) if X[j][feature] <= threshold]
                right_y = [y[j] for j in range(len(X)) if X[j][feature] > threshold]
                
                if not left_y or not right_y:
                    continue
                
                gain = current_variance - (
                    (len(left_y) * self._calculate_variance(left_y) +
                     len(right_y) * self._calculate_variance(right_y)) / len(y)
                )
                
                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature
                    best_threshold = threshold
        
        return best_feature, best_threshold

    def _build_tree(self, X, y, depth=0):
        node = self.Node()
        
        if depth >= self.max_depth or len(set(y)) == 1:
            node.value = sum(y) / len(y)
            return node
        
        feature_index, threshold = self._find_best_split(X, y)
        if feature_index is None:
            node.value = sum(y) / len(y)
            return node
        
        node.feature_index = feature_index
        node.threshold = threshold
        
        left_indices = [i for i in range(len(X)) if X[i][feature_index] <= threshold]
        right_indices = [i for i in range(len(X)) if X[i][feature_index] > threshold]
        
        left_X = [X[i] for i in left_indices]
        left_y = [y[i] for i in left_indices]
        right_X = [X[i] for i in right_indices]
        right_y = [y[i] for i in right_indices]
        
        node.left = self._build_tree(left_X, left_y, depth + 1)
        node.right = self._build_tree(right_X, right_y, depth + 1)
        
        return node

    def predict(self, X):
        return [self._predict_one(x, self.root) for x in X]

    def _predict_one(self, x, node):
        if node.value is not None:
            return node.value
        
        if x[node.feature_index] <= node.threshold:
            return self._predict_one(x, node.left)
        return self._predict_one(x, node.right)

class RandomForest:
    def __init__(self, n_trees=100, max_depth=10):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.trees = []
        
    def fit(self, X, y):
        n_features = len(X[0])
        self.features_per_tree = int(math.sqrt(n_features))
        
        for _ in range(self.n_trees):
            tree = DecisionTree(max_depth=self.max_depth)
            X_sample, y_sample = self._bootstrap_sample(X, y)
            feature_indices = random.sample(range(n_features), self.features_per_tree)
            
            X_subset = [[row[i] for i in feature_indices] for row in X_sample]
            
            tree.fit(X_subset, y_sample)
            self.trees.append((tree, feature_indices))

    def _bootstrap_sample(self, X, y):
        n_samples = len(X)
        indices = [random.randint(0, n_samples-1) for _ in range(n_samples)]
        return [X[i] for i in indices], [y[i] for i in indices]

    def predict(self, X):
        predictions = []
        for tree, features in self.trees:
            X_subset = [[row[i] for i in features] for row in X]
            prediction = tree.predict(X_subset)
            predictions.append(prediction)
        
        return [sum(pred[i] for pred in predictions) / len(self.trees)
                for i in range(len(X))]

