# /
#
# 'MULTIDIMENSIONAL MODELS' ROOT.RooFit tutorial macro #301
#
# Multi-dimensional p.d.f.s through composition, e.g. substituting a
# p.d.f parameter with a function that depends on other observables
#
# pdf = gauss(x,f(y),s) with f(y) = a0 + a1*y
#
#
# 07/2008 - Wouter Verkerke
#
# /


import ROOT


def rf301_composition():
    # S e t u p   c o m p o s e d   m o d e l   g a u s s ( x , m ( y ) , s )
    # -----------------------------------------------------------------------

    # Create observables
    x = ROOT.RooRealVar("x", "x", -5, 5)
    y = ROOT.RooRealVar("y", "y", -5, 5)

    # Create function f(y) = a0 + a1*y
    a0 = ROOT.RooRealVar("a0", "a0", -0.5, -5, 5)
    a1 = ROOT.RooRealVar("a1", "a1", -0.5, -1, 1)
    fy = ROOT.RooPolyVar("fy", "fy", y, ROOT.RooArgList(a0, a1))

    # Creat gauss(x,f(y),s)
    sigma = ROOT.RooRealVar("sigma", "width of gaussian", 0.5)
    model = ROOT.RooGaussian(
        "model", "Gaussian with shifting mean", x, fy, sigma)

    # S a m p l e   d a t a , l o t   d a t a   a n d   p d f   o n   x   a n d   y
    # ---------------------------------------------------------------------------------

    # Generate 10000 events in x and y from model
    data = model.generate(ROOT.RooArgSet(x, y), 10000)

    # Plot x distribution of data and projection of model x = Int(dy)
    # model(x,y)
    xframe = x.frame()
    data.plotOn(xframe)
    model.plotOn(xframe)

    # Plot x distribution of data and projection of model y = Int(dx)
    # model(x,y)
    yframe = y.frame()
    data.plotOn(yframe)
    model.plotOn(yframe)

    # Make two-dimensional plot in x vs y
    hh_model = model.createHistogram("hh_model", x, ROOT.RooFit.Binning(
        50), ROOT.RooFit.YVar(y, ROOT.RooFit.Binning(50)))
    hh_model.SetLineColor(ROOT.kBlue)

    # Make canvas and draw ROOT.RooPlots
    c = ROOT.TCanvas("rf301_composition", "rf301_composition", 1200, 400)
    c.Divide(3)
    c.cd(1)
    ROOT.gPad.SetLeftMargin(0.15)
    xframe.GetYaxis().SetTitleOffset(1.4)
    xframe.Draw()
    c.cd(2)
    ROOT.gPad.SetLeftMargin(0.15)
    yframe.GetYaxis().SetTitleOffset(1.4)
    yframe.Draw()
    c.cd(3)
    ROOT.gPad.SetLeftMargin(0.20)
    hh_model.GetZaxis().SetTitleOffset(2.5)
    hh_model.Draw("surf")

    c.SaveAs("rf301_composition.png")


if __name__ == "__main__":
    rf301_composition()
