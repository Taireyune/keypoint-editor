# Key Point Editor

**Key Point Editor** is a GUI that allow users to obtain human pose landmark 
coordinates from input videos. Since human pose-estimation inferences are not 
perfect, this tool provide users with the means to edit the coordinates by 
hand for human motion analysis research.

This repository shows the functions and sample code of the GUI. Please email 
tyleryuanwu@gmail.com or alanzhang@gmail.com to request related source code.

## Functions     

* Human pose inference from video
* Edit key point coordinates
* Correction of camera and movement based distortions
* Save/load/export data

## Human pose inferences from video
#### Load video
![load video](https://github.com/Taireyune/keypoint_editor/blob/master/images/load_video.png =1260x788)

#### Apply inference
There is several recognition models to choose from to get the most optimal inference.
The models are based on tf_pose (link to github) with various pre and post processing techniques.
This repository contain a snippet of the post-processing.

#### Show and inspect inference
![inspect inference](https://github.com/Taireyune/keypoint_editor/blob/master/images/show_inspect.gif)

## Edit key point coordinates
#### Add and delete objects
![add object](https://github.com/Taireyune/keypoint_editor/blob/master/images/add_object.png =1260x788)
![delete object](https://github.com/Taireyune/keypoint_editor/blob/master/images/delete_object.png)

#### Edit key points
![shoulder edit](https://github.com/Taireyune/keypoint_editor/blob/master/images/shoulder_edit.gif)
![undo edit](https://github.com/Taireyune/keypoint_editor/blob/master/images/undo.png)

## Distortion corrections
#### Camera calibration
![camera calibration](https://github.com/Taireyune/keypoint_editor/blob/master/images/camera_calibration.png =1260x788)
![cmo parameters](https://github.com/Taireyune/keypoint_editor/blob/master/images/cmo_parameters.png =1260x788)

#### Key point smoothing
![smooth before](https://github.com/Taireyune/keypoint_editor/blob/master/images/smoothing_before.png =1260x788)
![smooth settings](https://github.com/Taireyune/keypoint_editor/blob/master/images/smoothing_settings.png =1260x788)
![smooth after](https://github.com/Taireyune/keypoint_editor/blob/master/images/smoothing_after.png =1260x788)

## Save/load/export data
#### Save and load works
Unfinished work can be saved and reloaded. Pixel coordinates or real distances 
parallel to the camera plane can be exported for 2D analysis or further 3D triangulation
with other camera views. 

#### export data
![exported data](https://github.com/Taireyune/keypoint_editor/blob/master/images/exported_data.png =1260x788)



