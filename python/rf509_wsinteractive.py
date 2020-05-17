# /
#
# 'ORGANIZATION AND SIMULTANEOUS FITS' ROOT.RooFit tutorial macro #509
#
#  Easy CINT interactive access to workspace contents through a
#  'C++' namespace in CINT that maps the workspace contents in a typesafe way
#
#  *********************************************************************************
#  *** NB: ROOT.This macro exploits a feature native to CINT and _cannot_ be compiled ***
#  *********************************************************************************
#
# 04/2009 - Wouter Verkerke
#
# /

import ROOT


def rf509_wsinteractive():
    # C r e a t e  a n d   f i l l   w o r k s p a c e
    # ------------------------------------------------

    # Create a workspace named 'w'
    # With CINT w could exports its contents to
    # a same-name C++ namespace in CINT 'namespace w'.
    # but self does not work anymore in CLING.
    # so self tutorial is an example on how to
    # change the code
    w = ROOT.RooWorkspace("w", ROOT.kTRUE)

    # Fill workspace with p.d.f. and data in a separate function
    fillWorkspace(w)

    # Print workspace contents
    w.Print()

    # self does not work anymore with CLING
    # use normal workspace functionality

    # U s e   w o r k s p a c e   c o n t e n t s
    # ----------------------------------------------

    # Old syntax to use the name space prefix operator to access the workspace contents
    #
    #d = w.model.generate(w.x,1000)
    #r = w.model.fitTo(*d)

    # use normal workspace methods
    model = w.pdf("model")
    x = w.var("x")

    d = model.generate(ROOT.RooArgSet(x), 1000)
    r = model.fitTo(d)

    # old syntax to access the variable x
    # frame = w.x.frame()

    frame = x.frame()
    d.plotOn(frame)

    # OLD syntax to ommit x.
    # NB: ROOT.The 'w.' prefix can be omitted if namespace w is imported in local namespace
    # in the usual C++ way
    #
    # using namespace w
    # model.plotOn(frame)
    # model.plotOn(frame, ROOT.RooFit.Components(bkg), ROOT.RooFit.LineStyle(ROOT.kDashed))

    # correct syntax
    bkg = w.pdf("bkg")
    model.plotOn(frame)
    ras_bkg = ROOT.RooArgSet(bkg)
    model.plotOn(frame, ROOT.RooFit.Components(ras_bkg),
                 ROOT.RooFit.LineStyle(ROOT.kDashed))

    # Draw the frame on the canvas
    c = ROOT.TCanvas("rf509_wsinteractive", "rf509_wsinteractive", 600, 600)
    ROOT.gPad.SetLeftMargin(0.15)
    frame.GetYaxis().SetTitleOffset(1.4)
    frame.Draw()

    c.SaveAs("rf509_wsinteractive.png")


def fillWorkspace(w):
    # C r e a t e  p d f   a n d   f i l l   w o r k s p a c e
    # --------------------------------------------------------

    # Declare observable x
    x = ROOT.RooRealVar("x", "x", 0, 10)

    # Create two Gaussian PDFs g1(x,mean1,sigma) anf g2(x,mean2,sigma) and
    # their parameters
    mean = ROOT.RooRealVar("mean", "mean of gaussians", 5, 0, 10)
    sigma1 = ROOT.RooRealVar("sigma1", "width of gaussians", 0.5)
    sigma2 = ROOT.RooRealVar("sigma2", "width of gaussians", 1)

    sig1 = ROOT.RooGaussian("sig1", "Signal component 1", x, mean, sigma1)
    sig2 = ROOT.RooGaussian("sig2", "Signal component 2", x, mean, sigma2)

    # Build Chebychev polynomial p.d.f.
    a0 = ROOT.RooRealVar("a0", "a0", 0.5, 0., 1.)
    a1 = ROOT.RooRealVar("a1", "a1", -0.2, 0., 1.)
    bkg = ROOT.RooChebychev("bkg", "Background", x, ROOT.RooArgList(a0, a1))

    # Sum the signal components into a composite signal p.d.f.
    sig1frac = ROOT.RooRealVar(
        "sig1frac", "fraction of component 1 in signal", 0.8, 0., 1.)
    sig = ROOT.RooAddPdf(
        "sig", "Signal", ROOT.RooArgList(sig1, sig2), ROOT.RooArgList(sig1frac))

    # Sum the composite signal and background
    bkgfrac = ROOT.RooRealVar("bkgfrac", "fraction of background", 0.5, 0., 1.)
    model = ROOT.RooAddPdf(
        "model", "g1+g2+a", ROOT.RooArgList(bkg, sig), ROOT.RooArgList(bkgfrac))

    getattr(w, 'import')(model)


if __name__ == "__main__":
    rf509_wsinteractive()
