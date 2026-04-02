# 간단한 이미지 분류기 구현
# 손글씨 숫자 이미지(MNIST 데이터셋)를 이용하여 간단한 이미지 분류기를 구현

import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.utils import to_categorical

# 요구사항 1: MNIST 데이터셋을 로드
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# 요구사항 2: 데이터를 훈련 세트와 테스트 세트로 분할
x_train = x_train.reshape(-1, 28*28).astype('float32') / 255.
x_test = x_test.reshape(-1, 28*28).astype('float32') / 255.
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

# 요구사항 3: 간단한 신경망 모델을 구축
model = Sequential()
model.add(Dense(128, activation='relu', input_shape=(784,)))
model.add(Dense(64, activation='relu'))
model.add(Dense(10, activation='softmax'))

# 요구사항 4: 모델을 훈련시키고 정확도를 평가
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=5, batch_size=32, validation_split=0.2)
loss, acc = model.evaluate(x_test, y_test, verbose=0)
print(f'테스트 정확도: {acc}')