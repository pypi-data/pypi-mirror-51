from nilearn.image import clean_img, smooth_img
from nipype.utils.filemanip import split_filename
from nipype.interfaces.base import (
    BaseInterfaceInputSpec, TraitedSpec, SimpleInterface,
    ImageFile, File, Directory, traits
    )
import nibabel as nb
import pandas as pd
import os


class DenoiseInputSpec(BaseInterfaceInputSpec):
    fmri_prep = ImageFile(
        exists=True,
        desc='Preprocessed fMRI file',
        mandatory=True
    )

    fmri_prep_aroma = ImageFile(
        desc='ICA-Aroma preprocessed fMRI file',
        mandatory=False
    )

    conf_prep = File(
        exists=True,
        desc="Confound file",
        mandatory=True
    )

    pipeline = traits.Dict(
        desc="Denoising pipeline",
        mandatory=True)

    entities = traits.Dict(
        desc="entities dictionary",
        mandatory=True
    )

    tr_dict = traits.Dict(
        desc="dictionary of tr for all tasks",
        mandatory=True
    )

    output_dir = Directory(
        exists=True,
        desc="Output path"
    )

    high_pass = traits.Float(
        desc="High-pass filter",
    )

    low_pass = traits.Float(
        desc="Low-pass filter"
    )

    smoothing = traits.Bool(
        mandatory=False,
        desc='Optional smoothing'
    )

    ica_aroma = traits.Bool(
        mandatory=False,
        desc='ICA-Aroma files exists'
    )

class DenoiseOutputSpec(TraitedSpec):
    fmri_denoised = File(
        exists=True,
        desc='Denoised fMRI file',
        mandatory=True
    )

class Denoise(SimpleInterface):
    input_spec = DenoiseInputSpec
    output_spec = DenoiseOutputSpec

    def _run_interface(self, runtime):

        smoothing = self.inputs.smoothing
        pipeline_name = self.inputs.pipeline['name']
        pipeline_aroma = self.inputs.pipeline['aroma']
        img = nb.load(self.inputs.fmri_prep)

        if self.inputs.ica_aroma:
            img_aroma = nb.load(self.inputs.fmri_prep_aroma)
            if pipeline_aroma:
                img = img_aroma

        # Handle possibility of null pipeline
        try:
            conf = pd.read_csv(self.inputs.conf_prep,
                               delimiter='\t',
                               #low_memory=False,
                               #engine='python'
                               )
            conf = conf.values
        except pd.errors.EmptyDataError:
            conf = None

        # Determine proper TR
        task = self.inputs.entities['task']
        if task in self.inputs.tr_dict:
            tr = self.inputs.tr_dict[task]
        else:
            raise KeyError(f'{task} TR not found in tr_dict')


        if smoothing and not pipeline_aroma:
           img = smooth_img(img, fwhm=6)

        denoised_img = clean_img(
            img,
            confounds=conf,
            high_pass=self.inputs.high_pass,
            low_pass=self.inputs.low_pass,
            t_r=tr
        )

        _, base, _ = split_filename(self.inputs.fmri_prep)
        denoised_file = f'{self.inputs.output_dir}/{base}_denoised_pipeline-{pipeline_name}.nii.gz'

        nb.save(denoised_img, denoised_file)

        self._results['fmri_denoised'] = denoised_file

        return runtime


# --- TESTS

if __name__ == '__main__':

    ### INPUTS #################################################################
    root = '/home/kmb/Desktop/Neuroscience/Projects/NBRAINGROUP_fmridenoise/test_data/denoising'
    fmri_prep = os.path.join(root, 'sub-pd01_task-rest_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz')
    conf_prep = os.path.join(root, 'confounds_out', 'sub-pd01_task-rest_desc-confounds_regressors_prep.tsv')
    entities = {'task': 'rest'}
    tr_dict = {'rest': 2}
    output_dir = os.path.join(root, 'denoising_out')
    low_pass = 0.08
    high_pass = 0.008

    ### RUN INTERFACE ##########################################################
    dn = Denoise()

    dn.inputs.fmri_prep = fmri_prep
    dn.inputs.conf_prep = conf_prep
    dn.inputs.entities = entities
    dn.inputs.tr_dict = tr_dict
    dn.inputs.output_dir = output_dir
    dn.inputs.low_pass = low_pass
    dn.inputs.high_pass = high_pass

    results = dn.run()
    print(results.outputs)
