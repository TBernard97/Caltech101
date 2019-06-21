# Caltech101 Image Search

## Introduction

> This was a project for my linear algebra class. It takes a query image and compares it against all image files within a directory for similarity.

> The similar_search.py script will list out the images that are similar while the index.py script actually cycles through images with a wait key (currently 0)

## Code Samples



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

## Installation

> It is highly recommended that you install the latest version of anaconda as that is what was utilized to run all scripts. You can download it from here => https://www.anaconda.com/