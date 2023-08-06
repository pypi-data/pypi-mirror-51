from prophesy.sampling.sample_generator import SampleGenerator


class UniformSampleGenerator(SampleGenerator):
    """Generates a uniform grid of samples"""

    def __init__(self, sampler, parameters, region, samples, samples_per_dimension):
        super().__init__(sampler, parameters, region, samples)
        self.samples_per_dimension = samples_per_dimension

    def __iter__(self):
        # There is a special uniform function for samplers (optimization case for PRISM)
        yield self.sampler.perform_uniform_sampling(self.parameters, self.region, self.samples_per_dimension)
