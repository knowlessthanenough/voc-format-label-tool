enter anaconda prompt
conda activate work
1. run (cmd) $ python cut_frame.py the/path/of/video.mp4 the/folder/want/to/save
   (save path folder need to be open before run)

2. use label studio to label data (there is a limit of photo import in each project)
	# Requires Python >=3.7 <=3.9
	pip install label-studio

	# Start the server at http://localhost:8080
	label-studio

3. After label all data, export it into （Pascal VOC XML） format

4. create a txt file name labels.txt, write all label in it.(each label a row) than put the txt file in the folder output by label studio.
	e.g. man
	     woman
	     plan
	     car

5. run (cmd) $ python change_voc_format.py the/path/of/the/folder

6. (opptional) run (cmd) $ python Image_Processor.py the/path/of/the/folder
   if you can see the image with bbox, it is ok.

7. To combine multiple data folder, run (cmd) $ python combine_multiple_output.py data_all
(data_all switch to the data location whare you put all the data folder)

(the data structure should look like this)
data_all
├── dataset1
│   ├── Annotations
│   ├── ImageSets
│   │   └── Main
│   ├── JPEGImages
│   └── labels.txt
└── dataset2
    ├── Annotations
    ├── ImageSets
    │   └── Main
    ├── JPEGImages
    └── labels.txt

 (that data structure will look like this after step.7)
data_all
├── dataset1
│   ├── Annotations
│   ├── ImageSets
│   │   └── Main
│   ├── JPEGImages
│   └── labels.txt
├── dataset2
│   ├── Annotations
│   ├── ImageSets
│   │   └── Main
│   ├── JPEGImages
│   └── labels.txt
└── combined_file
    ├── Annotations
    ├── ImageSets
    │   └── Main
    └── JPEGImages

8. create a txt file name labels.txt, write all label in it.(each label a row) than put the txt file in the combined_file folder.
	e.g. man
	     woman
	     plan
	     car