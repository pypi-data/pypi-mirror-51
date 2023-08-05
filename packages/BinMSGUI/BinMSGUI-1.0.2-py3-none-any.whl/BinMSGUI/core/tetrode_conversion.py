import numpy as np
from core.readMDA import readMDA
import os
from core.utils import find_sub
from core.Tint_Matlab import get_setfile_parameter
from core.cut_creation import create_cut
import struct
import datetime


def get_tetrode_parameters(set_filename, samples_per_spike=50, rawRate=48e3):
    parameters = ['trial_date', 'trial_time', 'experimenter', 'comments', 'duration', 'sw_version']

    tetrode_parameters = {'samples_per_spike': samples_per_spike,
                          'rawRate': str(int(rawRate))}

    for x in parameters:
        tetrode_parameters[x] = get_setfile_parameter(x, set_filename)

    return tetrode_parameters


def write_tetrode(filepath, spike_times, spike_data, tetrode_parameters):
    # Note, this can be optimized instead of writing each tetrode one at a time

    with open(filepath, 'w') as f:
        date = 'trial_date %s' % (tetrode_parameters['trial_date'])
        time_head = '\ntrial_time %s' % (tetrode_parameters['trial_time'])
        experimenter = '\nexperimenter %s' % (tetrode_parameters['experimenter'])
        comments = '\ncomments %s' % (tetrode_parameters['comments'])

        duration = '\nduration %s' % (int(tetrode_parameters['duration']))

        sw_vers = '\nsw_version %s' % (tetrode_parameters['sw_version'])
        num_chans = '\nnum_chans 4'
        timebase_head = '\ntimebase %d hz' % (96000)
        bp_timestamp = '\nbytes_per_timestamp %d' % (4)
        # samps_per_spike = '\nsamples_per_spike %d' % (int(Fs*1e-3))
        samps_per_spike = '\nsamples_per_spike %d' % (int(tetrode_parameters['samples_per_spike']))
        sample_rate = '\nsample_rate %d hz' % (int(tetrode_parameters['rawRate']))
        b_p_sample = '\nbytes_per_sample %d' % (1)
        # b_p_sample = '\nbytes_per_sample %d' % (4)
        spike_form = '\nspike_format t,ch1,t,ch2,t,ch3,t,ch4'

        num_spikes = '\nnum_spikes %d' % (spike_data.shape[1])
        start = '\ndata_start'

        write_order = [date, time_head, experimenter, comments, duration, sw_vers, num_chans, timebase_head,
                       bp_timestamp,
                       samps_per_spike, sample_rate, b_p_sample, spike_form, num_spikes, start]

        f.writelines(write_order)

    spike_data = np.swapaxes(spike_data, 0, 1)

    n, n_channels, clip_size = spike_data.shape  # n spikes

    # re-shaping the data so that the channels are concatenated such that
    # the 0th dimension is n_channels * n_spikes, and the 1st dimension of the array
    # is the clip size (samples per spike).
    spike_data = spike_data.reshape((n_channels * n, clip_size))

    # when writing the spike times we write it for each channel, so lets tile
    spike_times = np.tile(spike_times, (n_channels, 1))
    spike_times = spike_times.flatten(order='F')

    # this will create a (n_samples, n_channels, n_samples_per_spike) => (n, 4, 50) sized matrix, we will create a
    # matrix of all the samples and channels going from ch1 -> ch4 for each spike time
    # time1 ch1_data
    # time1 ch2_data
    # time1 ch3_data
    # time1 ch4_data
    # time2 ch1_data
    # time2 ch2_data
    # .
    # .
    # .
    spike_array = np.hstack((spike_times.reshape(len(spike_times), 1), spike_data))

    spike_times = None
    spike_values = None

    spike_n = spike_array.shape[0]
    t_packed = struct.pack('>%di' % spike_n, *spike_array[:, 0].astype(int))
    spike_array = spike_array[:, 1:]  # removing time data from this matrix to save memory

    spike_data_pack = struct.pack('<%db' % (spike_n * clip_size), *spike_array.astype(int).flatten())

    spike_array = None

    # now we need to combine the lists by alternating

    comb_list = [None] * (2 * spike_n)
    comb_list[::2] = [t_packed[i:i + 4] for i in range(0, len(t_packed), 4)]  # breaks up t_packed into a list,
    # each timestamp is one 4 byte integer
    comb_list[1::2] = [spike_data_pack[i:i + 50] for i in range(0, len(spike_data_pack), 50)]  # breaks up spike_data_
    # pack and puts it into a list, each spike is 50 one byte integers

    t_packed = None
    spike_data_pack = None

    write_order = []
    with open(filepath, 'rb+') as f:
        write_order.extend(comb_list)
        write_order.append(bytes('\r\ndata_end\r\n', 'utf-8'))

        f.seek(0, 2)
        f.writelines(write_order)


def convert_tetrode(filt_filename, data_filename, output_basename, pre_spike=15, post_spike=35, self=None):
    """
    convert_tetrode will take an input filename that was processed and sorted via MountainSort
    and convert the MountainSorted output to a Tint output.

    Args:
        filt_filename (str): this is the fullpath of the file that was pre-processed/sorted using MountainSort
        self (bool): this refers to the self of a QtGui, that has a QTextEdit displaying logs. There is a method called
            LogAppend that prints the current status of the Gui to the TextEdit.
    Returns:
        None
    """

    msg = '[%s %s]: Converting the MountainSort output following filename to Tint: %s' % (str(datetime.datetime.now().date()),
                                                                            str(datetime.datetime.now().time())[
                                                                            :8], filt_filename)
    cell_numbers = None
    tetrode_skipped = False

    if self is None:
        print(msg)
    else:
        self.LogAppend.myGUI_signal_str.emit(msg)

    directory = os.path.dirname(filt_filename)

    mda_basename = os.path.splitext(filt_filename)[0]
    mda_basename = mda_basename[:find_sub(mda_basename, '_')[-1]]

    tint_basename = mda_basename[:find_sub(mda_basename, '_')[-1]]

    # set_filename = '%s.set' % (os.path.join(directory, tint_basename))
    set_filename = '%s.set' % output_basename

    tetrode = int(mda_basename[find_sub(mda_basename, '_')[-1] + 2:])

    # new_basename = '%s_ms' % tint_basename
    # tetrode_filepath = '%s.%d' % (os.path.join(directory, new_basename), tetrode)
    tetrode_filepath = '%s.%d' % (output_basename, tetrode)

    if os.path.exists(tetrode_filepath):
        msg = '[%s %s]: The following file already exists: %s, skipping conversion!' % (
        str(datetime.datetime.now().date()),
        str(datetime.datetime.now().time())[
        :8], tetrode_filepath)

        if self is None:
            print(msg)
        else:
            self.LogAppend.myGUI_signal_str.emit(msg)

        tetrode_skipped = True

    else:
        # masked_out_fname = mda_basename + '_masked.mda'
        firings_out = mda_basename + '_firings.mda'

        # ----------- reading in mountainsort spike data ------------------------- #

        if not os.path.exists(firings_out):

            msg = '[%s %s]: The following spike filename does not exist: %s, skipping!' % (
                str(datetime.datetime.now().date()),
                str(datetime.datetime.now().time())[
                :8], firings_out)

            if self is None:
                print(msg)
            else:
                self.LogAppend.myGUI_signal_str.emit(msg)

            raise FileNotFoundError('Could not find the following spike filename: %s' % firings_out)

        msg = '[%s %s]: Reading the spike data from the following file: %s' % (
            str(datetime.datetime.now().date()),
            str(datetime.datetime.now().time())[
            :8], firings_out)

        if self is None:
            print(msg)
        else:
            self.LogAppend.myGUI_signal_str.emit(msg)

        A, _ = readMDA(firings_out)

        # spike_channel = A[0, :].astype(int)
        spike_times = A[1, :].astype(int)  # at this stage it is in index values (0-based)
        cell_numbers = A[2, :].astype(int)
        # ------------- creating clips ---------------------- #

        # if not os.path.exists(masked_out_fname):
        if not os.path.exists(data_filename):
            msg = '[%s %s]: The following data filename does not exist: %s, skipping!' % (
                str(datetime.datetime.now().date()),
                str(datetime.datetime.now().time())[
                :8], data_filename)

            if self is None:
                print(msg)
            else:
                self.LogAppend.myGUI_signal_str.emit(msg)

            raise FileNotFoundError('Could not find the following data file: %s' % data_filename)

        msg = '[%s %s]: Reading the spike data from the following file: %s' % (
            str(datetime.datetime.now().date()),
            str(datetime.datetime.now().time())[
            :8], firings_out)

        if self is None:
            print(msg)
        else:
            self.LogAppend.myGUI_signal_str.emit(msg)

        # read in masked data
        # data_masked, _ = readMDA(masked_out_fname)
        data_out, _ = readMDA(data_filename)

        # get the tint spike information, placing the event at the 11th index
        clip_size = pre_spike + post_spike
        if clip_size != 50:
            raise ValueError("pre_spike (%d) and post_spike (%d) must add up to be a clip size of 50!" % (
                pre_spike, post_spike))

        # max sample index
        # max_n = data_masked.shape[1] - 1
        max_n = data_out.shape[1] - 1

        # making sure now
        spike_bool = np.where((spike_times + post_spike < max_n) * (spike_times - pre_spike >= 0))[0]

        # spike_channel = spike_channel[spike_bool]
        spike_times = spike_times[spike_bool]
        cell_numbers = cell_numbers[spike_bool]

        spike_bool = None

        clip_indices = np.tile(spike_times, (clip_size, 1)).T + np.arange(-pre_spike, post_spike)

        # getting the clip values

        # cell_data = data_masked[:, clip_indices]
        cell_data = data_out[:, clip_indices]

        # data_masked = None
        data_out = None
        # ------------------- getting spike times --------------------------------- #

        Fs = int(get_setfile_parameter('rawRate', set_filename))

        cell_times = (spike_times * (96000 / Fs)).astype(
            int)  # need to convert to the 96000 Hz timebase that Tint has, time occurs at the 12th value

        cell_data = np.divide(cell_data, 256).astype(int)  # converting from int16 back to int8

        tetrode_parameters = get_tetrode_parameters(set_filename, samples_per_spike=50, rawRate=Fs)

        msg = '[%s %s]: Creating the following tetrode file: %s!' % (
            str(datetime.datetime.now().date()),
            str(datetime.datetime.now().time())[
            :8], tetrode_filepath)

        if self is None:
            print(msg)
        else:
            self.LogAppend.myGUI_signal_str.emit(msg)

        write_tetrode(tetrode_filepath, cell_times, cell_data, tetrode_parameters)

    # ------------ creating the cut file ----------------------- #

    # output_basename = '%s_ms' % tint_basename
    clu_filename = '%s.clu.%d' % (os.path.join(directory, output_basename), tetrode)
    cut_filename = '%s_%d.cut' % (os.path.join(directory, output_basename), tetrode)

    if os.path.exists(cut_filename):
        msg = '[%s %s]: The following cut file already exists: %s, skipping conversion!' % (
            str(datetime.datetime.now().date()),
            str(datetime.datetime.now().time())[
            :8], cut_filename)

        if self is None:
            print(msg)
        else:
            self.LogAppend.myGUI_signal_str.emit(msg)
    else:

        msg = '[%s %s]: Creating the following cut file: %s!' % (
            str(datetime.datetime.now().date()),
            str(datetime.datetime.now().time())[
            :8], cut_filename)

        if self is None:
            print(msg)
        else:
            self.LogAppend.myGUI_signal_str.emit(msg)

        if tetrode_skipped:
            firings_out = mda_basename + '_firings.mda'
            # masked_out_fname = mda_basename + '_masked.mda'

            A, _ = readMDA(firings_out)

            spike_times = (A[1, :]).astype(int)  # at this stage it is in index values (0-based)
            cell_numbers = A[2, :].astype(int)

            pre_spike = 11
            post_spike = 39

            # max sample index

            data_out, _ = readMDA(data_filename)
            # data_masked, _ = readMDA(masked_out_fname)

            # max_n = data_masked.shape[1] - 1
            max_n = data_out.shape[1] - 1

            spike_bool = np.where((spike_times + post_spike < max_n) * (spike_times - pre_spike >= 0))[0]

            spike_times = None
            cell_numbers = cell_numbers[spike_bool]

        create_cut(cut_filename, clu_filename, cell_numbers, tetrode, tint_basename, output_basename, self=self)


def batch_basename_tetrodes(directory, tint_basename, output_basename,  pre_spike=15, post_spike=35, mask=True,
                            self=None):

    # find the filenames that were used by MountainSort to be sorted.
    filt_fnames = [os.path.join(directory, file) for file in os.listdir(
        directory) if '_filt.mda' in file if os.path.basename(tint_basename) in file]

    for file in filt_fnames:
        try:
            if mask:
                # previously I made it so you only have the option of using the masked data as the output
                mda_basename = os.path.splitext(file)[0]
                mda_basename = mda_basename[:find_sub(mda_basename, '_')[-1]]
                data_filename = mda_basename + '_masked.mda'
            else:
                # if the user decides not to use the masked value, the filtered data will be used.
                data_filename = file

            convert_tetrode(file, data_filename, output_basename,  pre_spike=pre_spike, post_spike=post_spike,
                            self=self)
        except FileNotFoundError:
            continue
