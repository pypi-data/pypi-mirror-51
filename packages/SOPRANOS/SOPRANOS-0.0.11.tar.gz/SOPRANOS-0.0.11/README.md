# SOPRANOS

[![PyPI](https://img.shields.io/pypi/v/SOPRANOS.svg?style=flat-square)](https://pypi.python.org/pypi/SOPRANOS)

## Documentation

`SOPRANOS` is a package for modeling the progenitor of a supernova (radius, ejected mass, and other parameters) with the model from Sapir and Waxman (2017).

### What does SOPRANOS do?

The steps are explained in Soumagnac et al. 2019.

SOPRANOS allows you to do 2 main things:

1. Calculate the probability distribution of the progeniotr parameters, with the function `SOPRANOS_fun.emcee_6_param`. In order to do this, it runs a mcmc using the probability defined in equations
(11) and (12) of Soumagnac et al 2019. This task is demonstrated [here](https://github.com/maayane/SOPRANO/blob/master/README.md#calculate-the-probability-distribution-of-the-progeniotr-parameters). 
2. Calculate the most probable combination of progeniotr parameters, with the function `SOPRANOS_fun.calc_best_fit_6_param`. In order to do this, it follows the two following steps:
	1. it calculates the probability of all the combinations in the mcmc chain
	2. it selects the most probable combinations and use them as the initial conditions of an optimising algorithm.
This task is demonstrated [here](https://github.com/maayane/SOPRANO/blob/master/README.md#calculate-the-most-probable-combination-of-progenitor-parameters).
 
In addition to this, it has several usefull functions. You can:
* visualize the marginalized distributions (demonstrated [here](https://github.com/maayane/SOPRANO/blob/master/README.md#visualize-the-2-D-marginalized-probability-distributions))
* plot a model (e.g. the best fit) superimposed with the data (demonstrated [here](https://github.com/maayane/SOPRANO/blob/master/README.md#plot-a-model-eg-the-best-fit-versus-the-data)).
* calculate the validity domain of a given model (demonstrated [here](https://github.com/maayane/SOPRANO/blob/master/README.md#calculate-the-validity-domain-for-a-given-combination-of-parameters-eg-the-best-fit)))
* calculate the chi2/dof for a given model (demonstrated [here](https://github.com/maayane/SOPRANO/blob/master/README.md#calculate-chi2dof-for-a-given-combination-of-parameters-eg-the-best-fit))
* compute symmetric and non-symmetric confidence intervals

## Credit

If you are using SOPRANO, please reference [Soumagnac et al. 2019](https://ui.adsabs.harvard.edu/abs/2019arXiv190711252S/exportcitation), Ganot et al. 2019 (in preparation) and [Sapir & Waxman 2017](https://ui.adsabs.harvard.edu/abs/2017ApJ...838..130S/exportcitation).

## How to install `SOPRANOS`?

### pip

`pip install SOPRANOS`

### Python version
* `python 3`

### Required python packages
* `math`
* `numpy`
* `pylab`
* `emcee`
* `matplotlib`
* `Decimal`

## How to run `SOPRANOS`?

### Edit the params.py file

The first step is to edit the content of the parameters file `params.py` as detailed in [this section](https://github.com/maayane/SOPRANO/blob/master/README.md#the-parameters-file-in-details). Unless you want to give it a try with the default parameters, which allow you to run `SOPRANOS` on the test data from 2018fif (Soumagnac et al 2019), as explained [here](https://github.com/maayane/SOPRANO/blob/master/README.md#give-it-a-try-with-the-test-data).


### Calculate the probability distribution of the progeniotr parameters

The simplest way to run SOPRANOS is
```python
>>> import SOPRANOS
>>> from SOPRANOS import SOPRANOS_fun
>>> import params_test as params
>>> samples= SOPRANOS_fun.emcee_6_param(params.dict_all, data_band_dic=params.data_band_dic,prior_param=[params.to_prior,params.rs_prior,params.vs_prior,params.ms_prior,params.frho_prior,params.ebv_prior],
							dic_transmissions=params.dico,redshift=params.redshift, initial_conditions=params.initial_conditions,
							nwalkers=params.nwalkers,num_steps=params.num_steps,flatchain_path=params.output_mcmc+'/'+params.flatchain_file_name,
							already_run=params.already_run_mcmc,parallel_epochs=True,processes=params.proc)

```
The result of the mcmc run, i.e. the chain, will be put in the file specified in the keyword `flatchain_path`, (below, specified in the parameters file by the pa.

#### Train with the test data!
In the directory `test`, simply running the following code. Look at how it is written. Note that it uses the parameters from the file `params_test.py` 
```python
>>> python main_mcmc_test.py
```

### Visualize the 2-D marginalized probability distributions

To visualize the 2-D marginalized probability distributions, run the function `SOPRANOS_fun.plot_2D_distributions` as follows:
```python
>>>import pylab
>>>triangle = SOPRANOS_fun.plot_2D_distributions(
	flatchain_path=params.output_mcmc+'/'+params.flatchain_file_name, bests=None, title='test_mcmc',
	output_file_path=params.output_mcmc+'/2D-distributions.png', parameters_labels=[r'$t_{\rm exp}$',r'$R$',r'$v_{\rm s*}$',r'$M$',r'$f_{\rho}$',r'$E_{\rm BV}$'],quantiles=[])#quantiles)
>>>pylab.show()
```

<p align="center">
  <img src="./test/output_test_mcmc/2D-distributions.png" width="350">
</p>

You can also superimpose to the plot a given combination of parameters, in blue, e.g. the best-fit you calculated with `SOPRANOS_fun.calc_best_fit_6_param`:

```python
>>>import pylab
>>>[t_best,R_best,vs_best,Mej_best,frho_best,Ebv_best]=[2.458350039588246960e+06,1.126680885134050186e+03,
													 2.163744281199419498e+08,8.040544097550345271e+00,
													 2.230561458966353605e+00,2.313776135439769566e-01]
>>>triangle = SOPRANOS_fun.plot_2D_distributions(
        flatchain_path=params.output_mcmc+'/'+params.flatchain_file_name, bests=[t_best,R_best,vs_best,Mej_best,frho_best,Ebv_best], title='test_mcmc',
        output_file_path=params.output_mcmc+'/2D-distributions.png', parameters_labels=[r'$t_{\rm exp}$',r'$R$',r'$v_{\rm s*}$',r'$M$',r'$f_{\rho}$',r'$E_{\rm BV}$'],quantiles=[])#quantiles)
>>>pylab.show()
```

<p align="center">
  <img src="./test/output_test_mcmc/2D-distributions_wmax.png" width="350">
</p>

#### Train with the test data!
In the directory `test`, simply running the following code. Look at how it is written. Note that it uses the parameters from the file `params_test.py` 
```python
>>> python main_plot2D_test.py
```

### Calculate the most probable combination of progenitor parameters

```python
>>> import SOPRANOS
>>> from SOPRANOS import SOPRANOS_fun
>>> import params_test as params
bests=SOPRANOS_fun.calc_best_fit_6_param(params.dict_all,flatchain_path=params.chain_constrained,data_band_dic=params.data_band_dic,winners=params.winners,output_file_path=params.output_optimizer,ProgType=params.ProgType,model=params.model,
                          bounds=[params.to_prior,params.rs_prior,params.vs_prior,params.ms_prior,params.frho_prior,params.ebv_prior],already_run_calc_all_chis=params.already_run_calc_all_chis,show_plots=True,dilution_factor=params.dilution_factor,
                          parallel_filters=False,parallel_epochs=True,processes=params.proc,filters_directory=None,redshift=params.redshift,simplest=params.simplest,dic_transmissions=params.dico)

```
`bests` is the list with the most probable parameters in the following order: explosion time (in JD), progenitor radius (in solar radii), vs8,5 (see Soumagnac et at. 2019), ejected mass (in solar masses),
                        frho (see Soumagnac et al 2019), extinction Ebv.
			
#### Train with the test data!
In the directory `test`, simply running the following code. Look at how it is written. Note that it uses the parameters from the file `params_test.py` 
```python
>>> python main_optimizer_test.py
```

### Calculate the validity domain for a given combination of parameters (e.g. the best-fit)
First define the combination of parameters for the model you would like to calculate chi2/dof for:
```python
>>>[t_best,R_best,vs_best,Mej_best,frho_best,Ebv_best]=[2.458350039588246960e+06,1.126680885134050186e+03,
                                                                                                         2.163744281199419498e+08,8.040544097550345271e+00,
                                                                                                         2.230561458966353605e+00,2.313776135439769566e-01]
```

Then run the function ``info_model`` as follows:
```python

>>>SOPRANOS_fun.info_model(ProgType=params.ProgType,R=R_best,vs=vs_best,Mej=Mej_best,frho=frho_best,Ebv=Ebv_best,redshift=params.redshift,dic_transmission=params.dico)
***** calculating the validity range for a given combination of parameters *****
**** Validity domain ****
** lower temporal limit:
tmin in the rest-frame is:  3.8274797937844336
tmin*(1+z) (i.e. in the observer frame) is:  3.8932703439597938
** higher temporal limit:
tmax in the rest-frame is:  36.524849456715295
tmax*(1+redshift) (i.e. in observer frame) is:  37.15267509402677
topac in the rest-frame: 16.469115733555245
topac*(1+redshift) (i.e. in the observer frame) is:  16.752203363899326
********************************
As a result, the temporal validity window of this model is [3.8274797937844336, 16.469115733555245] in the rest-frame, or [3.8932703439597938, 16.752203363899326] in the observer frame.
********************************
```


#### Train with the test data!
In the directory `test`, simply running the following code. Look at how it is written. Note that it uses the parameters from the file `params_test.py`
```python
>>> python main_validity_test.py
```



### Calculate chi2/dof for a given combination of parameters (e.g. the best-fit)

First define the combination of parameters for the model you would like to calculate chi2/dof for:
```python
>>>[t_best,R_best,vs_best,Mej_best,frho_best,Ebv_best]=[2.458350039588246960e+06,1.126680885134050186e+03,
													 2.163744281199419498e+08,8.040544097550345271e+00,
													 2.230561458966353605e+00,2.313776135439769566e-01]
```

Then run the function ``pdf_parallel_epochs`` as follows:
```python
>>>[lnprob,chi2dof] = SOPRANOS_fun.pdf_parallel_epochs(params.dict_all, data_band_dic=params.data_band_dic, to=t_best, rs=R_best, vs=vs_best,
							 ms=Mej_best, frho=frho_best, ebv=Ebv_best,
							 ProgType=params.ProgType, model=params.model, dic_transmissions=params.dico, redshift=params.redshift, verbose=True,
							 processes=params.proc, ndim=6,chi2show=True)
***** calculating chi2/dof for a given combination of parameters *****
***** Running pdf_parallel_epochs with: *****
to= 2458350.039588247
rs= 1126.6808851340502
vs= 216374428.11994195
ms= 8.040544097550345
froh= 2.2305614589663536
ebv= 0.23137761354397696
*****
For this model, the total number of valid data points is 115.0
chi2/dof is 0.987365692209
the pdf is 0.02720411338154048175308474810663028620183467864990234375
log(pdf) is -3.604387089851357461734457238
```

#### Train with the test data!
In the directory `test`, simply running the following code. Look at how it is written. Note that it uses the parameters from the file `params_test.py`
```python
>>> python main_chi2dof_test.py
```


### Plot a model (e.g. the best-fit) versus the data
First define the combination of parameters for the model you would like to calculate chi2/dof for:
```python
>>>[t_best,R_best,vs_best,Mej_best,frho_best,Ebv_best]=[2.458350039588246960e+06,1.126680885134050186e+03,
                                                                                                         2.163744281199419498e+08,8.040544097550345271e+00,
                                                                                                         2.230561458966353605e+00,2.313776135439769566e-01]
```

Then run the function ``plot_model_versus_data`` as follows:
```python
>>>SOPRANOS_fun.plot_model_versus_data(params.dict_all,path_to_data=params.path_to_data,path_to_filters=params.filters_directory,ProgType=params.ProgType,texp=t_best,R=R_best,vs=vs_best,Mej=Mej_best,frho=frho_best,Ebv=Ebv_best,redshift=params.redshift,dic_transmission=params.dico,output_flux_file='output_test_various/SW_model_flux.txt',kappa=None,output_file_path='model_versus_data.png')
```
<p align="center">
  <img src="./test/output_test_various/model_versus_data.png" width="350">
</p>

#### Train with the test data!
In the directory `test`, simply running the following code. Look at how it is written. Note that it uses the parameters from the file `params_test.py`
```python
>>> python main_plotmodeldata_test.py
```

### Compute the (non-symmetric) 1-sigma confidence interval

the 1-sigma confidence interval are computed as the shortest intervals containing 68% of the marginalized posterior probability.
#### Train with the test data!
In the directory `test`, simply run the following code. Look at how it is written. Note that it uses the parameters from the file `params_test.py`
```python
>>> python main_plot1D_test.py
```
<p align="center">
  <img src="./test/output_test_mcmc/1D-distributions.png" width="350">
</p>

## The parameters file in details

Let's dive into the parameters file in full details. You can look at the example file `params_test.py` containing parameters used by all the scripts starting with `main_`, in the `test` directory.

DOCUMENTATION WORK IN PROGRESS

## Give it a try with the test data!

All the figures above were obtained by running `SOPRANOS` on the multiple-bands light curve of the Supernova 2018fif (Soumagnac et al 2019). The data is available in the `test` directory (including the output of the time-consuming steps). You can reproduce all these results and figures by running `SOPRANOS` with the parameters file `params_test.py` as it is.



