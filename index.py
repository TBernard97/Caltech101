# import the necessary packages
from imutils import paths
import argparse
import time
import sys
import cv2
import os
import pprint

def dhash(image, hashSize=8):
	# resize the input image, adding a single column (width) so we
	# can compute the horizontal gradient
	resized = cv2.resize(image, (hashSize + 1, hashSize))

	# compute the (relative) horizontal gradient between adjacent
	# column pixels
	diff = resized[:, 1:] > resized[:, :-1]

	# convert the difference image to a hash
	return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

def hamming_distance(s1, s2):
    """Return the Hamming distance between equal-length sequences"""
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length")
    return sum(el1 != el2 for el1, el2 in zip(s1, s2))
	
ap = argparse.ArgumentParser()
ap.add_argument("-a", "--dataset", required=True,
	help="dataset for retrieving images from.")
ap.add_argument("-q", "--query", required=True,
	help="image to query against dataset")

args = vars(ap.parse_args())

print("[INFO] Computing hashes within dataset")

datasetPaths = list(paths.list_images(args["dataset"]))


dataset = {}

start = time.time()

for p in datasetPaths:
	dataset_image = cv2.imread(p)
	if dataset_image is None:
		continue
	dataset_image = cv2.cvtColor(dataset_image, cv2.COLOR_BGR2GRAY)
	imageHash = dhash(dataset_image)

	l = dataset.get(imageHash, [])
	l.append(p)
	dataset[imageHash] = l

print("[INFO] processed {} images in {:.2f} seconds".format(len(dataset), time.time() - start))

print("[INFO] computing query hash")

query_image = cv2.imread(args["query"])
query_image = cv2.cvtColor(query_image, cv2.COLOR_BGR2GRAY)
query_hash = dhash(query_image)
cv2.imshow('query image', query_image)
matchedHashes = dataset.get(query_hash,[])

print("[RESULTS] Matches....")

for matchedHash in matchedHashes:
	print(matchedHash)
	matchedImage = cv2.imread(matchedHash)
	cv2.imshow('matched image', matchedImage)
	cv2.waitKey(0)

cv2.destroyAllWindows()