> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# P1B numerical result tables

Generated from retained JSON/CSV evidence. AP and IoU are in 0–1 units; a gain of 0.002 is 0.2 percentage points. These tables do not themselves issue a scientific verdict.

## Native numerical closure

| Model | Primary fits | Status | Max gradient | Max native/design IoU difference | Max logit difference | Positive-lambda failures |
|---|---|---|---|---|---|---|
| historical | 505 | PASS | 9.767e-08 | 0.000e+00 | 1.525e-05 | 0/2525 |
| yolo11n-seg | 503 | PASS | 7.815e-08 | 0.000e+00 | 1.548e-05 | 0/2515 |
| yolov8n-seg | 505 | PASS | 9.569e-08 | 0.000e+00 | 1.165e-05 | 0/2525 |
| yolo26n-seg | 495 | PASS | 2.084e-07 | 0.000e+00 | 1.291e-05 | 0/2475 |

## Stable oracle on each model’s own pilot matched set

| Model | Support | Split | N | Native IoU | Stable IoU | Gap | Small control |
|---|---|---|---|---|---|---|---|
| historical | GT | all | 250 | 0.95055 | 0.97996 | 0.02942 | WEAK |
| historical | GT | train | 121 | 0.95055 | 0.97921 | 0.02866 | WEAK |
| historical | GT | val | 129 | 0.95054 | 0.98067 | 0.03013 | WEAK |
| historical | predicted | all | 250 | 0.94210 | 0.97297 | 0.03087 | SUPPORTED |
| historical | predicted | train | 121 | 0.94224 | 0.97132 | 0.02909 | SUPPORTED |
| historical | predicted | val | 129 | 0.94198 | 0.97451 | 0.03254 | SUPPORTED |
| yolo11n-seg | GT | all | 248 | 0.94876 | 0.97945 | 0.03069 | WEAK |
| yolo11n-seg | GT | train | 119 | 0.94976 | 0.97975 | 0.02999 | WEAK |
| yolo11n-seg | GT | val | 129 | 0.94783 | 0.97916 | 0.03133 | WEAK |
| yolo11n-seg | predicted | all | 248 | 0.94107 | 0.97228 | 0.03121 | SUPPORTED |
| yolo11n-seg | predicted | train | 119 | 0.94199 | 0.97166 | 0.02967 | SUPPORTED |
| yolo11n-seg | predicted | val | 129 | 0.94022 | 0.97285 | 0.03263 | SUPPORTED |
| yolo26n-seg | GT | all | 240 | 0.94962 | 0.97954 | 0.02993 | WEAK |
| yolo26n-seg | GT | train | 114 | 0.95017 | 0.97906 | 0.02889 | WEAK |
| yolo26n-seg | GT | val | 126 | 0.94912 | 0.97998 | 0.03086 | WEAK |
| yolo26n-seg | predicted | all | 240 | 0.94077 | 0.97231 | 0.03155 | WEAK |
| yolo26n-seg | predicted | train | 114 | 0.94084 | 0.97033 | 0.02950 | WEAK |
| yolo26n-seg | predicted | val | 126 | 0.94071 | 0.97410 | 0.03340 | WEAK |
| yolov8n-seg | GT | all | 250 | 0.94968 | 0.97914 | 0.02945 | WEAK |
| yolov8n-seg | GT | train | 120 | 0.95275 | 0.97933 | 0.02659 | WEAK |
| yolov8n-seg | GT | val | 130 | 0.94686 | 0.97895 | 0.03210 | WEAK |
| yolov8n-seg | predicted | all | 250 | 0.94044 | 0.97161 | 0.03118 | SUPPORTED |
| yolov8n-seg | predicted | train | 120 | 0.94467 | 0.97174 | 0.02708 | SUPPORTED |
| yolov8n-seg | predicted | val | 130 | 0.93653 | 0.97149 | 0.03496 | SUPPORTED |


Small-control status comes from the pooled model with split adjustment, not a separate test in every displayed split row. All oracle rows use the frozen primary lambda.

## Non-IoU native-to-stable measurements

| Model | Support | Metric | Native mean | Stable mean | Stable minus native |
|---|---|---|---|---|---|
| historical | GT | fp | 133.90800 | 50.64800 | -83.26000 |
| historical | GT | fn | 83.54400 | 45.16400 | -38.38000 |
| historical | GT | symmetric_difference_area | 0.05190 | 0.02034 | -0.03156 |
| historical | GT | boundary_f | 0.95560 | 0.99617 | 0.04058 |
| historical | GT | contour_distance | 0.66333 | 0.25674 | -0.40659 |
| historical | GT | error_per_perimeter | 0.60087 | 0.25091 | -0.34996 |
| historical | predicted | fp | 142.00000 | 44.92800 | -97.07200 |
| historical | predicted | fn | 107.25600 | 74.17600 | -33.08000 |
| historical | predicted | symmetric_difference_area | 0.06203 | 0.02737 | -0.03466 |
| historical | predicted | boundary_f | 0.94784 | 0.99322 | 0.04539 |
| historical | predicted | contour_distance | 0.76879 | 0.33002 | -0.43878 |
| historical | predicted | error_per_perimeter | 0.70405 | 0.32497 | -0.37908 |
| yolo11n-seg | GT | fp | 152.75403 | 53.47581 | -99.27823 |
| yolo11n-seg | GT | fn | 76.01210 | 47.12097 | -28.89113 |
| yolo11n-seg | GT | symmetric_difference_area | 0.05425 | 0.02085 | -0.03340 |
| yolo11n-seg | GT | boundary_f | 0.94781 | 0.99552 | 0.04771 |
| yolo11n-seg | GT | contour_distance | 0.71523 | 0.27053 | -0.44470 |
| yolo11n-seg | GT | error_per_perimeter | 0.63604 | 0.26229 | -0.37375 |
| yolo11n-seg | predicted | fp | 154.93548 | 48.30645 | -106.62903 |
| yolo11n-seg | predicted | fn | 100.63306 | 75.20968 | -25.42339 |
| yolo11n-seg | predicted | symmetric_difference_area | 0.06334 | 0.02805 | -0.03528 |
| yolo11n-seg | predicted | boundary_f | 0.94024 | 0.99105 | 0.05081 |
| yolo11n-seg | predicted | contour_distance | 0.80307 | 0.34341 | -0.45966 |
| yolo11n-seg | predicted | error_per_perimeter | 0.72641 | 0.33684 | -0.38957 |
| yolo26n-seg | GT | fp | 155.75417 | 52.27500 | -103.47917 |
| yolo26n-seg | GT | fn | 75.20833 | 47.06250 | -28.14583 |
| yolo26n-seg | GT | symmetric_difference_area | 0.05329 | 0.02077 | -0.03253 |
| yolo26n-seg | GT | boundary_f | 0.95074 | 0.99597 | 0.04523 |
| yolo26n-seg | GT | contour_distance | 0.70773 | 0.26849 | -0.43923 |
| yolo26n-seg | GT | error_per_perimeter | 0.64277 | 0.26189 | -0.38088 |
| yolo26n-seg | predicted | fp | 162.61250 | 46.90000 | -115.71250 |
| yolo26n-seg | predicted | fn | 100.88750 | 75.00000 | -25.88750 |
| yolo26n-seg | predicted | symmetric_difference_area | 0.06373 | 0.02804 | -0.03569 |
| yolo26n-seg | predicted | boundary_f | 0.94007 | 0.98971 | 0.04964 |
| yolo26n-seg | predicted | contour_distance | 0.81641 | 0.34355 | -0.47286 |
| yolo26n-seg | predicted | error_per_perimeter | 0.74991 | 0.33564 | -0.41426 |
| yolov8n-seg | GT | fp | 152.57600 | 53.32000 | -99.25600 |
| yolov8n-seg | GT | fn | 72.93200 | 46.92800 | -26.00400 |
| yolov8n-seg | GT | symmetric_difference_area | 0.05317 | 0.02118 | -0.03198 |
| yolov8n-seg | GT | boundary_f | 0.94993 | 0.99557 | 0.04564 |
| yolov8n-seg | GT | contour_distance | 0.69948 | 0.26987 | -0.42961 |
| yolov8n-seg | GT | error_per_perimeter | 0.62524 | 0.26299 | -0.36225 |
| yolov8n-seg | predicted | fp | 159.24800 | 47.82400 | -111.42400 |
| yolov8n-seg | predicted | fn | 99.77200 | 76.77200 | -23.00000 |
| yolov8n-seg | predicted | symmetric_difference_area | 0.06419 | 0.02874 | -0.03545 |
| yolov8n-seg | predicted | boundary_f | 0.94067 | 0.99052 | 0.04985 |
| yolov8n-seg | predicted | contour_distance | 0.81273 | 0.35115 | -0.46158 |
| yolov8n-seg | predicted | error_per_perimeter | 0.73735 | 0.34302 | -0.39433 |


These are instance-weighted means on each model’s own matched pilot set. Higher boundary F is better; lower FP/FN, symmetric-difference area, contour distance and error per perimeter are better. FP/FN are absolute input-grid pixels; contour distance is in input pixels. Definitions and empty-mask conventions are in MEASUREMENT_NOTES.md.

## Continuous-area effects after geometric controls

| Model | Support | Outcome | Log-area coefficient | Image-bootstrap interval |
|---|---|---|---|---|
| historical | GT | delta_iou | -0.05352 | [-0.08879, -0.02869] |
| historical | GT | headroom_gain | -0.00403 | [-0.07624, 0.06093] |
| historical | GT | gain_error_per_perimeter | -0.28295 | [-0.51504, -0.10135] |
| historical | GT | gain_boundary_f | -0.08305 | [-0.11755, -0.04875] |
| historical | GT | gain_contour_distance | -0.38837 | [-0.60599, -0.19926] |
| historical | GT | gain_fp | -37.56948 | [-100.32218, 8.57693] |
| historical | GT | gain_fn | -76.13521 | [-192.39432, 30.07208] |
| historical | GT | gain_symmetric_difference_area | -0.05841 | [-0.09452, -0.03272] |
| historical | predicted | delta_iou | -0.06039 | [-0.09713, -0.03244] |
| historical | predicted | headroom_gain | -0.08424 | [-0.16057, -0.01799] |
| historical | predicted | gain_error_per_perimeter | -0.34983 | [-0.62148, -0.10188] |
| historical | predicted | gain_boundary_f | -0.08807 | [-0.13007, -0.04501] |
| historical | predicted | gain_contour_distance | -0.45718 | [-0.71707, -0.21878] |
| historical | predicted | gain_fp | -57.68828 | [-141.65540, 3.98617] |
| historical | predicted | gain_fn | -75.85212 | [-188.82782, 27.60812] |
| historical | predicted | gain_symmetric_difference_area | -0.06854 | [-0.10822, -0.03675] |
| yolo11n-seg | GT | delta_iou | -0.04676 | [-0.06083, -0.03253] |
| yolo11n-seg | GT | headroom_gain | -0.03328 | [-0.08323, 0.01749] |
| yolo11n-seg | GT | gain_error_per_perimeter | -0.24433 | [-0.38044, -0.12280] |
| yolo11n-seg | GT | gain_boundary_f | -0.08474 | [-0.11847, -0.05059] |
| yolo11n-seg | GT | gain_contour_distance | -0.35058 | [-0.52052, -0.18574] |
| yolo11n-seg | GT | gain_fp | -80.97783 | [-127.58135, -39.89189] |
| yolo11n-seg | GT | gain_fn | -8.85347 | [-55.32738, 32.56397] |
| yolo11n-seg | GT | gain_symmetric_difference_area | -0.05392 | [-0.06953, -0.03813] |
| yolo11n-seg | predicted | delta_iou | -0.04945 | [-0.06623, -0.03300] |
| yolo11n-seg | predicted | headroom_gain | -0.09097 | [-0.15980, -0.03362] |
| yolo11n-seg | predicted | gain_error_per_perimeter | -0.25411 | [-0.42776, -0.06919] |
| yolo11n-seg | predicted | gain_boundary_f | -0.08000 | [-0.11409, -0.04306] |
| yolo11n-seg | predicted | gain_contour_distance | -0.36137 | [-0.55335, -0.17594] |
| yolo11n-seg | predicted | gain_fp | -89.13141 | [-144.92682, -33.68708] |
| yolo11n-seg | predicted | gain_fn | -0.24398 | [-41.87240, 36.68747] |
| yolo11n-seg | predicted | gain_symmetric_difference_area | -0.05861 | [-0.07965, -0.03790] |
| yolo26n-seg | GT | delta_iou | -0.03547 | [-0.04832, -0.02395] |
| yolo26n-seg | GT | headroom_gain | 0.02543 | [-0.02257, 0.07174] |
| yolo26n-seg | GT | gain_error_per_perimeter | -0.14898 | [-0.30213, -0.01176] |
| yolo26n-seg | GT | gain_boundary_f | -0.06760 | [-0.09816, -0.03341] |
| yolo26n-seg | GT | gain_contour_distance | -0.28255 | [-0.44995, -0.12828] |
| yolo26n-seg | GT | gain_fp | -68.61374 | [-122.16618, -21.52730] |
| yolo26n-seg | GT | gain_fn | 6.64977 | [-41.44021, 44.80897] |
| yolo26n-seg | GT | gain_symmetric_difference_area | -0.04193 | [-0.05607, -0.02910] |
| yolo26n-seg | predicted | delta_iou | -0.03840 | [-0.05465, -0.02514] |
| yolo26n-seg | predicted | headroom_gain | 0.01359 | [-0.05349, 0.07188] |
| yolo26n-seg | predicted | gain_error_per_perimeter | -0.18330 | [-0.41840, 0.00612] |
| yolo26n-seg | predicted | gain_boundary_f | -0.06849 | [-0.10582, -0.03072] |
| yolo26n-seg | predicted | gain_contour_distance | -0.33013 | [-0.58014, -0.13241] |
| yolo26n-seg | predicted | gain_fp | -75.19485 | [-149.76260, -8.61969] |
| yolo26n-seg | predicted | gain_fn | 11.60184 | [-34.61620, 47.84760] |
| yolo26n-seg | predicted | gain_symmetric_difference_area | -0.04725 | [-0.06963, -0.02980] |
| yolov8n-seg | GT | delta_iou | -0.03986 | [-0.05145, -0.02916] |
| yolov8n-seg | GT | headroom_gain | -0.00088 | [-0.06090, 0.05327] |
| yolov8n-seg | GT | gain_error_per_perimeter | -0.20281 | [-0.33796, -0.09084] |
| yolov8n-seg | GT | gain_boundary_f | -0.06223 | [-0.08858, -0.03910] |
| yolov8n-seg | GT | gain_contour_distance | -0.34703 | [-0.50365, -0.20273] |
| yolov8n-seg | GT | gain_fp | -60.38374 | [-114.50379, -21.79315] |
| yolov8n-seg | GT | gain_fn | -28.47788 | [-100.71390, 25.94541] |
| yolov8n-seg | GT | gain_symmetric_difference_area | -0.04631 | [-0.05978, -0.03359] |
| yolov8n-seg | predicted | delta_iou | -0.04399 | [-0.06226, -0.02869] |
| yolov8n-seg | predicted | headroom_gain | -0.07283 | [-0.14431, -0.00317] |
| yolov8n-seg | predicted | gain_error_per_perimeter | -0.24385 | [-0.45316, -0.04656] |
| yolov8n-seg | predicted | gain_boundary_f | -0.06336 | [-0.09795, -0.03293] |
| yolov8n-seg | predicted | gain_contour_distance | -0.37628 | [-0.59767, -0.18553] |
| yolov8n-seg | predicted | gain_fp | -76.81478 | [-151.84250, -17.27521] |
| yolov8n-seg | predicted | gain_fn | -22.03728 | [-91.98730, 31.62088] |
| yolov8n-seg | predicted | gain_symmetric_difference_area | -0.05406 | [-0.08253, -0.03218] |


Models also adjust for log perimeter, image GT count, nearest-neighbor distance, split and singleton status. Intervals use 1,000 image-cluster bootstrap draws over the 36-image pilot and remain descriptive. Outcomes denote improvement (native error minus stable error, or stable quality minus native quality).

## Scale-adjusted conditioning associations

| Model | Support | Split | Log-condition coefficient | Image-bootstrap interval |
|---|---|---|---|---|
| historical | GT | all | 0.02184 | [-0.01683, 0.05633] |
| historical | GT | train | 0.03774 | [-0.01247, 0.06975] |
| historical | GT | val | 0.00281 | [-0.03614, 0.04991] |
| historical | predicted | all | -0.00439 | [-0.04735, 0.03847] |
| historical | predicted | train | 0.01985 | [-0.04301, 0.06664] |
| historical | predicted | val | -0.03339 | [-0.07884, 0.02189] |
| yolo11n-seg | GT | all | -0.01310 | [-0.03169, 0.00503] |
| yolo11n-seg | GT | train | -0.02615 | [-0.05373, 0.00124] |
| yolo11n-seg | GT | val | -0.00045 | [-0.02356, 0.02112] |
| yolo11n-seg | predicted | all | -0.02887 | [-0.04969, -0.00958] |
| yolo11n-seg | predicted | train | -0.03654 | [-0.07509, -0.00614] |
| yolo11n-seg | predicted | val | -0.02424 | [-0.05284, 0.00364] |
| yolo26n-seg | GT | all | -0.00965 | [-0.03713, 0.01209] |
| yolo26n-seg | GT | train | -0.02543 | [-0.06760, 0.01240] |
| yolo26n-seg | GT | val | 0.00352 | [-0.01758, 0.02596] |
| yolo26n-seg | predicted | all | -0.04351 | [-0.08442, -0.01031] |
| yolo26n-seg | predicted | train | -0.06151 | [-0.11660, -0.00074] |
| yolo26n-seg | predicted | val | -0.02651 | [-0.06729, 0.00769] |
| yolov8n-seg | GT | all | -0.00237 | [-0.02526, 0.01660] |
| yolov8n-seg | GT | train | 0.00677 | [-0.01380, 0.02104] |
| yolov8n-seg | GT | val | -0.01102 | [-0.05145, 0.02406] |
| yolov8n-seg | predicted | all | -0.02873 | [-0.06183, -0.00356] |
| yolov8n-seg | predicted | train | -0.00405 | [-0.04240, 0.02276] |
| yolov8n-seg | predicted | val | -0.05024 | [-0.10225, -0.01107] |


The outcome is native-to-stable IoU gain. These are associations of a column-normalized local design, not evidence that normalization causes a deployment improvement. Train/val consistency and intervention evidence are required before a conditioning mechanism claim.

## Common-GT scope

| Model | Matched / pilot GT | Coverage | Own-set gap | Common N | Common-set gap | Own-set area quartiles |
|---|---|---|---|---|---|---|
| yolo11n-seg | 248/255 | 0.97255 | 0.03121 | 240 | 0.02991 | 424.0, 2124.2, 4856.5, 8796.0, 28640.0 |
| yolo26n-seg | 240/255 | 0.94118 | 0.03155 | 240 | 0.03155 | 424.0, 2137.8, 4906.5, 8804.0, 28640.0 |
| yolov8n-seg | 250/255 | 0.98039 | 0.03118 | 240 | 0.02881 | 424.0, 2120.5, 4802.0, 8738.2, 28640.0 |

## Full validation native detector output

| Model | AP | AP50 | AP75 | Small AP | Medium AP | Large AP | Class 0 AP | Class 1 AP |
|---|---|---|---|---|---|---|---|---|
| yolo11n-seg | 0.83969 | 0.93222 | 0.89163 | 0.59819 | 0.82916 | 0.92880 | 0.87322 | 0.80615 |
| yolov8n-seg | 0.83976 | 0.92995 | 0.89384 | 0.61877 | 0.83084 | 0.92149 | 0.87108 | 0.80845 |
| yolo26n-seg | 0.83514 | 0.92604 | 0.88860 | 0.57666 | 0.82665 | 0.92844 | 0.86475 | 0.80553 |


All 254 val images and 1,803 GT annotations participate. This is COCO-style mask AP on the common 640 input raster with maxDet=300, not original-resolution official benchmark AP.

## Full-val matched diagnostic coverage

| Model | Matched GT / all GT | Matched images | Small matched / all small GT | Small matched images | Native matched IoU | Native small IoU | Native boundary F |
|---|---|---|---|---|---|---|---|
| yolo11n-seg | 1728/1803 | 251 | 108/132 | 43 | 0.93194 | 0.86219 | 0.92220 |
| yolov8n-seg | 1733/1803 | 251 | 106/132 | 45 | 0.93338 | 0.87277 | 0.92238 |
| yolo26n-seg | 1698/1803 | 251 | 96/132 | 40 | 0.93422 | 0.87436 | 0.92370 |


This class-agnostic bbox/confidence diagnostic conditions on localized matches. Full mask AP above uses all 254 images and every GT, including the cases absent from these matched means.

## Every held-out probe and seed

| Probe_seed | Matched IoU | IoU gain | Image-bootstrap interval | Small IoU gain | Boundary F gain | AP | AP gain | AP50 | AP75 | Small AP | Recovered fraction | Recovery N |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P0_42 | 0.93435 | 0.00241 | [0.00139, 0.00343] | 0.00606 | -0.00020 | 0.83986 | 0.00017 | 0.93001 | 0.89031 | 0.58680 | 0.01879 | 98 |
| P0_128 | 0.93426 | 0.00231 | [0.00126, 0.00329] | -0.00061 | -0.00026 | 0.83982 | 0.00014 | 0.92955 | 0.89284 | 0.57799 | 0.06902 | 98 |
| P0_2024 | 0.93448 | 0.00254 | [0.00157, 0.00361] | 0.00422 | 0.00050 | 0.84083 | 0.00115 | 0.92942 | 0.89154 | 0.58658 | 0.01082 | 98 |
| P1_42 | 0.93427 | 0.00233 | [0.00120, 0.00340] | 0.00644 | 0.00066 | 0.84109 | 0.00141 | 0.93170 | 0.88829 | 0.58741 | 0.09161 | 98 |
| P1_128 | 0.93507 | 0.00313 | [0.00224, 0.00400] | 0.00805 | 0.00175 | 0.84308 | 0.00339 | 0.93258 | 0.89184 | 0.59566 | 0.06439 | 98 |
| P1_2024 | 0.93399 | 0.00205 | [0.00104, 0.00296] | 0.00769 | -0.00024 | 0.83914 | -0.00054 | 0.92973 | 0.88822 | 0.59643 | -0.04629 | 98 |
| P2_42 | 0.93472 | 0.00278 | [0.00187, 0.00368] | 0.00945 | -0.00015 | 0.84087 | 0.00119 | 0.93081 | 0.88996 | 0.58912 | 0.07793 | 98 |
| P2_128 | 0.93491 | 0.00297 | [0.00179, 0.00406] | 0.00614 | 0.00155 | 0.84142 | 0.00173 | 0.93114 | 0.89045 | 0.59049 | 0.02521 | 98 |
| P2_2024 | 0.93457 | 0.00263 | [0.00165, 0.00364] | 0.00629 | 0.00083 | 0.84119 | 0.00151 | 0.92748 | 0.88939 | 0.59149 | 0.10238 | 98 |
| P3_42 | 0.93474 | 0.00280 | [0.00189, 0.00370] | 0.00758 | 0.00044 | 0.84222 | 0.00253 | 0.93107 | 0.88967 | 0.59123 | 0.00120 | 98 |
| P3_128 | 0.93495 | 0.00301 | [0.00209, 0.00388] | 0.00676 | 0.00129 | 0.84310 | 0.00341 | 0.93196 | 0.89078 | 0.60171 | 0.10822 | 98 |
| P3_2024 | 0.93395 | 0.00201 | [0.00095, 0.00305] | 0.00387 | -0.00017 | 0.84144 | 0.00176 | 0.93006 | 0.88926 | 0.59315 | 0.02289 | 98 |
| C1_42 | 0.93489 | 0.00294 | [0.00195, 0.00386] | 0.00699 | 0.00125 | 0.84291 | 0.00322 | 0.93195 | 0.88932 | 0.58929 | 0.02414 | 98 |
| C1_128 | 0.93400 | 0.00206 | [0.00095, 0.00313] | 0.00567 | 0.00042 | 0.84117 | 0.00149 | 0.93296 | 0.88902 | 0.59673 | -0.02619 | 98 |
| C1_2024 | 0.93446 | 0.00251 | [0.00139, 0.00364] | 0.00412 | 0.00073 | 0.84215 | 0.00246 | 0.93274 | 0.88849 | 0.59095 | 0.03547 | 98 |
| C2_42 | 0.93478 | 0.00284 | [0.00186, 0.00379] | 0.00490 | 0.00157 | 0.84208 | 0.00240 | 0.93090 | 0.88794 | 0.59617 | 0.10482 | 98 |
| C2_128 | 0.93488 | 0.00294 | [0.00180, 0.00401] | 0.00735 | 0.00157 | 0.84223 | 0.00255 | 0.93006 | 0.88778 | 0.59264 | 0.11943 | 98 |
| C2_2024 | 0.93504 | 0.00309 | [0.00208, 0.00401] | 0.00859 | 0.00140 | 0.84405 | 0.00436 | 0.93070 | 0.88891 | 0.59605 | 0.00309 | 98 |
| C3_42 | 0.93435 | 0.00241 | [0.00139, 0.00343] | 0.00606 | -0.00020 | 0.83986 | 0.00017 | 0.93001 | 0.89031 | 0.58680 | 0.01879 | 98 |
| C3_128 | 0.93426 | 0.00231 | [0.00126, 0.00329] | -0.00061 | -0.00026 | 0.83982 | 0.00014 | 0.92955 | 0.89284 | 0.57799 | 0.06902 | 98 |
| C3_2024 | 0.93448 | 0.00254 | [0.00157, 0.00361] | 0.00422 | 0.00050 | 0.84083 | 0.00115 | 0.92942 | 0.89154 | 0.58658 | 0.01082 | 98 |


Matched metrics condition on the fixed bbox/confidence assignment. Recovery uses only comparable pilot-val matches with stable gap >=0.01; it is not the recovery of the entire val set. P0 and C3 are the same learned-constant null definition. Seed repetitions do not represent independent datasets.

## Measured deployment costs: clean YOLO11, seed 42

| Variant | Learned extra params | MLP FLOPs/candidate | Fixed projection FLOPs/candidate | Projection buffer elements | Mean ms | Median ms | P95 ms | FPS | Peak allocated MiB |
|---|---|---|---|---|---|---|---|---|---|
| native | 0 | 0 | 0 | 0 | 36.341 | 34.128 | 49.576 | 27.52 | 183.4 |
| P0 | 10912 | 21504 | 147456 | 73728 | 37.425 | 36.690 | 44.464 | 26.72 | 183.8 |
| P1 | 10912 | 21504 | 184320 | 92160 | 41.455 | 41.428 | 49.071 | 24.12 | 183.8 |
| P2 | 10912 | 21504 | 165888 | 82944 | 36.224 | 35.673 | 41.250 | 27.61 | 183.9 |
| P3 | 10912 | 21504 | 202752 | 101376 | 37.444 | 36.821 | 42.820 | 26.71 | 183.9 |
| C1 | 10912 | 21504 | 202752 | 101376 | 39.072 | 38.186 | 45.937 | 25.59 | 183.9 |
| C2 | 10912 | 21504 | 202752 | 101376 | 38.737 | 37.898 | 44.647 | 25.81 | 183.9 |
| C3 | 10912 | 21504 | 147456 | 73728 | 37.833 | 36.501 | 46.904 | 26.43 | 183.9 |


Native network: 2,842,998 parameters; THOP estimate 9.787 GFLOPs. MAC=2 FLOPs. ROI interpolation and normalization are additional operations, separately recorded in the resource JSON.


Timing includes CPU letterbox, transfer, the unfused detector, candidate selection, required ROI/projection work, one probe and ready GPU masks. Disk reads and CPU RLE serialization are excluded. Each mode uses 36 synchronized measurements over the same 12 images, after three warmups. Desktop GPU use may remain; all 21 tiny probe weight slices are resident. Allocated VRAM is this process’s PyTorch peak, not total system VRAM.

## Baseline training resources

| Model | Fixed epochs | Train-call minutes | Peak allocated MiB | Final checkpoint SHA256 |
|---|---|---|---|---|
| yolo11n-seg | 30 | 32.54 | 2086.4 | fe653f3463bddc072bb84730b7a1294720af73076686c000b826e15dd9a9399c |
| yolov8n-seg | 30 | 30.65 | 1970.5 | a10be654fd6684698fcfeb30be76fad1ea9c071d802c30ef851991ca10f38ff0 |
| yolo26n-seg | 30 | 46.51 | 2309.3 | 3422b5599731b3bc2919b5ade35880a19300797a190470ffb5dabc549aa3a251 |


Train-call duration includes setup/validation inside the official trainer, but not the prior initialization download. Full stage wall times and exact commands remain in artifacts/runs.
