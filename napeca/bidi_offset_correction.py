# -*- coding: utf-8 -*-

import numpy as np
from scipy import signal

class bidi_offset_correction:

    """
        Input:

            data : np array
                dimensions must be in the format of (samples, y_pixels, x_pixels)

        Output:

            data_corrected : np array
                same dimensions as input; but now odd rows have been shifted accordingly to correct for bidirectional
                offsets

        How to use:

            Step 1) Call bidi_offset_correction with your uncorrected data as a single argument. Assign this object to a variable
                For example: my_bidi_corr_obj = bidi_offset_correction.bidi_offset_correction(data_uncorrected)
                IMPORTANT: USE THIS USER DEFINED OBJECT FOR THE DOWNSTREAM STEPS. You can replace "my_bidi_corr_obj" with whatever you want
                This will store your data in the bidi_offset_correction object for downstream processing

            Step 2) Call my_bidi_corr_obj.compute_mean_image() with no argument. This will
                compute a mean image based on the data in step 1.

            Step 3) Call my_bidi_corr_obj.determine_bidi_offset() with no argument. This will
                calculate the bidirection offset using an fft cross-correlation method.

            Step 4) Call my_bidi_corr_obj.correct_bidi_frames() with no argument. You will have to
                assign it to an output variable; for example:
                    data_corrected = my_bidi_corr_obj.correct_bidi_frames()
                This will apply the offset calculated in step 3 to all frames in the data and output that corrected data

    """

    def __init__(self, data):
        self.data = data

    def compute_mean_image(self):
        self.mean_img = np.mean(self.data, axis=0)
        return self

    def determine_bidi_offset(self):

        even_rows = self.mean_img[::2]
        odd_rows = self.mean_img[1::2]

        # for cross-corr to work, need to have equal number of even and odd rows
        if even_rows.shape[0] != odd_rows.shape[0]:
            min_rows = np.min([even_rows.shape[0], odd_rows.shape[0]])
        else:
            min_rows = even_rows.shape[0]

        # make same length in y dimension
        even_rows = even_rows[:min_rows]
        odd_rows = odd_rows[:min_rows]

        # get rid of averages
        even_rows_mean_sub = even_rows - np.mean(even_rows)
        odd_rows_mean_sub = odd_rows - np.mean(odd_rows)

        # perform fft : https://stackoverflow.com/questions/24768222/how-to-detect-a-shift-between-images
        self.xcorr_bidi = signal.fftconvolve(even_rows_mean_sub, odd_rows_mean_sub[::-1, ::-1], mode='same')
        """ [::-1,::-1] rotates it by 180° (mirrors both horizontally and vertically)
        This is the difference between convolution and correlation, correlation is a convolution 
        with the second signal mirrored.
        """

        xcorr_shape = self.xcorr_bidi.shape
        fft_peak = np.unravel_index(np.argmax(self.xcorr_bidi), xcorr_shape)  # get the peak location of the fft

        self.bidi_offset = int(np.ceil((fft_peak[1] - xcorr_shape[1] / 2.0)))
        print("Calculated bidirectional offset: " + str(self.bidi_offset))

        return self.bidi_offset