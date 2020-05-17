# /
#
# 'ADDITION AND CONVOLUTION' ROOT.RooFit tutorial macro #207
#
# ROOT.Tools and utilities for manipulation of composite objects
#
#
# 07/2008 - Wouter Verkerke
#
# /


import ROOT


def rf207_comptools():

    # S e t u p   c o m p o s i t e    p d f, a t a s e t
    # --------------------------------------------------------

    # Declare observable x
    x = ROOT.RooRealVar("x", "x", 0, 10)

    # Create two Gaussian PDFs g1(x,mean1,sigma) anf g2(x,mean2,sigma) and
    # their parameters
    mean = ROOT.RooRealVar("mean", "mean of gaussians", 5)
    sigma = ROOT.RooRealVar("sigma", "width of gaussians", 0.5)
    sig = ROOT.RooGaussian("sig", "Signal component 1", x, mean, sigma)

    # Build Chebychev polynomial p.d.f.
    a0 = ROOT.RooRealVar("a0", "a0", 0.5, 0., 1.)
    a1 = ROOT.RooRealVar("a1", "a1", -0.2, 0., 1.)
    bkg1 = ROOT.RooChebychev("bkg1", "Background 1",
                             x, ROOT.RooArgList(a0, a1))

    # Build expontential pdf
    alpha = ROOT.RooRealVar("alpha", "alpha", -1)
    bkg2 = ROOT.RooExponential("bkg2", "Background 2", x, alpha)

    # Sum the background components into a composite background p.d.f.
    bkg1frac = ROOT.RooRealVar(
        "bkg1frac", "fraction of component 1 in background", 0.2, 0., 1.)
    bkg = ROOT.RooAddPdf(
        "bkg", "Signal", ROOT.RooArgList(bkg1, bkg2), ROOT.RooArgList(bkg1frac))

    # Sum the composite signal and background
    bkgfrac = ROOT.RooRealVar("bkgfrac", "fraction of background", 0.5, 0., 1.)
    model = ROOT.RooAddPdf(
        "model", "g1+g2+a", ROOT.RooArgList(bkg, sig), ROOT.RooArgList(bkgfrac))

    # Create dummy dataset that has more observables than the above pdf
    y = ROOT.RooRealVar("y", "y", -10, 10)
    data = ROOT.RooDataSet("data", "data", ROOT.RooArgSet(x, y))

    #############################
    # B a s i c   i n f o r m a t i o n   r e q u e s t s  #
    #############################

    # G e t   l i s t   o f   o b s e r v a b l e s
    # ---------------------------------------------

    # Get list of observables of pdf in context of a dataset
    #
    # Observables are define each context as the variables
    # shared between a model and a dataset. In self case
    # that is the variable 'x'

    model_obs = model.getObservables(data)
    model_obs.Print("v")

    # G e t   l i s t   o f   p a r a m e t e r s
    # -------------------------------------------

    # Get list of parameters, list of observables
    model_params = model.getParameters(ROOT.RooArgSet(x))
    model_params.Print("v")

    # Get list of parameters, a dataset
    # (Gives identical results to operation above)
    model_params2 = model.getParameters(data)
    model_params2.Print()

    # G e t   l i s t   o f   c o m p o n e n t s
    # -------------------------------------------

    # Get list of component objects, top-level node
    model_comps = model.getComponents()
    model_comps.Print("v")

    # /
    # M o d i f i c a t i o n s   t o   s t r u c t u r e   o f   c o m p o s i t e s #
    # /

    # Create a second Gaussian
    sigma2 = ROOT.RooRealVar("sigma2", "width of gaussians", 1)
    sig2 = ROOT.RooGaussian("sig2", "Signal component 1", x, mean, sigma2)

    # Create a sum of the original Gaussian plus the second Gaussian
    sig1frac = ROOT.RooRealVar(
        "sig1frac", "fraction of component 1 in signal", 0.8, 0., 1.)
    sigsum = ROOT.RooAddPdf("sigsum", "sig+sig2",
                            ROOT.RooArgList(sig, sig2), ROOT.RooArgList(sig1frac))

    # Construct a customizer utility to customize model
    cust = ROOT.RooCustomizer(model, "cust")

    # Instruct the customizer to replace node 'sig' with node 'sigsum'
    sigsum = ROOT.RooRealVar()  # just define some kind of RooFit type
    cust.replaceArg(sig, sigsum)

    # Build a clone of the input pdf according to the above customization
    # instructions. Each node that requires modified is clone so that the
    # original pdf remained untouched. ROOT.The name of each cloned node is that
    # of the original node suffixed by the name of the customizer object
    #
    # ROOT.The returned head node own all nodes that were cloned as part of
    # the build process so when cust_clone is deleted so will all other
    # nodes that were created in the process.
    cust_clone = cust.build(ROOT.kTRUE)

    # Print structure of clone of model with sig.sigsum replacement.
    cust_clone.Print("t")


if __name__ == "__main__":
    rf207_comptools()
