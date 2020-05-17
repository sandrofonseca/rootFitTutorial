#####################################
#
# 'LIKELIHOOD AND MINIMIZATION' ROOT.RooFit tutorial macro #605
#
# Working with the profile likelihood estimator
#
#
#
# 07/2008 - Wouter Verkerke
#
# /


import ROOT


def rf605_profilell():
    # C r e a t e   m o d e l   a n d   d a t a s e t
    # -----------------------------------------------

    # Observable
    x = ROOT.RooRealVar("x", "x", -20, 20)

    # Model (intentional strong correlations)
    mean = ROOT.RooRealVar("mean", "mean of g1 and g2", 0, -10, 10)
    sigma_g1 = ROOT.RooRealVar("sigma_g1", "width of g1", 3)
    g1 = ROOT.RooGaussian("g1", "g1", x, mean, sigma_g1)

    sigma_g2 = ROOT.RooRealVar("sigma_g2", "width of g2", 4, 3.0, 6.0)
    g2 = ROOT.RooGaussian("g2", "g2", x, mean, sigma_g2)

    frac = ROOT.RooRealVar("frac", "frac", 0.5, 0.0, 1.0)
    model = ROOT.RooAddPdf("model", "model", ROOT.RooArgList(
        g1, g2), ROOT.RooArgList(frac))

    # Generate 1000 events
    data = model.generate(ROOT.RooArgSet(x), 1000)

    # C o n s t r u c t   p l a i n   l i k e l i h o o d
    # ---------------------------------------------------

    # Construct unbinned likelihood
    nll = model.createNLL(data, ROOT.RooFit.NumCPU(2))

    # Minimize likelihood w.r.t all parameters before making plots
    ROOT.RooMinuit(nll).migrad()

    # Plot likelihood scan frac
    frame1 = frac.frame(ROOT.RooFit.Bins(10), ROOT.RooFit.Range(
        0.01, 0.95), ROOT.RooFit.Title("LL and profileLL in frac"))
    nll.plotOn(frame1, ROOT.RooFit.ShiftToZero())

    # Plot likelihood scan in sigma_g2
    frame2 = sigma_g2.frame(ROOT.RooFit.Bins(10), ROOT.RooFit.Range(
        3.3, 5.0), ROOT.RooFit.Title("LL and profileLL in sigma_g2"))
    nll.plotOn(frame2, ROOT.RooFit.ShiftToZero())

    # C o n s t r u c t   p r o f i l e   l i k e l i h o o d   i n   f r a c
    # -----------------------------------------------------------------------

    # ROOT.The profile likelihood estimator on nll for frac will minimize nll w.r.t
    # all floating parameters except frac for each evaluation

    pll_frac = nll.createProfile(ROOT.RooArgSet(frac))

    # Plot the profile likelihood in frac
    pll_frac.plotOn(frame1, ROOT.RooFit.LineColor(ROOT.kRed))

    # Adjust frame maximum for visual clarity
    frame1.SetMinimum(0)
    frame1.SetMaximum(3)

    # C o n s t r u c t   p r o f i l e   l i k e l i h o o d   i n   s i g m a _ g 2
    # -------------------------------------------------------------------------------

    # ROOT.The profile likelihood estimator on nll for sigma_g2 will minimize nll
    # w.r.t all floating parameters except sigma_g2 for each evaluation
    pll_sigmag2 = nll.createProfile(ROOT.RooArgSet(sigma_g2))

    # Plot the profile likelihood in sigma_g2
    pll_sigmag2.plotOn(frame2, ROOT.RooFit.LineColor(ROOT.kRed))

    # Adjust frame maximum for visual clarity
    frame2.SetMinimum(0)
    frame2.SetMaximum(3)

    # Make canvas and draw ROOT.RooPlots
    c = ROOT.TCanvas("rf605_profilell", "rf605_profilell", 800, 400)
    c.Divide(2)
    c.cd(1)
    ROOT.gPad.SetLeftMargin(0.15)
    frame1.GetYaxis().SetTitleOffset(1.4)
    frame1.Draw()
    c.cd(2)
    ROOT.gPad.SetLeftMargin(0.15)
    frame2.GetYaxis().SetTitleOffset(1.4)
    frame2.Draw()

    c.SaveAs("rf605_profilell.png")


if __name__ == "__main__":
    rf605_profilell()
