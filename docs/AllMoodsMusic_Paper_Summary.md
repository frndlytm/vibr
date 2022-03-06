## Music Classification Using Listening Data Paper Summary ##

### Introduction: ###
- #### Argument: ####
    - Listening-based features outperform content-based ones when classifying moods in music. 
    - “listening embeddings yield superior results due to their ability to capture information that is not straightforward to be extracted from pure audio content only”

- #### Dataset: ####
    - Subset of Million Song Dataset, totalling 67k tracks (from the Taste Profile subset), annotations of 188 different moods collected from AllMusic

- #### Goals: ####
    - Estimation of moods that a given music track may evoke
    - “music emotion recognition”

- #### Impact: ####
    - Assist streaming music services and impact track navigation and user recommendations
    - Identifies that listener personality correlates not only with musical taste but also with genre, contributes to psychologically driven approaches to a music recommendation system
    - “Emotion aware recommendation systems

- #### Existing Models: ####
    - Regression on a continuous mood space then clustering the space to obtain a “specific mood vocabulary”
    - Multi-label classification problem by classifying a given track into one or more moods given a fixed label vocabulary

### Mood Classification: ### 

- #### Problem definition: ####
    - Multi-label classification problem
    - **$x \in R^E$** - an embedding of a single track, where E is the number of dimensions
    - Each track is associated with a set of mood tags from mood vocabulary $T$
    - Each label is represented as a binary indicator **$y \in {0,1}^{|T|}$**
    - Aim to learn function f that computes the predicted label vector
    - x will be extracted from tracks using **audio and listening based approaches**
    - Leverage features derived from user interactions to estimate the mood of a track

### Data: ###
- #### Sources: ####
    - AllMusic - mood annotations
    - Echo Nest Taste Profile - mapped tracks to MillionSong Dataset
    - 7-digital - provides 30 sec song previews as audio data
- #### Splitting: ####
    - Randomly split 10% validation, 10% test, 80% training
    - (splits available on github for replication)

- #### Mood Tags: ####
    - human-annotated mood tags on an album level that is assigned to each track
    - total of 188 mood tags
    - there are similar moods that often co-occur and can be clustered into smaller groups, but are left as is for this paper
    - expect for machine learning models to cope with the large and overlapping vocabulary
    - these are human curated tags so while they may be similar words, they could provide additional nuance that is valuable 
    - Median of 2385 tracks associated with each track
    - Most tracks have an average of 9 moods associated with them, with none having more than 13

- #### Audio Data: ####
    - 30 second clips from 7-digital

- #### Listening Data: ####
    - Taste Profile from Million Song Dataset
    - contains play counts from undisclosed partners accounting for over a million listeners
    - Useful for showing the relationship between listening habits and the moods of the tracks played
    - General trend that listeners tend to play music that is consistent in terms of mood
    - Consistency ratio: fraction of times it appears in the listening history of a given user
    - Almost two thirds of all plays by a given user contain a mood tag for that users most popular mood

### Experiments ###

- #### Evaluation Metrics: ####
    - Compare the predictive performance of each embedding, given an input embedding of a certain type and how well the predicted moods $\hat{y}$ resemble the true moods associated with the track
    - Macro-averaged average precision as evaluation metric
    - Summarizes the precision-recall curve in a single number:
        - AP = $\sum_{n} (R_n - R_{n-1}) * P_n $
        - Where: Rn and Pn are the recall and precision at the nth threshold at which the recall changes
        - Compute AP for each mood tag and then average for the final result

- #### Audio Based Models: ####
    - Musicnn
        - spectral based CNN for audio tagging
        - employed as main pre-trained audio-based baseline
    - MagnaTagAtune **(MCN-MTT-A)**, and **MCN-MSD-A** 
        - both pre trained to predict 50 tags (a subset of which can be associated with specific moods)
    - extract the activation of the penultimate layer of the model for use as a single embedding per track

- #### Short-Chunk CNN #### 
    - Mel-spectrogram fed through 7-layer CNN with 3x3 filers, 2x2 max-pooling layers, and a fully connected layer before the output

- #### Listening-Based Models: ####
    - Consider user-song interaction as source data
    - Listening data:
        - sparse feedback matrix $Y \in NL * S$
        - where $y_{l,s}$ is a cell in $Y$ representing the number of times the listener $l$ has either played or rated the song $s$
        - playing the song - implicit feedback, rating the song - explicit feedback
    - Taste-Profile
        - listening data from the complete taste profile of play counts to obtain song embeddings by applying weighted matrix factorization using alternating least squares with a rank E = 200
        - **TP-L** - embeddings on how many times which listeners have listened to which songs
    - Proprietary Factorization
        - maps results on open datasets to industrial settings
        - **P-L** - embeddings on user rating over the entire catalog

- #### Transfer Learning: ####
    - Map track level embeddings x from these various sources to the mood tags
    - Transfer learning scenario:
        - “the input embeddings are obtained from a model trained to solve a different (but related) task, such as collaborative filtering or general audio tagging, and then applied for mood prediction by learning f”
    - Model of f:
        - multi-layer perceptron with binary indicator vector as output
        - such that $\hat{y} = f(x)$ where **$\hat{y} \in [0,1]^{|T|}$**
        - thresholding $\hat{y}$ gives the set of predicted moods
        - train f for each embedding type by minimizing binary cross-entropy between predicted vectors $\hat{y}$ and target vectors y obtained from true model tags
    - Optimized learning parameters:
        - **Number of layers, number of units, learning rate, dropout, weight decay**
        - optimized for each embedding type individually using **Bayesian optimization monitoring average precision** on the validation set
    - To limit computational cost: only using TP-L and MCN-MSD-A as input embeddings as they are the main points of comparison
    - Running of MLP:
        - Initialize MLP weights using Kaimig’s method
        - Use rectifier activation function after each layer (output layer uses sigmoid)
        - Input standardized using mean and standard deviation estimated on the training set
        - Trains f for 100 epochs using a cosine-annealed learning rate with restarts and 1-epoch warm-up phase
        - Monitor average precision on the validation set to select the best performing model parameters 

### Results: ###
- #### Overall results: #### 
    - Listening based embeddings (TP-L) outperformed audio-based embeddings (MCN-MSD-A) 
    - variation within audio based models, predicted an outcome of large train size in relation to vocabulary
- #### Tag-Wise Results ####
    - some tags are found to outperform prediction accuracy for audio based methods over listening data
        - explored by subtracting the tag-wise average of TP-L and MCN-MSD-A
        - found 20 tags where audio (MCN-MSD-A) outperforms listening (TP-L)
        - these found tags also are clustered in the same group together when using affinity propogation 
        - suggests audio data outperforms listening data for a specific subspace of moods 
- #### Results by tag frequency: ####
    - all embedding types seem to be equally affected such that model accuracy decreases with further scarcity of tags
- ##### Results of Proprietary algorithms ####
    - P-L out-performed TP-L and is faily easily explained just by the sheer amount of data and stronger signal of explicit feedback (user ratings instead of listens)
- #### Consistency of Audio-Based Models ####
    - "tag-wise results of audio-based models are much more correlated than between audio and lsiteneing-based embeddings"
    - indicates similar aspects are being found by audio embeddings even if they do nor perform as well

### Conclusions: ###

- #### Take aways: ####
    - encourage researchers to use listener-based data that goes beyond just the audio content of a track in order to estimate the mood it conveys
    - Future additions:
        - further investigage tags to understand which moods are more subtible to be extracted by each type of input representation 
        - combine different sources to potentially improve performance of the model
	


### Citations: ####
- This paper citation:

    Filip Korzeniowski, Oriol Nieto, Matthew C. McCallum, Minz Won, Sergio Oramas, and Erik M. Schmidt. Mood Classification Using Listening Data. *arXiv preprint arXiv:2010.11512*, October 2020.

	
- Million song dataset:

    Thierry Bertin-Mahieux, Daniel P. W. Ellis, Brian Whitman, and Paul Lamere. The Million Song Dataset. In Anssi Klapuri and Colby Leider, editors, *Proceedings of the 12th International Society for Music Information Retrieval Conference (ISMIR)*, Miami, USA, October 2011.
