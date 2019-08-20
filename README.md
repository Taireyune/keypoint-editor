# Key Point Editor

**Key Point Editor** is a GUI that allow users to obtain human pose landmark 
coordinates from input videos. Since human pose-estimation inferences are not 
perfect, this tool provide users with the means to edit the coordinates by 
hand for human motion analysis research.

This repository shows the functions and sample code of the GUI. Please email 
tyleryuanwu@gmail.com or alanzhang@gmail.com to request related source code.

## Functions     

* [Human pose inferences from video](https://github.com/Taireyune/keypoint_editor#Human-pose-inference-from-video)
* [Human pose inferences from video](https://github.com/Taireyune/keypoint_editor#Edit-key-point-coordinates)
* [Human pose inferences from video](https://github.com/Taireyune/keypoint_editor#Correction-of-camera-and-movement-based-distortions)
* [Human pose inferences from video](https://github.com/Taireyune/keypoint_editor#Save/load/export-data)

## Human pose inferences from video
### Load video
<img 
src="https://github.com/Taireyune/keypoint_editor/blob/master/images/load_video.png" 
width="840" height="525" alt="load video">
### Apply inference
There is several recognition models to choose from to get the most optimal inference.
The models are based on tf_pose (link to github) with various pre and post processing techniques.
This repository contain a snippet of the post-processing.

### Show and inspect inference
<img 
src="https://github.com/Taireyune/keypoint_editor/blob/master/images/show_inspect.gif" 
alt="inspect inference">

## Edit key point coordinates
### Add and delete objects
<img 
src="https://github.com/Taireyune/keypoint_editor/blob/master/images/add_object.png" 
width="840" height="525" alt="add object">
<img 
src="https://github.com/Taireyune/keypoint_editor/blob/master/images/delete_object.png" 
width="840" height="525" alt="delete object">

### Edit key points
<img 
src="https://github.com/Taireyune/keypoint_editor/blob/master/images/shoulder_edit.gif" 
alt="shoulder edit">
<img 
src="https://github.com/Taireyune/keypoint_editor/blob/master/images/undo.png" 
width="840" height="525" alt="undo edit">

## Distortion corrections
### Camera calibration
<img 
src="https://github.com/Taireyune/keypoint_editor/blob/master/images/camera_calibration.png" 
width="840" height="525" alt="camera calibration">
<img 
src="https://github.com/Taireyune/keypoint_editor/blob/master/images/cmo_parameters.png" 
width="840" height="525" alt="cmo parameters">

### Key point smoothing
<img 
src="https://github.com/Taireyune/keypoint_editor/blob/master/images/smoothing_before.png" 
width="840" height="525" alt="smooth before">
<img 
src="https://github.com/Taireyune/keypoint_editor/blob/master/images/smoothing_settings.png" 
width="840" height="525" alt="smooth settings">
<img 
src="https://github.com/Taireyune/keypoint_editor/blob/master/images/smoothing_after.png" 
width="840" height="525" alt="smooth after">

## Save/load/export data
### Save and load works
Unfinished work can be saved and reloaded. Pixel coordinates and real distances 
(parallel to the camera plane with distoration corrections) can be exported for 2D analysis or further 3D triangulation
with other camera views. 

### export data
<img 
src="https://github.com/Taireyune/keypoint_editor/blob/master/images/exported_data.png" 
width="840" height="525" alt="exported data">


