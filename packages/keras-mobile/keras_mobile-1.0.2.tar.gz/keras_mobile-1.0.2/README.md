# Keras Mobile
Fast &amp; Compact keras blocks and layers for use in mobile applications

### Currently Implemented:
* `SeperableConvBlock` from MnasNet
* `MobileConvBlock` used in MnasNet & MobileNetV2
    * Generalization of Conv blocks used in both networks
* `MatrixSwish|ScalarSwish` Swish with learnable `beta` parameter
* `Swish` takes a constant scalar for `beta`
* `InstanceLayerNormalization` 
* `AdaptiveInstanceLayerNormalization` from UGATIT

### Current Namespaces:
* `keras_mobile.blocks.conv.{SeperableConvBlock|MobileConvBlock}`
* `keras_mobile.layers.activations.{MatrixSwish|ScalarSwish}`
* `keras_mobile.layers.normalization.{InstanceLayerNormalization|AdaptiveInstanceLayerNormalization}`
* `keras_mobile.functions.{Swish}`

### Notes:
All non-operations (so layers and blocks) are implemented with the same interface as keras.layers.* in that they have a init function which returns a function which in turn takes a tensor as input.

For example:
```py
from keras.layers import Input
from keras_mobile.blocks.conv import SeperableConvBlock

# Create some input x and some network
x = Input((32,32,3))
x = SeperableConvBlock()(x)
x = SeperableConvBlock(16)(x)
```