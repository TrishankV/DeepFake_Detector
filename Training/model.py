import tensorflow as tf

# Define the model with increased dropout rate
def train_model(train_data,Val_data) :
    model_1 = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(filters=10,
                            kernel_size=3,
                            activation="relu",
                            input_shape=(224, 224, 3)),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Conv2D(10, 3, activation="relu"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPool2D(pool_size=2, padding="valid"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Conv2D(10, 3, activation="relu"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Conv2D(10, 3, activation="relu"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dense(100, activation='relu'),
        tf.keras.layers.Conv2D(10, 3, activation="relu"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPool2D(2),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dropout(0.5),  # Increase dropout rate to 0.5
        tf.keras.layers.Dense(1, activation="sigmoid")
    ])

    # Define EarlyStopping callback
    early_stopping_callback = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',  # Monitor validation loss
        patience=5,           # Number of epochs with no improvement after which training will be stopped
        restore_best_weights=True  # Restore model weights from the epoch with the best validation loss
    ) #slow and 77% ,56% accuracy
    model_1.compile(loss="binary_crossentropy",
              optimizer=tf.keras.optimizers.Adam(),
              metrics=["accuracy"])
    # Fit the model
    history_1 = model_1.fit(train_data,
                        epochs=15,
                        steps_per_epoch=len(train_data),
                        validation_data=Val_data,
                        validation_steps=len(Val_data))
    return model_1