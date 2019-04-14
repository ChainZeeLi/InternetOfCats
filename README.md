# InternetOfCats
EC544 project

### Introduction

With the onset of mass social media, many cat owners have chosen to create dedicated accounts for photos and videos of their cats. Some accounts (e.g. @maruhanamogu, @iamlilbub) have garnered so many followers and sponsorships that their creators have been able to quit their previous jobs and curate these accounts full-time. The average cat owner, however, does not have the time or resources to generate and post captivating cat content on a regular basis. Thus, there is a pressing market need for dedicated software and hardware for the purpose of automating this process and allowing cat owners to keep their audiences entertained via new and exciting posts.

In this project, we will construct an automated cat-based content generator as well as a standalone data storage system. We will test our system in a household containing two cats. The data-gathering portion of this system will consist of a Raspberry Pi equipped with a motion sensor and camera module, and it will be mounted near the cats’ food bowl, so that when a cat walks by the bowl, the sensor will be triggered and the camera module will be brought out of sleep mode in order to take a picture of the cat. After this image is taken and temporarily stored on the Raspberry Pi, it will be sent to the storage system. The data storage system will shard a image file and store the shards across a peer-to-peer network of Raspberry Pis after. Specifically, we will implement APIs for image storing and retrieving services and build a separate storage system so that we can gather and store as many images as needed.

The cat image content generator will call a API to store the captured cat images to the storage system as soon as they are taken. Our peer-to-peer storage network will store a large amount of images, which will later be ranked with machine learning algorithm. Using the TensorFlow API for deep learning, the images will be classified in terms of which cat is in the picture and tagged with the cat’s name. The most aesthetically appealing cat image will be chosen from this pool of images and uploaded to a dedicated Instagram account for the cats, allowing fans of the cats to observe their day-to-day activities and be entertained by their cuteness. 

### Resources
#### Software
* IPFS
* MPI library
* Instagram Account
* Instagram API
* ATLAS (Automatically Tuned Linear Algebra Software) Library
* TensorFlow
#### Hardware
* Raspberry Pi with Raspbian Stretch OS (9.0+)
* Raspberry Pi camera module
* MicroSD card
* wifi adapter
* Motion Sensor, e.g. PARALLAX 555-28027 PIR Passive IR Sensor
* Power cable

![System structure][logo]

[logo]: Diagram.png