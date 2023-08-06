from data_loading.data_io import Data_IO
from data_loading.interfaces.nifti_io import NIFTI_interface

interface = NIFTI_interface(pattern="case_0000[0-9]", channels=1, classes=3)
data_path = "/home/mudomini/projects/KITS_challenge2019/kits19/data.interpolated/"
data_io = Data_IO(interface, data_path, delete_batchDir=False)
print(data_io.indices_list)

from miscnn.processing.data_augmentation import Data_Augmentation
data_aug = Data_Augmentation(cycles=2,
                             scaling=False, rotations=False,
                             elastic_deform=False, mirror=False,
                             brightness=False, contrast=False,
                             gamma=True, gaussian_noise=True)

from processing.subfunctions.normalization import Normalization
from processing.subfunctions.clipping import Clipping
from processing.subfunctions.resampling import Resampling
from processing.subfunctions.resize import Resize
sf = [Clipping(min=-100, max=500), Normalization(z_score=True), Resampling((3.22, 1.62, 1.62)), Resize((128,128,128))]

from processing.preprocessor import Preprocessor
pp = Preprocessor(data_io, data_aug=data_aug, batch_size=2, subfunctions=sf,
                  prepare_subfunctions=True, prepare_batches=False,
                  analysis="patchwise-crop", patch_shape=(16,16,16))

indices_list = data_io.get_indiceslist()

from neural_network.model import Neural_Network
model = Neural_Network(preprocessor=pp, workers=4, batch_queue_size=4)

# sample = data_io.sample_loader(indices_list[0])
# print(sample.img_data.shape)

# from keras.callbacks import ModelCheckpoint
# cb_model = ModelCheckpoint("submission_model.hdf5", monitor="loss",
#                         c   verbose=1, save_best_only=True, mode="min")


# model.train(indices_list, epochs=3, iterations=6, callbacks=[])

# test = model.predict([indices_list[0]], direct_output=True)
# print(test[0].shape)

# history = model.evaluate(training_samples=[indices_list[0]], validation_samples=[indices_list[1]],
#                          iterations=10)

# from miscnn.evaluation.cross_validation import cross_validation
# cross_validation(indices_list, model, k_fold=3, epochs=3, iterations=10)

from miscnn.evaluation.split_validation import split_validation
split_validation(indices_list[0:7], model, percentage=0.2, epochs=3, iterations=10)

# from miscnn.evaluation.detailed_validation import detailed_validation
# detailed_validation(indices_list, model, evaluation_path="evaluation")

# from utils.visualizer import visualize_sample
# for i in range(0, batches[0][0].shape[0]):
#     img = batches[0][0][i]
#     seg = batches[0][1][i]
#     visualize_sample(img, seg, str(i), "test")


# Initialize Keras Data Generator for generating batches
# from miscnn.neural_network.data_generator import DataGenerator
# dataGen = DataGenerator(sample_list[0:2], pp, training=True, validation=False, shuffle=True)
#
# from miscnn.utils.visualizer import visualize_sample
# import numpy as np
#
# for i, batch in enumerate(dataGen):
#     batch_img = batch[0]
#     batch_seg = batch[1]
#
#     print(str(batch_img[0].shape) + "\t" + str(batch_seg[0].shape))
#     print(str(batch_img[1].shape) + "\t" + str(batch_seg[1].shape))
#
#     batch_seg = np.argmax(batch_seg, axis=-1)
#     batch_seg = np.reshape(batch_seg, batch_seg.shape + (1,))
#     visualize_sample(batch_img[0], batch_seg[0], str(i) + "_batch1", "visualization")
#     visualize_sample(batch_img[1], batch_seg[1], str(i) + "_batch2", "visualization")
