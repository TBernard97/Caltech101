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


def hamming_distance(str1, str2):
    """Count the # of differences between equal length strings str1 and str2"""
    diffs = 0
    for ch1, ch2 in zip(str1, str2):
        if ch1 != ch2:
                diffs += 1
    return diffs

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

print("[INFO] computing query hash search")

query_image = cv2.imread(args["query"])
query_image = cv2.cvtColor(query_image, cv2.COLOR_BGR2GRAY)
query_hash = dhash(query_image)
cv2.imshow('query image', query_image)

for dataset_hash in dataset:
    difference = hamming_distance(str(query_hash),str(dataset_hash))
    if(difference < 16):
        path = dataset.get(dataset_hash,[])
        print(path)