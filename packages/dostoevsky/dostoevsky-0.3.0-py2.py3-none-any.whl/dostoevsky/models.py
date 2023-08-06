import os

from typing import List, Dict, Optional

from keras.models import Model, load_model
from keras.layers import Input, Dense, concatenate, Activation, Dropout
from keras.layers.convolutional import Conv1D
from keras.layers.pooling import GlobalMaxPooling1D
from keras.preprocessing.sequence import pad_sequences

from fasttext import load_model as load_fasttext_model

from dostoevsky.tokenization import BaseTokenizer
from dostoevsky.embeddings import BaseEmbeddingsContainer
from dostoevsky.corpora import BaseCorpusContainer, RusentimentCorpus
from dostoevsky.data import DATA_BASE_PATH


class BaseModel:

    def __init__(
        self,
        sentence_length: int,
        tokenizer: BaseTokenizer,
        embeddings_container: BaseEmbeddingsContainer,
        lemmatize: bool = True,
        model_path: Optional[str] = None,
        corpus: Optional[BaseCorpusContainer] = None,
    ):
        self.model_path = model_path
        self.sentence_length = sentence_length
        self.tokenizer = tokenizer
        self.embeddings_container = embeddings_container
        self.lemmatize = lemmatize
        self.corpus = corpus
        self.model = (
            self.get_compiled_model()
            if self.model_path
            else self.get_raw_model()
        )

    def get_compiled_model(self):
        raise NotImplementedError

    def preprocess_input(self, sentences: List[str]):
        raise NotImplementedError

    def predict(self, sentences: List[str]):
        raise NotImplementedError

    def get_raw_model(self):
        raise NotImplementedError


class BaseCNNModel(BaseModel):
    '''
    Slightly modified word-level CNN model from https://github.com/sismetanin/sentiment-analysis-of-tweets-in-russian
    '''

    def get_raw_model(self):
        branches = []
        tweet_input = Input(shape=(
            self.sentence_length,
            self.embeddings_container.dimension
        ), dtype='float32')
        x = Dropout(0.2)(tweet_input)

        for size, filters_count in [(2, 10), (3, 10), (4, 10), (5, 10)]:
            for i in range(filters_count):
                branch = Conv1D(
                    filters=1,
                    kernel_size=size,
                    padding='valid',
                    activation='relu'
                )(x)
                branch = GlobalMaxPooling1D()(branch)
                branches.append(branch)

        x = concatenate(branches, axis=1)
        x = Dropout(0.2)(x)
        x = Dense(30, activation='relu')(x)
        x = Dense(len(self.corpus.label_encoder.classes_))(x)
        output = Activation('softmax')(x)

        model = Model(inputs=[tweet_input], outputs=[output])
        model.compile(
            loss='categorical_crossentropy',
            optimizer='rmsprop',
            metrics=['categorical_accuracy']
        )
        return model


class SocialNetworkModel(BaseCNNModel):
    '''
    Trained on RuSentiment dataset (https://github.com/text-machine-lab/rusentiment)
    Achieves up to ~0.70 F1 (original RuSentiment model has ~0.72 F1 score)
    '''

    SENTENCE_LENGTH: int = 60
    MODEL_PATH: str = os.path.join(
        DATA_BASE_PATH,
        'models/cnn-social-network-model.hdf5'
    )

    def __init__(
        self,
        tokenizer: BaseTokenizer,
        embeddings_container: BaseEmbeddingsContainer,
        lemmatize: bool = False,
    ):
        super(SocialNetworkModel, self).__init__(
            sentence_length=self.SENTENCE_LENGTH,
            tokenizer=tokenizer,
            embeddings_container=embeddings_container,
            lemmatize=lemmatize,
            model_path=self.MODEL_PATH,
            corpus=RusentimentCorpus(
                data_path=None,
                tokenizer=tokenizer,
                embeddings_container=embeddings_container,
                lemmatize=lemmatize,
            )
        )

    def get_compiled_model(self):
        return load_model(self.model_path)

    def preprocess_input(self, sentences: List[str]) -> List[
        List[List[float]]
    ]:
        '''
        Convert array of sentences to array of sentences word embeddings.
        '''
        return pad_sequences([
            self.embeddings_container.get_word_vectors(
                self.tokenizer.split(sentence, lemmatize=self.lemmatize)
            ) for sentence in sentences
        ], maxlen=self.sentence_length, dtype='float32')

    def predict(self, sentences: List[str]):
        X = self.preprocess_input(sentences)
        Y = self.model.predict(X)
        labels: List[str] = (
            self
            .corpus
            .label_encoder
            .inverse_transform(Y)
        )
        return labels


class FastTextSocialNetworkModel(BaseModel):
    '''
    FastText model trained on RuSentiment dataset.
    '''

    SENTENCE_LENGTH: Optional[int] = None

    MODEL_PATH: str = os.path.join(
        DATA_BASE_PATH,
        'models/fasttext-social-network-model.bin'
    )

    def __init__(
        self,
        tokenizer: BaseTokenizer,
        lemmatize: bool = False,
    ):
        super(FastTextSocialNetworkModel, self).__init__(
            sentence_length=self.SENTENCE_LENGTH,
            tokenizer=tokenizer,
            embeddings_container=None,
            lemmatize=lemmatize,
            model_path=self.MODEL_PATH,
            corpus=None
        )

    def get_compiled_model(self):
        return load_fasttext_model(self.MODEL_PATH)

    def preprocess_input(self, sentences: List[str]) -> List[str]:
        return [
            ' '.join(
                token for token, _ in self.tokenizer.split(
                    sentence, lemmatize=self.lemmatize
                )
            )
            for sentence in sentences
        ]

    def predict(self, sentences: List[str], k: int = -1) -> List[
        Dict[str, float]
    ]:
        X = self.preprocess_input(sentences)
        Y = (
            self.model.predict(sentence, k=k) for sentence in X
        )
        return [
            dict(zip(
                (label.replace('__label__', '') for label in labels),
                scores
            )) for labels, scores in Y
        ]
