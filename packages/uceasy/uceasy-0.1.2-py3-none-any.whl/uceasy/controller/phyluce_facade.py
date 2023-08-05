import os

from uceasy.adapters import assembly
from uceasy.adapters import quality_control
from uceasy.controller import env_manager
from uceasy.use_cases.uce_phylogenomics import UCEPhylogenomics


class Facade:


    def quality_control(self, input, output, sheet, adapter_i7, adapter_i5):

        config_dict = env_manager.prepare_illumiprocessor_conf(sheet,
                                                               adapter_i7,
                                                               adapter_i5)

        config = env_manager.render_conf_file(output + '/illumiprocessor.conf', config_dict)

        return quality_control.run_illumiprocessor(input, output + '/clean_fastq', config)


    def assembly(self, output, assembler, samples):

        config_dict = env_manager.prepare_assembly_conf(output, samples)
        config = env_manager.render_conf_file(output + '/assembly.conf', config_dict)

        return assembly.run_spades(config, output + '/assembly')


    def process_uce(self, output, log, contigs, probes, samples, aligner, charsets, percent, internal_trimming):
        taxon_set_conf = env_manager.render_taxon_set_conf(output + '/taxon-set.conf', samples)

        taxa = str(len(samples))

        processor = UCEPhylogenomics(output, log, contigs, probes, taxon_set_conf, taxa, aligner, charsets, percent, internal_trimming)
        processor.run_uce_processing()
