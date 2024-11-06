import numpy as np

class DecisionTree:
    def __init__(self, max_depth=5):
        self.max_depth = max_depth
        self.root = None
    
    class Node:
        def __init__(self):
            self.feature = None
            self.threshold = None
            self.left = None
            self.right = None
            self.value = None
    
    def fit(self, X, y):
        # Basic data validation for stock data
        valid_mask = ~np.isnan(y) & ~np.isinf(y)
        X = X[valid_mask]
        y = y[valid_mask]
        
        self.root = self._build_tree(X, y)
    
    def _build_tree(self, X, y, depth=0):
        node = self.Node()
        
        # Leaf conditions
        if depth >= self.max_depth or len(y) < 2:
            node.value = np.mean(y)
            return node
        
        # Randomly select features to consider (random forest characteristic)
        n_features = X.shape[1]
        feature_subset = np.random.choice(n_features, max(1, n_features//3), replace=False)
        
        best_var_reduction = 0
        best_feature = None
        best_threshold = None
        
        current_variance = np.var(y)
        
        # Find best split
        for feature in feature_subset:
            # Use percentiles for thresholds
            thresholds = np.percentile(X[:, feature], [25, 50, 75])
            
            for threshold in thresholds:
                left_mask = X[:, feature] <= threshold
                right_mask = ~left_mask
                
                # Need minimum samples in each split
                if np.sum(left_mask) < 2 or np.sum(right_mask) < 2:
                    continue
                
                left_variance = np.var(y[left_mask])
                right_variance = np.var(y[right_mask])
                
                # Calculate variance reduction
                n_left = np.sum(left_mask)
                n_right = np.sum(right_mask)
                var_reduction = current_variance - (
                    (n_left * left_variance + n_right * right_variance) / len(y)
                )
                
                if var_reduction > best_var_reduction:
                    best_var_reduction = var_reduction
                    best_feature = feature
                    best_threshold = threshold
        
        # If no good split found, make leaf
        if best_feature is None:
            node.value = np.mean(y)
            return node
        
        # Split the node
        node.feature = best_feature
        node.threshold = best_threshold
        
        left_mask = X[:, best_feature] <= best_threshold
        right_mask = ~left_mask
        
        node.left = self._build_tree(X[left_mask], y[left_mask], depth + 1)
        node.right = self._build_tree(X[right_mask], y[right_mask], depth + 1)
        
        return node
    
    def predict(self, X):
        return np.array([self._predict_single(x, self.root) for x in X])
    
    def _predict_single(self, x, node):
        if node.value is not None:
            return node.value
        
        if x[node.feature] <= node.threshold:
            return self._predict_single(x, node.left)
        return self._predict_single(x, node.right)
    
class RandomForest:
    def __init__(self, n_trees=10, max_depth=5):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.trees = []
    
    def fit(self, X, y):
        # Convert inputs to numpy arrays
        X = np.asarray(X)
        y = np.asarray(y)
        
        # Remove invalid values
        valid_mask = ~np.isnan(y) & ~np.isinf(y)
        valid_mask &= ~np.any(np.isnan(X), axis=1)
        valid_mask &= ~np.any(np.isinf(X), axis=1)
        
        X = X[valid_mask]
        y = y[valid_mask]
        
        # Train trees with bootstrapped samples
        for _ in range(self.n_trees):
            # Bootstrap sampling
            indices = np.random.choice(len(X), len(X), replace=True)
            sample_X = X[indices]
            sample_y = y[indices]
            
            # Create and train tree
            tree = DecisionTree(max_depth=self.max_depth)
            tree.fit(sample_X, sample_y)
            self.trees.append(tree)
    
    def predict(self, X):
        # Get predictions from all trees
        predictions = np.array([tree.predict(X) for tree in self.trees])
        
        # Average predictions
        return np.mean(predictions, axis=0)