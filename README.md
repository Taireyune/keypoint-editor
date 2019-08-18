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
![screen shot](https://github.com/Taireyune/keypoint_editor/blob/master/images/load_video.png)

#### Apply inference

apply_inference.png

#### Show and inspect

show_and_inspect.gif

## Edit key point coordinates
#### Add and delete objects

add_delete.png

#### Edit key points

edit_key_points.gif
undo_edits.png

## Distortion corrections
#### Camera calibration

camera_calibration.png
other_parameters.png

#### Key point smoothing

keypoint_smoothing_before.png
keypoint_smoothing_after.png

## Save/load/export data
#### Save and load works
save_load.png

#### export data
export_data.png 



