import numpy as np
from keras.utils.np_utils import to_categorical
from keras import models
from keras import layers
from dataloader import DataLoader
import argparse
import matplotlib.pyplot as plt


def vectorize_sequences(sequences, dimension):
    results = np.zeros((len(sequences), dimension))
    for i, sequence in enumerate(sequences):
        sequence = list(sequence)
        results[i, sequence] = 1.
    return results


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', type=str, default='data/dataset.json')
    parser.add_argument('--epoch', type=int, default=100)
    parser.add_argument('--batch_size', type=int, default=5)

    args = parser.parse_args()

    # 데이터 전처리
    dl = DataLoader(args.data_path)
    # position_score = [101,101,101,101]
    position_score = [4,4,4,4]
    shape_X = sum(position_score)
    dl.setBias(position_score)
    
    X_labels = np.array([i for i in range(dl.getCount())])
    num2hobby = dl.getNum2Hobby()
    scores_with_bias = dl.getDatasetWithBias()

    X_train = vectorize_sequences(scores_with_bias, sum(position_score))
    one_hot_train_labels = to_categorical(X_labels)
    
    # 새 모델로 시작
    model = models.Sequential()
    model.add(layers.Dense(40, activation='relu', input_shape=(shape_X,)))
    model.add(layers.Dense(20, activation='relu'))
    model.add(layers.Dense(dl.getCount(), activation='softmax'))

    model.compile(optimizer='adam',
                loss='categorical_crossentropy',
                metrics=['accuracy'])

    # Train
    history = model.fit(X_train,
                    one_hot_train_labels,
                    epochs=args.epoch,
                    batch_size=args.batch_size
                    )
    # Loss 시각화

    loss = history.history['loss']

    epochs = range(1, len(loss) + 1)

    plt.plot(epochs, loss, 'bo', label='Training loss')
    plt.title('Training and validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    plt.show()

    # 모델 저장
    model.save('./model_saved.h5')