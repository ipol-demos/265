import os
import json
import numpy as np
import matplotlib.pyplot as plt

FOLDER = "GaitData"
CODE_LIST = [filename.replace(".csv", "") for filename in os.listdir(
    FOLDER) if filename.endswith(".csv")]
COLUMN_NAMES = {'LAV': 0, 'LAX': 1, 'LAY': 2, 'LAZ': 3, 'LRV': 4, 'LRX': 5, 'LRY': 6, 'LRZ': 7,
                'RAV': 8, 'RAX': 9, 'RAY': 10, 'RAZ': 11, 'RRV': 12, 'RRX': 13, 'RRY': 14, 'RRZ': 15}


def load_metadata(subject, trial):
    """Return the metadata dict for the given subject-trial.

    Arguments:
        subject {int} -- Subject number
        trial {int} -- Trial number

    Returns
    -------
    dict
        Metadata
    """

    code = str(subject) + "-" + str(trial)
    fname = os.path.join(FOLDER, code)
    with open(fname + ".json") as metadata_file:
        metadata_dict = json.load(metadata_file)
    return metadata_dict


def load_signal(subject, trial):
    """Return the signal associated with the subject-trial pair.

    Parameters
    ----------
    subject : int
        Subject number
    trial : int
        Trial number

    Returns
    -------
    numpy array
        Signal

    """
    code = str(subject) + "-" + str(trial)
    fname = os.path.join(FOLDER, code)
    signal = np.loadtxt(fname+".csv", delimiter=",", skiprows=1)
    return signal


def print_trial_info(metadata_dict, signal):
    """Dump the trial information in a text file (trial_info.txt)

    Parameters
    ----------
    metadata_dict : dict
        Metadata of the trial.
    signal : numpy array
        Time series of the trial.

    """
    n_samples, _ = signal.shape
    display_dict = {'Subject': "Subject: {Subject}".format(**metadata_dict),
                    'Trial': "Trial: {Trial}".format(**metadata_dict),
                    'Age': "Age (year): {Age}".format(**metadata_dict),
                    'Gender': "Gender: {Gender}".format(**metadata_dict),
                    'Height': "Height (m): {Height}".format(**metadata_dict),
                    'Weight': "Weight (kg): {Weight}".format(**metadata_dict),
                    'PathologyGroup': "Pathology group: {PathologyGroup}".format(**metadata_dict),
                    'WalkingSpeed': "Walking speed (km/h): {WalkingSpeed}".format(**metadata_dict),
                    'Duration': 'Duration (s): {:.1f}'.format(n_samples/100),
                    'LeftGaitCycles': '    - Left foot: {}'.format(len(metadata_dict['LeftFootActivity'])),
                    'RightGaitCycles': '    - Right foot: {}'.format(len(metadata_dict['RightFootActivity'])),
                    'Laterality': "Laterality : {Laterality}".format(**metadata_dict),
                    }
    info_msg = """
    {Subject:^30}|{Trial:^30}
    ------------------------------+------------------------------
    {Age:<30}| {WalkingSpeed:<30}
    {Height:<30}| {Duration:<30}
    {Weight:<30}| Number of footsteps:
    {PathologyGroup:<30}| {LeftGaitCycles:<30}
    {Laterality:<30}| {RightGaitCycles:<30}
    """
    # Dump information
    with open("trial_info.txt", "w") as f:
        print(info_msg.format(**display_dict), file=f)


def dump_plot(signal, metadata_dict, to_plot=["RAV", "RAZ", "RRY"]):

    n_samples, _ = signal.shape
    tt = np.arange(n_samples) / 100

    # get limits
    acc = np.take(signal, indices=[COLUMN_NAMES[dim_name]
                                   for dim_name in to_plot if dim_name[1] == "A"], axis=1)
    if acc.size > 0:
        acc_ylim = [acc.min()-0.1, acc.max()+0.1]
    rot = np.take(signal, indices=[COLUMN_NAMES[dim_name]
                                   for dim_name in to_plot if dim_name[1] == "R"], axis=1)
    if rot.size > 0:
        rot_ylim = [rot.min()-20, rot.max()+20]

    for dim_name in to_plot:
        fig, ax = plt.subplots(figsize=(10, 4))
        # xlim
        ax.set_xlim(0, n_samples/100)
        # plot
        dim = COLUMN_NAMES[dim_name]
        ax.plot(tt, signal[:, dim])
        # ylim
        if dim_name[1] == "A":
            ax.set_ylim(acc_ylim)
        elif dim_name[1] == "R":
            ax.set_ylim(rot_ylim)
        # number of yticks
        plt.locator_params(axis='y', nbins=6)
        # ylabel
        ylabel = "m/s²" if dim_name[1] == "A" else "deg/s"
        ax.set_ylabel(ylabel, fontdict={"size": 20})
        for z in ax.get_yticklabels() + ax.get_xticklabels():
            z.set_fontsize(15)
        # step annotations
        if dim_name[0] == "R":
            steps = metadata_dict["RightFootActivity"]
        elif dim_name[0] == "L":
            steps = metadata_dict["LeftFootActivity"]

        ymin, ymax = ax.get_ylim()
        for start, end in steps:
            ax.vlines([start/100, end/100], ymin, ymax, linestyles="--", lw=1)
            ax.fill_between([start/100, end/100], ymin, ymax,
                            facecolor="green", alpha=0.3)
        fig.tight_layout()
        plt.savefig(dim_name + ".svg", dpi=300,
                    transparent=True, bbox_inches='tight')


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(
        description='Display information and time series for a given trial.')
    parser.add_argument('--subject', metavar='subject', type=int,
                        help='The subject identifier')
    parser.add_argument('--trial', metavar='trial', type=int,
                        help='The trial identifier')
    args = parser.parse_args()

    subject, trial = args.subject, args.trial
    to_plot = ["RAV", "RAZ", "RRY", "LAV", "LAZ", "LRY"]

    # check if the code exists.
    code = str(subject) + "-" + str(trial)
    assert code in CODE_LIST, "The following code does not exist: {}".format(
        code)

    # Check if the signal to display follow the naming convention.
    assert all(
        dim_name in COLUMN_NAMES for dim_name in to_plot), "Check the names of the dimensions to plot."

    # load metadata and signal
    metadata = load_metadata(subject, trial)
    signal = load_signal(subject, trial)
    # dump trial info
    print_trial_info(metadata, signal)
    # dump plots
    dump_plot(signal, metadata, to_plot=to_plot)
