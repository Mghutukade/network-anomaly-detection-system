def train_model(model, X_train, y_train):
    model.fit(X_train, y_train)
    print("Model trained ✅")
    return model