#####################################
#
# 'SPECIAL PDFS' ROOT.RooFit tutorial macro #705
#
# Linear interpolation between p.d.f shapes using the 'Alex Read' algorithm
#
#
#
# 07/2008 - Wouter Verkerke
#
# /


import ROOT


def rf705_linearmorph():
    # C r e a t e   e n d   p o i n t   p d f   s h a p e s
    # ------------------------------------------------------

    # Observable
    x = ROOT.RooRealVar("x", "x", -20, 20)

    # Lower end point shape: a Gaussian
    g1mean = ROOT.RooRealVar("g1mean", "g1mean", -10)
    g1 = ROOT.RooGaussian("g1", "g1", x, g1mean, ROOT.RooFit.RooConst(2))

    # Upper end point shape: a Polynomial
    g2 = ROOT.RooPolynomial("g2", "g2", x, ROOT.RooArgList(
        ROOT.RooFit.RooConst(-0.03), ROOT.RooFit.RooConst(-0.001)))

    # C r e a t e   i n t e r p o l a t i n g   p d f
    # -----------------------------------------------

    # Create interpolation variable
    alpha = ROOT.RooRealVar("alpha", "alpha", 0, 1.0)

    # Specify sampling density on observable and interpolation variable
    x.setBins(1000, "cache")
    alpha.setBins(50, "cache")

    # Construct interpolating pdf in (x,a) represent g1(x) at a=a_min
    # and g2(x) at a=a_max
    lmorph = ROOT.RooIntegralMorph("lmorph", "lmorph", g1, g2, x, alpha)

    # P l o t   i n t e r p o l a t i n g   p d f   a t   v a r i o u s   a l p h a
    # -----------------------------------------------------------------------------

    # Show end points as blue curves
    frame1 = x.frame()
    g1.plotOn(frame1)
    g2.plotOn(frame1)

    # Show interpolated shapes in red
    alpha.setVal(0.125)
    lmorph.plotOn(frame1, ROOT.RooFit.LineColor(ROOT.kRed))
    alpha.setVal(0.25)
    lmorph.plotOn(frame1, ROOT.RooFit.LineColor(ROOT.kRed))
    alpha.setVal(0.375)
    lmorph.plotOn(frame1, ROOT.RooFit.LineColor(ROOT.kRed))
    alpha.setVal(0.50)
    lmorph.plotOn(frame1, ROOT.RooFit.LineColor(ROOT.kRed))
    alpha.setVal(0.625)
    lmorph.plotOn(frame1, ROOT.RooFit.LineColor(ROOT.kRed))
    alpha.setVal(0.75)
    lmorph.plotOn(frame1, ROOT.RooFit.LineColor(ROOT.kRed))
    alpha.setVal(0.875)
    lmorph.plotOn(frame1, ROOT.RooFit.LineColor(ROOT.kRed))
    alpha.setVal(0.95)
    lmorph.plotOn(frame1, ROOT.RooFit.LineColor(ROOT.kRed))

    # S h o w   2 D   d i s t r i b u t i o n   o f   p d f ( x , l p h a )
    # -----------------------------------------------------------------------

    # Create 2D histogram
    hh = lmorph.createHistogram("hh", x, ROOT.RooFit.Binning(
        40), ROOT.RooFit.YVar(alpha, ROOT.RooFit.Binning(40)))
    hh.SetLineColor(ROOT.kBlue)

    # F i t   p d f   t o   d a t a s e t   w i t h   a l p a = 0 . 8
    # -----------------------------------------------------------------

    # Generate a toy dataset alpha = 0.8
    alpha.setVal(0.8)
    data = lmorph.generate(ROOT.RooArgSet(x), 1000)

    # Fit pdf to toy data
    lmorph.setCacheAlpha(ROOT.kTRUE)
    lmorph.fitTo(data, ROOT.RooFit.Verbose(ROOT.kTRUE))

    # Plot fitted pdf and data overlaid
    frame2 = x.frame(ROOT.RooFit.Bins(100))
    data.plotOn(frame2)
    lmorph.plotOn(frame2)

    # S c a n   - l o g ( L )   v s   a l p h a
    # -----------------------------------------

    # Show scan -log(L) of dataset w.r.t alpha
    frame3 = alpha.frame(ROOT.RooFit.Bins(100), ROOT.RooFit.Range(0.1, 0.9))

    # Make 2D pdf of histogram
    nll = ROOT.RooNLLVar("nll", "nll", lmorph, data)
    nll.plotOn(frame3, ROOT.RooFit.ShiftToZero())

    lmorph.setCacheAlpha(ROOT.kFALSE)

    c = ROOT.TCanvas("rf705_linearmorph", "rf705_linearmorph", 800, 800)
    c.Divide(2, 2)
    c.cd(1)
    ROOT.gPad.SetLeftMargin(0.15)
    frame1.GetYaxis().SetTitleOffset(1.6)
    frame1.Draw()
    c.cd(2)
    ROOT.gPad.SetLeftMargin(0.20)
    hh.GetZaxis().SetTitleOffset(2.5)
    hh.Draw("surf")
    c.cd(3)
    ROOT.gPad.SetLeftMargin(0.15)
    frame3.GetYaxis().SetTitleOffset(1.4)
    frame3.Draw()
    c.cd(4)
    ROOT.gPad.SetLeftMargin(0.15)
    frame2.GetYaxis().SetTitleOffset(1.4)
    frame2.Draw()

    c.SaveAs("rf705_linearmorph.png")

    return


if __name__ == "__main__":
    rf705_linearmorph()
