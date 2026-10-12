# SPDX-License-Identifier: AGPL-3.0-or-later
"""Cache-independent port of ENG02 COCO AP and P1B reference-grid rasterization."""
import copy
import json
from pathlib import Path
import cv2
import numpy as np
import torch
from pycocotools import mask as maskutil
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval
from ultralytics import YOLO
from ultralytics.data.augment import LetterBox
from ultralytics.utils import ops
from ultralytics.utils.nms import non_max_suppression
from .data import load_prepared, polygons
from .io import fresh_directory, sha256, write_json
from .models import register


def encode(mask):
    rle = maskutil.encode(np.asfortranarray(mask.astype(np.uint8)))
    rle['counts'] = rle['counts'].decode('ascii')
    return rle


def rasterize(xy, width, height, size):
    gain = min(size/width, size/height)
    left = round((size-round(width*gain))/2-.1)
    top = round((size-round(height*gain))/2-.1)
    # P1B rasterization used float64 normalized labels before integer truncation.
    points = xy.astype(np.float64) * [width, height] * gain + [left, top]
    mask = np.zeros((size, size), np.uint8)
    cv2.fillPoly(mask, [points.astype(np.int32)], 1)
    return mask


def coco_metrics(gt, predictions):
    coco = COCO()
    coco.dataset = gt
    coco.createIndex()
    if predictions:
        results = coco.loadRes(copy.deepcopy(predictions))
    else:
        results = COCO()
        results.dataset = dict(images=gt['images'], categories=gt['categories'], annotations=[])
        results.createIndex()
    evaluator = COCOeval(coco, results, 'segm')
    evaluator.params.maxDets = [1, 10, 300]
    evaluator.evaluate()
    evaluator.accumulate()
    precision = evaluator.eval['precision']
    def average(threshold=slice(None), area=0):
        cell = precision[threshold, :, :, area, -1]
        valid = cell[cell > -1]
        return float(valid.mean()) if len(valid) else None
    return dict(AP=average(), AP50=average(0), AP75=average(5), AP90=average(8), AP_small=average(area=1), AP_medium=average(area=2), AP_large=average(area=3), images=len(gt['images']), GT=len(gt['annotations']), detections=len(predictions))


def run(run_dir, data, output, reference_size=640):
    run_dir = Path(run_dir).resolve()
    plan = json.loads((run_dir/'run.json').read_text(encoding='utf-8'))
    receipt = json.loads((run_dir/'completion.json').read_text(encoding='utf-8'))
    checkpoint = run_dir/receipt['checkpoint']
    if receipt['status'] != 'PASS' or sha256(checkpoint) != receipt['checkpoint_sha256']:
        raise ValueError('Missing/changed completed checkpoint')
    root, manifest, manifest_hash = load_prepared(data)
    if manifest_hash != plan['dataset_manifest_sha256']:
        raise ValueError('Evaluation manifest differs from the training run.')
    if reference_size < 64 or reference_size % 32:
        raise ValueError('Reference grid must be >=64 and divisible by 32.')
    folder = fresh_directory(output)
    register(plan['variant'])
    device = torch.device('cpu' if plan['device'] == 'cpu' else 'cuda:'+str(plan['device']))
    torch.set_num_threads(2)
    model = YOLO(str(checkpoint)).model.to(device).float().eval().requires_grad_(False)
    model.model[-1].end2end = False
    nc = len(manifest['names'])
    gt = dict(info={'description':'Portable reference-grid evaluation'}, images=[], annotations=[], categories=[dict(id=i+1, name=name) for i, name in enumerate(manifest['names'])])
    predictions = []
    size = plan['imgsz']
    for iid, row in enumerate([r for r in manifest['samples'] if r['split'] == 'val'], 1):
        image = cv2.imread(str(root/row['image']))
        if image is None:
            raise ValueError(f'Cannot decode {row["image"]}')
        if image.shape[:2] != (row['height'], row['width']):
            raise ValueError('Image geometry differs from manifest; normalize EXIF before preparing data.')
        gt['images'].append(dict(id=iid, file_name=row['image'], width=reference_size, height=reference_size))
        for cls, xy in polygons(root/row['label'], nc):
            mask = rasterize(xy, row['width'], row['height'], reference_size)
            if not mask.any():
                raise ValueError('GT polygon disappeared on reference grid; choose a suitable evaluation protocol.')
            rle = encode(mask)
            gt['annotations'].append(dict(id=len(gt['annotations'])+1, image_id=iid, category_id=cls+1, segmentation=rle, area=int(mask.sum()), bbox=maskutil.toBbox(rle).tolist(), iscrowd=0))
        image = LetterBox(new_shape=(size, size), auto=False)(image=image)
        tensor = torch.from_numpy(np.ascontiguousarray(image[:,:,::-1].transpose(2,0,1))).to(device).float()[None]/255
        with torch.no_grad():
            raw = model(tensor)
            proto = raw[0][1][0]
            detections = non_max_suppression(raw[0][0].clone(), .001, .7, nc=nc, max_det=300, max_time_img=10)[0]
            for start in range(0, len(detections), 16):
                chunk = detections[start:start+16]
                masks = ops.process_mask(proto, chunk[:,6:], chunk[:,:4], (size,size), upsample=True).cpu().numpy().astype(np.uint8)
                for detection, mask in zip(chunk.cpu().numpy(), masks):
                    if size != reference_size:
                        mask = cv2.resize(mask, (reference_size,reference_size), interpolation=cv2.INTER_NEAREST)
                    if mask.any():
                        predictions.append(dict(image_id=iid, category_id=int(detection[5])+1, score=float(detection[4]), segmentation=encode(mask)))
    metrics = coco_metrics(gt, predictions)
    write_json(folder/'gt.json', gt)
    write_json(folder/'predictions.json', predictions)
    result = dict(schema=1, variant=plan['variant'], seed=plan['seed'], role=plan['purpose'], metrics=metrics,
                  protocol=dict(id='coco-mask-reference-grid-v1', reference_size=reference_size, imgsz=size, conf=.001, nms_iou=.7, max_det=300, area_units='reference_grid_pixels', split='val'),
                  dataset_manifest_sha256=manifest_hash, run_config=plan, checkpoint_sha256=sha256(checkpoint), gt_sha256=sha256(folder/'gt.json'), predictions_sha256=sha256(folder/'predictions.json'), test_access=False)
    write_json(folder/'metrics.json', result)
    return result


def replay(folder):
    folder = Path(folder)
    saved = json.loads((folder/'metrics.json').read_text(encoding='utf-8'))
    for name in ['gt','predictions']:
        if sha256(folder/(name+'.json')) != saved[name+'_sha256']:
            raise ValueError(f'{name} changed after evaluation')
    actual = coco_metrics(json.loads((folder/'gt.json').read_text()), json.loads((folder/'predictions.json').read_text()))
    for key, value in actual.items():
        expected = saved['metrics'][key]
        if value is None or expected is None:
            if value != expected:
                raise ValueError(f'Replay mismatch: {key}')
        elif abs(value-expected) > 1e-10:
            raise ValueError(f'Replay mismatch: {key}')
    return {'status':'PASS', 'scope':'saved predictions / same COCO evaluator consistency', 'metrics':actual}
