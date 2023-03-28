from collections import defaultdict
import numpy as np
import operator
from helpers import extractFeature, getGenres
import statistics as st
from scipy.spatial.distance import mahalanobis


def getPrediction(soundFile, dataset, k, genresPath):
    genres = getGenres(genresPath)

    feature = extractFeature(soundFile, 0)
    neighbors = getNeighbors(dataset, feature, k)
    result = nearestClass(neighbors)
    
    return genres[result]


def distance(referenceFeature, feature, k):
    distance = 0
    featureMeanMatrix = feature[0]
    featureCovariance = feature[1]
    referenceMeanMatrix = referenceFeature[0]
    referenceCovariance = referenceFeature[1]
    
    inv_covariance = np.linalg.inv(referenceCovariance)
    distance = mahalanobis(featureMeanMatrix, referenceMeanMatrix, inv_covariance)
    
    # distance = np.trace(np.dot(np.linalg.inv(referenceCovariance), featureCovariance))
    # distance += (np.dot(np.dot((referenceMeanMatrix-featureMeanMatrix).transpose(),
    #              np.linalg.inv(referenceCovariance)), referenceMeanMatrix-featureMeanMatrix))
    # distance += np.log(np.linalg.det(referenceCovariance)) - np.log(np.linalg.det(featureCovariance))
    # distance -= k
    
    return distance


def getNeighbors(trainingSet, instance, k):
    distances = []
    for x in range(len(trainingSet)):
        dist = distance(trainingSet[x], instance, k) + distance(instance, trainingSet[x], k)
        distances.append((trainingSet[x][2], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors


def nearestClass(neighbors):
    np_neighbors = np.array(neighbors)
    return st.mode(np_neighbors)


def getAccuracy(testSet, predictions):
    correct = 0
    for x in range(len(testSet)):
        if testSet[x][-1] == predictions[x]:
            correct += 1
    return 1.0*correct/len(testSet)
