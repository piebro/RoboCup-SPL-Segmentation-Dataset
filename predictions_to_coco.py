def annotations_from_mask_semantic_segmentation(mask):
  annotations = []
  for class_id in np.unique(mask):
    if class_id == 0:
      continue
    class_mask = (mask==class_id)
    im_mask = imantics.Mask(class_mask)
    polygons = im_mask.polygons()
    polygons_new = []
    for poly in polygons:
      polygons_new.append(poly.tolist())
    
    annotation = {
      "category_id": int(class_id),
      "segmentation": polygons_new,
      "bbox": list(im_mask.bbox().bbox()),
    }
    annotations.append(annotation)

  return annotations


def annotations_from_mask_instance_segmentation(class_ids, masks):
  annotations = []
  for i, class_id in enumerate(class_ids): 
    im_mask = imantics.Mask(masks[i])
    polygons = im_mask.polygons()
    polygons_new = []
    for poly in polygons:
      polygons_new.append(poly.tolist())

    annotation = {
      "category_id": int(class_id)+1,
      "segmentation": polygons_new,
      "bbox": list(im_mask.bbox().bbox()),
    }

    annotations.append(annotation)
  
  return annotations


def get_not_annotated_images(all_manual_annotated_json, img_dir):
  all_images = [f for f in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, f))]
  with open(all_manual_annotated_json) as json_file:
    manual_json = json.load(json_file)
  
  manual_images = []
  for img_dict in manual_json["images"]:
    manual_images.append(img_dict["file_name"])

  img_to_annotate = [x for x in all_images if x not in manual_images]
  return img_to_annotate


def filename_annotations_list_to_coco_json(filename_annotations_list, categories):
  images = []
  annotations = []
  categories_json = []

  for i, cat_name in enumerate(categories):
    categories_json.append({"id":i+1, "name":cat_name})

  for img_id, filename_annotations in enumerate(filename_annotations_list):
    images.append({
        "id": img_id,
        "path": filename_annotations["filename"],
        "file_name": filename_annotations["filename"],
    })

    for annotation in filename_annotations["annotations"]:
      annotation["id"] = len(annotations)+1
      annotation["image_id"] = img_id
      annotations.append(annotation)

  return {
      "images":images,
      "annotations":annotations,
      "categories":categories_json
  }


def save_predicted_coco_json(img_dir, img_to_annotate, automatic_annotated_json, get_annotation_func, categories):

  filename_annotations = []
  for i, img_filename in enumerate(img_to_annotate):
    filename_annotations.append({
        "filename": img_filename,
        "annotations": get_annotation_func(os.path.join(img_dir, img_filename))
    })
    sys.stdout.write('\rgenerated annotations to '+str(i+1)+' / '+str(len(img_to_annotate))+' images')
    sys.stdout.flush()
  print()
  
  coco_json = filename_annotations_list_to_coco_json(filename_annotations, categories)

  with open(automatic_annotated_json, 'w') as outfile:
    json.dump(coco_json, outfile)