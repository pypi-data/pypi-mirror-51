import os
import unittest

from cmdstanpy.cmdstan_args import SamplerArgs, CmdStanArgs
from cmdstanpy.utils import EXTENSION
from cmdstanpy.model import Model
from cmdstanpy.stanfit import StanFit
from contextlib import contextmanager
import logging
from multiprocessing import cpu_count
import numpy as np
import sys
from testfixtures import LogCapture

here = os.path.dirname(os.path.abspath(__file__))
datafiles_path = os.path.join(here, 'data')

code = '''data {
  int<lower=0> N;
  int<lower=0,upper=1> y[N];
}
parameters {
  real<lower=0,upper=1> theta;
}
model {
  theta ~ beta(1,1);
  for (n in 1:N)
    y[n] ~ bernoulli(theta);
}
'''


class ModelTest(unittest.TestCase):
    def test_model_good(self):
        stan = os.path.join(datafiles_path, 'bernoulli.stan')
        exe = os.path.join(datafiles_path, 'bernoulli' + EXTENSION)

        model = Model(stan_file=stan)
        self.assertEqual(stan, model.stan_file)
        self.assertEqual(None, model.exe_file)

        model = Model(stan_file=stan, exe_file=exe)
        self.assertEqual(exe, model.exe_file)

    def test_model_good_no_source(self):
        exe = os.path.join(datafiles_path, 'bernoulli' + EXTENSION)
        model = Model(exe_file=exe)
        self.assertEqual(exe, model.exe_file)
        self.assertEqual('bernoulli', model.name)

        with self.assertRaises(RuntimeError):
            model.code()
        with self.assertRaises(RuntimeError):
            model.compile()

    def test_model_none(self):
        with self.assertRaises(ValueError):
            _ = Model(exe_file=None, stan_file=None)

    def test_model_bad(self):
        with self.assertRaises(Exception):
            model = Model(stan_file='xdlfkjx', exe_file='sdfndjsds')

        stan = os.path.join(datafiles_path, 'b')
        with self.assertRaises(Exception):
            model = Model(stan_file=stan)

    def test_repr(self):
        stan = os.path.join(datafiles_path, 'bernoulli.stan')
        model = Model(stan_file=stan)
        s = repr(model)
        self.assertIn('name=bernoulli', s)

    def test_print(self):
        stan = os.path.join(datafiles_path, 'bernoulli.stan')
        model = Model(stan_file=stan)
        self.assertEqual(code, model.code())

    def test_model_compile(self):
        stan = os.path.join(datafiles_path, 'bernoulli.stan')
        exe = os.path.join(datafiles_path, 'bernoulli' + EXTENSION)
        model = Model(stan_file=stan)
        self.assertEqual(None, model.exe_file)
        model.compile()
        self.assertTrue(model.exe_file.endswith(exe.replace('\\', '/')))

        model = Model(stan_file=stan)
        if os.path.exists(exe):
            os.remove(exe)
        model.compile()
        self.assertTrue(model.exe_file.endswith(exe.replace('\\', '/')))

        stan = os.path.join(datafiles_path, 'bernoulli_include.stan')
        exe = os.path.join(datafiles_path, 'bernoulli_include' + EXTENSION)
        here = os.path.dirname(os.path.abspath(__file__))
        datafiles_abspath = os.path.join(here, 'data')
        include_paths = [datafiles_abspath]
        if os.path.exists(exe):
            os.remove(exe)
        model = Model(stan_file=stan)
        model.compile(include_paths=include_paths)
        self.assertEqual(stan, model.stan_file)
        self.assertTrue(model.exe_file.endswith(exe.replace('\\', '/')))

    # TODO: test compile with existing exe - timestamp on exe unchanged
    # TODO: test overwrite with existing exe - timestamp on exe updated


class OptimizeTest(unittest.TestCase):
    def test_optimize_works(self):
        exe = os.path.join(datafiles_path, 'bernoulli' + EXTENSION)
        stan = os.path.join(datafiles_path, 'bernoulli.stan')
        model = Model(stan_file=stan, exe_file=exe)
        jdata = os.path.join(datafiles_path, 'bernoulli.data.json')
        jinit = os.path.join(datafiles_path, 'bernoulli.init.json')
        fit = model.optimize(
            data=jdata,
            seed=1239812093,
            inits=jinit,
            algorithm='BFGS',
            init_alpha=0.001,
            iter=100,
        )

        # check if calling sample related stuff fails
        with self.assertRaises(RuntimeError):
            fit.summary()
        with self.assertRaises(RuntimeError):
            _ = fit.sample
        with self.assertRaises(RuntimeError):
            fit.diagnose()

        # test numpy output
        self.assertAlmostEqual(fit.optimized_params_np[0], -5, places=2)
        self.assertAlmostEqual(fit.optimized_params_np[1], 0.2, places=3)

        # test pandas output
        self.assertEqual(
            fit.optimized_params_np[0], fit.optimized_params_pd['lp__'][0]
        )
        self.assertEqual(
            fit.optimized_params_np[1], fit.optimized_params_pd['theta'][0]
        )

        # test dict output
        self.assertEqual(
            fit.optimized_params_np[0], fit.optimized_params_dict['lp__']
        )
        self.assertEqual(
            fit.optimized_params_np[1], fit.optimized_params_dict['theta']
        )

    def test_optimize_works_dict(self):
        import json

        exe = os.path.join(datafiles_path, 'bernoulli' + EXTENSION)
        stan = os.path.join(datafiles_path, 'bernoulli.stan')
        model = Model(stan_file=stan, exe_file=exe)
        with open(os.path.join(datafiles_path, 'bernoulli.data.json')) as d:
            data = json.load(d)
        with open(os.path.join(datafiles_path, 'bernoulli.init.json')) as d:
            init = json.load(d)
        fit = model.optimize(
            data=data,
            seed=1239812093,
            inits=init,
            algorithm='BFGS',
            init_alpha=0.001,
            iter=100,
        )

        # test numpy output
        self.assertAlmostEqual(fit.optimized_params_np[0], -5, places=2)
        self.assertAlmostEqual(fit.optimized_params_np[1], 0.2, places=3)


class SampleTest(unittest.TestCase):
    def test_bernoulli_good(self):
        stan = os.path.join(datafiles_path, 'bernoulli.stan')
        exe = os.path.join(datafiles_path, 'bernoulli' + EXTENSION)
        bern_model = Model(stan_file=stan, exe_file=exe)
        bern_model.compile()

        jdata = os.path.join(datafiles_path, 'bernoulli.data.json')
        bern_fit = bern_model.sample(
            data=jdata, chains=4, cores=2, seed=12345, sampling_iters=100
        )

        for i in range(bern_fit.chains):
            csv_file = bern_fit.csv_files[i]
            txt_file = ''.join([os.path.splitext(csv_file)[0], '.txt'])
            self.assertTrue(os.path.exists(csv_file))
            self.assertTrue(os.path.exists(txt_file))

        self.assertEqual(bern_fit.chains, 4)
        self.assertEqual(bern_fit.draws, 100)
        column_names = [
            'lp__',
            'accept_stat__',
            'stepsize__',
            'treedepth__',
            'n_leapfrog__',
            'divergent__',
            'energy__',
            'theta',
        ]
        self.assertEqual(bern_fit.column_names, tuple(column_names))

        bern_sample = bern_fit.sample
        self.assertEqual(bern_sample.shape, (100, 4, len(column_names)))

        self.assertEqual(bern_fit.metric_type, 'diag_e')
        self.assertEqual(bern_fit.stepsize.shape, (4,))
        self.assertEqual(bern_fit.metric.shape, (4, 1))

        output = os.path.join(datafiles_path, 'test1-bernoulli-output')
        bern_fit = bern_model.sample(
            data=jdata,
            chains=4,
            cores=2,
            seed=12345,
            sampling_iters=100,
            csv_basename=output,
        )
        for i in range(bern_fit.chains):
            csv_file = bern_fit.csv_files[i]
            txt_file = ''.join([os.path.splitext(csv_file)[0], '.txt'])
            self.assertTrue(os.path.exists(csv_file))
            self.assertTrue(os.path.exists(txt_file))
        bern_sample = bern_fit.sample
        self.assertEqual(bern_sample.shape, (100, 4, len(column_names)))
        for i in range(bern_fit.chains):  # cleanup datafile_path dir
            os.remove(bern_fit.csv_files[i])
            os.remove(bern_fit.console_files[i])

        rdata = os.path.join(datafiles_path, 'bernoulli.data.R')
        bern_fit = bern_model.sample(
            data=rdata, chains=4, cores=2, seed=12345, sampling_iters=100
        )
        bern_sample = bern_fit.sample
        self.assertEqual(bern_sample.shape, (100, 4, len(column_names)))

        data_dict = {'N': 10, 'y': [0, 1, 0, 0, 0, 0, 0, 0, 0, 1]}
        bern_fit = bern_model.sample(
            data=data_dict, chains=4, cores=2, seed=12345, sampling_iters=100
        )
        bern_sample = bern_fit.sample
        self.assertEqual(bern_sample.shape, (100, 4, len(column_names)))

        # check if  optimized_params_np returns first draw
        # (actually first row from csv)
        np.testing.assert_equal(
            bern_fit.get_drawset().iloc[0].values, bern_fit.optimized_params_np
        )

    def test_bernoulli_bad(self):
        stan = os.path.join(datafiles_path, 'bernoulli.stan')
        exe = os.path.join(datafiles_path, 'bernoulli' + EXTENSION)
        bern_model = Model(stan_file=stan, exe_file=exe)
        bern_model.compile()

        with self.assertRaisesRegex(Exception, 'Error during sampling'):
            bern_fit = bern_model.sample(
                chains=4, cores=2, seed=12345, sampling_iters=100
            )

    def test_multi_proc(self):
        logistic_stan = os.path.join(datafiles_path, 'logistic.stan')
        logistic_model = Model(stan_file=logistic_stan)
        logistic_model.compile()
        logistic_data = os.path.join(datafiles_path, 'logistic.data.R')

        with LogCapture() as log:
            logger = logging.getLogger()
            fit = logistic_model.sample(data=logistic_data, chains=4, cores=1)
        log.check_present(
            ('cmdstanpy', 'INFO', 'finish chain 1'),
            ('cmdstanpy', 'INFO', 'start chain 2'),
        )
        with LogCapture() as log:
            logger = logging.getLogger()
            fit = logistic_model.sample(data=logistic_data, chains=4, cores=2)
        if cpu_count() >= 4:
            # finish chains 1, 2 before starting chains 3, 4
            log.check_present(
                ('cmdstanpy', 'INFO', 'finish chain 1'),
                ('cmdstanpy', 'INFO', 'start chain 4'),
            )
        if cpu_count() >= 4:
            with LogCapture() as log:
                logger = logging.getLogger()
                fit = logistic_model.sample(
                    data=logistic_data, chains=4, cores=4
                )
                log.check_present(
                    ('cmdstanpy', 'INFO', 'start chain 4'),
                    ('cmdstanpy', 'INFO', 'finish chain 1'),
                )


class GenerateQuantitiesTest(unittest.TestCase):
    def test_gen_quantities_good(self):
        stan = os.path.join(datafiles_path, 'bernoulli_ppc.stan')
        model = Model(stan_file=stan)
        model.compile()

        jdata = os.path.join(datafiles_path, 'bernoulli.data.json')

        # synthesize stanfit object -
        # see test_stanfit.py, method 'test_validate_good_run'
        goodfiles_path = os.path.join(datafiles_path, 'runset-good')
        output = os.path.join(goodfiles_path, 'bern')
        sampler_args = SamplerArgs(
            sampling_iters=100, max_treedepth=11, adapt_delta=0.95
        )
        cmdstan_args = CmdStanArgs(
            model_name=model.name,
            model_exe=model.exe_file,
            chain_ids=[1, 2, 3, 4],
            seed=12345,
            data=jdata,
            output_basename=output,
            method_args=sampler_args,
        )
        sampler_fit = StanFit(args=cmdstan_args, chains=4)
        for i in range(4):
            sampler_fit._set_retcode(i, 0)

        bern_fit = model.run_generated_quantities(
            csv_files=sampler_fit.csv_files, data=jdata
        )

        # check results - ouput files, quantities of interest, draws
        self.assertEqual(bern_fit.chains, 4)
        for i in range(4):
            self.assertEqual(bern_fit._retcodes[i], 0)
            csv_file = bern_fit.csv_files[i]
            self.assertTrue(os.path.exists(csv_file))
        column_names = [
            'y_rep.1',
            'y_rep.2',
            'y_rep.3',
            'y_rep.4',
            'y_rep.5',
            'y_rep.6',
            'y_rep.7',
            'y_rep.8',
            'y_rep.9',
            'y_rep.10',
        ]
        self.assertEqual(bern_fit.column_names, tuple(column_names))
        self.assertEqual(bern_fit.draws, 100)


if __name__ == '__main__':
    unittest.main()
