# L05. Image Recognition

  ## 01. 간단한 이미지 분류기 구현
  손글씨 숫자 이미지(MNIST 데이터셋)를 이용하여 간단한 이미지 분류기를 구현

  <details>
    <summary>전체 코드</summary>
    
    import tensorflow as tf
    from tensorflow.keras.datasets import mnist
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, Flatten
    from tensorflow.keras.utils import to_categorical
    
    # 요구사항1: MNIST 데이터셋을 로드
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    
    # 요구사항2: 데이터를 훈련 세트와 테스트 세트로 분할
    x_train = x_train.reshape(-1, 28*28).astype('float32') / 255.
    x_test = x_test.reshape(-1, 28*28).astype('float32') / 255.
    y_train = to_categorical(y_train, 10)
    y_test = to_categorical(y_test, 10)
    
    # 요구사항3: 간단한 신경망 모델을 구축
    model = Sequential()
    model.add(Dense(128, activation='relu', input_shape=(784,)))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(10, activation='softmax'))
    
    # 요구사항4: 모델을 훈련시키고 정확도를 평가
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=5, batch_size=32, validation_split=0.2)
    loss, acc = model.evaluate(x_test, y_test, verbose=0)
    print(f'테스트 정확도: {acc}')
  </details>
  
  #### 요구사항1: MNIST 데이터셋을 로드
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
  #### 요구사항 2: 데이터를 훈련 세트와 테스트 세트로 분할
    x_train = x_train.reshape(-1, 28*28).astype('float32') / 255.
    x_test = x_test.reshape(-1, 28*28).astype('float32') / 255.
    y_train = to_categorical(y_train, 10)
    y_test = to_categorical(y_test, 10)
  #### 요구사항  3: 간단한 신경망 모델을 구축
    model = Sequential()
    model.add(Dense(128, activation='relu', input_shape=(784,)))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(10, activation='softmax'))
  #### 요구사항 4: 모델을 훈련시키고 정확도를 평가
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=5, batch_size=32, validation_split=0.2)
    loss, acc = model.evaluate(x_test, y_test, verbose=0)
    print(f'테스트 정확도: {acc}')
    
  #### 모델 훈련 과정 및 결과화면
<img width="658" height="143" alt="MNIST_Train_epoch" src="https://github.com/user-attachments/assets/c4e6140b-5b59-4539-b5b6-50c655f4dde7" />
정확도: 0.97


---
  ## 02. CIFAR-10 데이터셋을 활용한 CNN 모델 구축
  CIFAR-10 데이터셋을 활용하여 합성곱 신경망(CNN)을 구축하고, 이미지 분류를 수행

  <details>
    <summary>전체 코드</summary>
    
    import tensorflow as tf
    from tensorflow.keras.datasets import cifar10
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
    from tensorflow.keras.utils import to_categorical
    from tensorflow.keras.preprocessing import image
    import numpy as np
    
    # 요구사항1: CIFAR-10 데이터셋을 로드
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()
    
    # CIFAR-10 클래스 이름
    class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
    
    # 요구사항2: 데이터 전처리(정규화 등)를 수행
    x_train = x_train.astype('float32') / 255.
    x_test = x_test.astype('float32') / 255.
    y_train = to_categorical(y_train, 10)
    y_test = to_categorical(y_test, 10)
    
    # 요구사항3: CNN 모델을 설계하고 훈련
    model = Sequential()
    model.add(Conv2D(32, (3,3), activation='relu', padding='same', input_shape=(32,32,3)))
    model.add(Conv2D(32, (3,3), activation='relu'))
    model.add(MaxPooling2D((2,2)))
    
    model.add(Conv2D(64, (3,3), activation='relu', padding='same'))
    model.add(Conv2D(64, (3,3), activation='relu'))
    model.add(MaxPooling2D((2,2)))
    
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dense(10, activation='softmax'))
    
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=10, batch_size=64, validation_split=0.2)
    
    # 요구사항4: 모델의 성능을 평가하고, 테스트 이미지(dog.jpg)에 대한 예측을 수행
    loss, acc = model.evaluate(x_test, y_test, verbose=0)
    print(f'테스트 정확도: {acc}')
    
    img = image.load_img('dog.jpg', target_size=(32, 32))
    img_array = image.img_to_array(img)
    img_array = img_array.astype('float32') / 255.0
    img_array = np.expand_dims(img_array, axis=0)   # (1, 32, 32, 3)
    
    dog_prediction = model.predict(img_array)
    dog_pred_class = np.argmax(dog_prediction, axis=1)[0]
    
    print('dog.jpg 예측 클래스명:', class_names[dog_pred_class])
  </details>
  
  #### 요구사항 1: CIFAR-10 데이터셋을 로드
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()
  #### 요구사항 2: 데이터 전처리(정규화 등)를 수행
    x_train = x_train.astype('float32') / 255.
    x_test = x_test.astype('float32') / 255.
    y_train = to_categorical(y_train, 10)
    y_test = to_categorical(y_test, 10)
  #### 요구사항 3: CNN 모델을 설계하고 훈련
    model = Sequential()
    model.add(Conv2D(32, (3,3), activation='relu', padding='same', input_shape=(32,32,3)))
    model.add(Conv2D(32, (3,3), activation='relu'))
    model.add(MaxPooling2D((2,2)))
    
    model.add(Conv2D(64, (3,3), activation='relu', padding='same'))
    model.add(Conv2D(64, (3,3), activation='relu'))
    model.add(MaxPooling2D((2,2)))
    
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dense(10, activation='softmax'))
    
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=10, batch_size=64, validation_split=0.2)
  #### 요구사항 4: 모델의 성능을 평가하고, 테스트 이미지(dog.jpg)에 대한 예측을 수행
    loss, acc = model.evaluate(x_test, y_test, verbose=0)
    print(f'테스트 정확도: {acc}')
    
    img = image.load_img('dog.jpg', target_size=(32, 32))
    img_array = image.img_to_array(img)
    img_array = img_array.astype('float32') / 255.0
    img_array = np.expand_dims(img_array, axis=0)   # (1, 32, 32, 3)
    
    dog_prediction = model.predict(img_array)
    dog_pred_class = np.argmax(dog_prediction, axis=1)[0]
    
    print('dog.jpg 예측 클래스명:', class_names[dog_pred_class])

  #### 모델 훈련 과정 및 결과화면
<img width="661" height="300" alt="CIFAR_Train" src="https://github.com/user-attachments/assets/b46d4132-de34-4a2b-a61e-d2aec3beb6b4" />
