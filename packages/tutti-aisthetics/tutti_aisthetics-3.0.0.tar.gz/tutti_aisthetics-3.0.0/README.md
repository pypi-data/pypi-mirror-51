# A I S T H E T I C S

## What?

This repository contains the `tutti-aisthetics` Python package, which is based on a modified version of the source code [hosted here](https://github.com/idealo/image-quality-assessment).

## Installation

To install production-ready released version, run: `pip install tutti-aisthetics`.

To install for development puprposes, run `pip install -e ./`

## Development

To develop and publish a new version of the `tutti-aisthetics` package, follow these general instructions:

0. Install the package using `pip install -e .` so your changes are instantly reflected in your tests.
1. Modify the source, do tests, etc.
2. Bump the version in `__init__.py` and reflect your changes in `CHANGELOG.md`.
3. Generate a source distribution and a binary wheel for the package with `python setup.py sdist bdist_wheel` (you may require to install `wheel` if it's not installed: `pip install wheel`).
4. Time to upload the new version to PyPI. Say your new version is `2.2.2`, then in `dist/` directory you will find a `tutti_aisthetics-2.2.2.tar.gz` archive and a `tutti_aisthetics-2.2.2-py3-none-any.whl` wheel. You need to upload _both_ files to PyPI. This can be done with `twine` (`pip install twine` if not installed, see [documentation](https://twine.readthedocs.io/en/latest/)) simply by running `twine upload --repository pipy dist/*2.2.2*`.

## Working examples

### Version 3.0.0

```python
from tutti_aisthetics import Scorer

Scorer().score(image_path='/path/to/image.jpg')
```

### Version 2.0.0

#### Prediction

This version allows for a "one line prediction script":
```python
import tutti_aisthetics
import json

nima = tutti_aisthetics.get_aisthetics_model()
result = nima.predict(images='/path/to/image.jpg', augmented=True)
print(json.dumps(result,indent=2))

# One liner is possible albeit not really necessary:
print(json.dumps(tutti_aisthetics.get_aisthetics_model().predict(images='/path/to/image.jpg', augmented=True), indent=2)
```
This should ouptut something like
```
[
  {
    "image": "/path/to/image.jpg",
    "predictions": [
      1.95023458218202e-05,
      0.018782516941428185,
      0.058153558522462845,
      0.15053792297840118,
      0.3187156915664673,
      0.24706070125102997,
      0.120249442756176,
      0.060940422117710114,
      0.02441250905394554,
      0.0011277177836745977
    ],
    "mean_score_prediction": 5.450398804605356,
    "sd_score_prediction": 1.4300220472301666
  }
]
```

### Version 1.0.3

#### Prediction

This version does not support "one line prediction" yet, some preparation is needed.
```python
import json
import pkg_resources

from tutti_aisthetics.evaluater import predictor
from tutti_aisthetics.handlers import model_builder

WEIGHTS_FILE = pkg_resources.resource_filename('tutti_aisthetics', 'model/weights_aisthetic.hdf5')

nima = model_builder.Nima('MobileNet', weights=None)
nima.build()
nima.nima_model.load_weights(WEIGHTS_FILE)

result = predictor.prediction_summary(model=nima,
                                      image_source='path/to/image.jpg',
                                      predictions_file=None,
                                      img_format='jpg')

print(json.dumps(json.loads(result)[0], indent=True))
```
This should output something like:
```
1/1 [==============================] - 0s 118ms/step
{
 "image_id": "42039",
 "predictions": [
  1.872770008048974e-05,
  0.03170372545719147,
  0.07744381576776505,
  0.18988454341888428,
  0.33110326528549194,
  0.21527288854122162,
  0.0972161516547203,
  0.044985581189394,
  0.012080984190106392,
  0.0002903776185121387
 ],
 "mean_score_prediction": 5.154479802262358,
 "sd_score_prediction": 1.4039202179181693
}
```

## Additional information

### Where is the training data?

We did not train the model ourselves, although we could very well do so if necessary using the following datasets.

#### AVA dataset

The most interesting dataset I found for this work is called [AVA](https://www.researchgate.net/publication/261336804_AVA_A_large-scale_database_for_aesthetic_visual_analysis) (Aesthetic Visual Analysis). Consists on a dataset of 255530 images, and for each one we have a histogram of scores from 1 to 10 that around 300 amateur photographers gave them (based on aesthetical value).

It is a rather big dataset (~33GB) so you won't find it in this repository.

#### ImageNet

This is a huge open dataset of labeled images. There are 1000 different categories. For years, researchers have used this dataset as a ground truth and challenge for their models. Every year there is a contest and every year the winner team's model is a breakthrough in the field of image classification and computer vision.

Most image quality assessment models are based on existing CNN architectures for image classification (the ones that are used are of course the winners of the ImageNet challenge). This is because these networks have been trained to detect many features on images of 1000 different categories, which makes them good at most stuff image related. These models build some layers of neurons on top of the baseline CNN to transform their outputs, and retrain the weights on some of the layers using AVA.

### Model

It is called Neural Image Assessment (NIMA). In their paper, the authors implement the same idea over different baseline networks (VGG16, Inception-v2 and MobileNet).

Here, we use MobileNet as the base model, because it seems to be the best performing one. Details aside, MobileNet changes the classic convolution layers by so called _depthwise separable convolutions_ (or more recently _projection layers_). These are computationally cheaper, making this network suitable for running even in portable devices (hence its name).

On top of MobileNet (replacing its output layer), NIMA is a 10 neuron fully connected layer followed by a softmax activation. The loss function used is squared EMD (earth mover's distance), and the data for retraining is the AVA dataset with histogram inputs. Besides this they do more stuff but we don't care about that right now.

### Shortcomings

Even though this model is probably the best performing in the field of aesthetic assessment, a perfect model for such a subjective topic has not been achieved. Check the [hackdays readme](https://gitlab.com/tutti-ch/hackdays-2019/aisthetics/blob/master/README.md#shortcomings) for more information.
